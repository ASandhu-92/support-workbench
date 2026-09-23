"""Billing lookups against the Stripe sandbox, and the only two writes this tool can make.

Reads (safe, used by the pipeline):
    python billing.py lookup dana.ivers@example.com

Writes (never run by the pipeline; a person runs them after reading the draft):
    python billing.py refund ch_... --reason "duplicate charge"                       # refused
    python billing.py refund ch_... --reason "duplicate charge" --confirm --approved-by "your name"
    python billing.py cancel sub_... --reason "customer asked" --confirm --approved-by "your name"

Guardrails:
- Only a Stripe test-mode key is accepted. A live key is refused before any network call.
- A write without --confirm and a named approver is refused, and the refusal is logged.
- Every write attempt, allowed or refused, is appended to logs/billing_actions.jsonl.
"""
import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

import stripe

HERE = Path(__file__).resolve().parent
AUDIT_LOG = Path(os.environ.get("WORKBENCH_AUDIT_LOG") or HERE / "logs" / "billing_actions.jsonl")
TAG = {"workbench": "buildbox"}


class BillingError(RuntimeError):
    pass


def check_key(key: str | None) -> str:
    if not key:
        raise BillingError("STRIPE_TEST_SECRET_KEY is not set; export it from the encrypted env file first")
    parts = key.split("_")
    if len(parts) < 3 or parts[0] not in ("sk", "rk") or parts[1] != "test":
        raise BillingError("refusing to run: this is not a Stripe test-mode key")
    return key


def configure() -> None:
    key = check_key(os.environ.get("STRIPE_TEST_SECRET_KEY"))
    stripe.api_key = key


def _iso(ts: int | None) -> str | None:
    return dt.datetime.fromtimestamp(ts, dt.UTC).strftime("%Y-%m-%d %H:%M UTC") if ts else None


def _usd(cents: int | None) -> float | None:
    return None if cents is None else round(cents / 100, 2)


def meta(obj) -> dict:
    """Metadata as a plain dict (StripeObject is not a dict in stripe-python 15)."""
    return obj.metadata.to_dict() if obj.metadata else {}


def find_customer(email: str):
    """Customer.list by email first; search as a fallback (it is eventually consistent)."""
    email = email.lower()
    found = stripe.Customer.list(email=email, limit=10).data
    if not found:
        found = stripe.Customer.search(query=f"email:'{email}'", limit=10).data
    ours = [c for c in found if meta(c).get("workbench") == TAG["workbench"]]
    return (ours or found or [None])[0]


def lookup(email: str) -> dict:
    """Everything a support agent needs to answer a billing ticket. Read-only."""
    cust = find_customer(email)
    if cust is None:
        return {"email": email.lower(), "customer": None}
    view = {
        "email": email.lower(),
        "customer": {"id": cust.id, "name": cust.name, "created": _iso(cust.created),
                     "delinquent": cust.delinquent},
        "subscriptions": [], "invoices": [], "charges": [], "refunds": [],
    }
    for sub in stripe.Subscription.list(customer=cust.id, status="all", limit=10).data:
        item = sub["items"].data[0]
        price = item.price
        view["subscriptions"].append({
            "id": sub.id, "status": sub.status,
            "plan": meta(price).get("plan") or price.nickname or price.id,
            "amount_usd": _usd(price.unit_amount),
            "interval": price.recurring.interval if price.recurring else None,
            "cancel_at_period_end": sub.cancel_at_period_end,
            "current_period_end": _iso(item.current_period_end),
        })
    for inv in stripe.Invoice.list(customer=cust.id, limit=5).data:
        view["invoices"].append({
            "id": inv.id, "status": inv.status, "billing_reason": inv.billing_reason,
            "created": _iso(inv.created), "amount_due_usd": _usd(inv.amount_due),
            "amount_paid_usd": _usd(inv.amount_paid), "attempt_count": inv.attempt_count,
            "customer_name_on_invoice": inv.customer_name,
            "lines": [{"description": ln.description, "amount_usd": _usd(ln.amount)}
                      for ln in inv.lines.data],
        })
    for ch in stripe.Charge.list(customer=cust.id, limit=10).data:
        view["charges"].append({
            "id": ch.id, "created": _iso(ch.created), "amount_usd": _usd(ch.amount),
            "status": ch.status, "description": ch.description, "refunded": ch.refunded,
            "amount_refunded_usd": _usd(ch.amount_refunded),
            "failure_code": ch.failure_code, "failure_message": ch.failure_message,
        })
        if ch.amount_refunded:
            for rf in stripe.Refund.list(charge=ch.id, limit=10).data:
                view["refunds"].append({"id": rf.id, "charge": ch.id, "amount_usd": _usd(rf.amount),
                                        "status": rf.status, "created": _iso(rf.created)})
    return view


def audit(entry: dict) -> None:
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    entry = {"at": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"), **entry}
    with AUDIT_LOG.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def guard(action: str, target: str, confirm: bool, approved_by: str | None, reason: str) -> None:
    """Refuse (and log the refusal) unless a named person confirmed this exact write."""
    approver = (approved_by or "").strip()
    if not confirm or not approver:
        missing = "--confirm" if not confirm else "--approved-by"
        audit({"action": action, "target": target, "reason": reason, "approved_by": approver or None,
               "executed": False, "refused": f"missing {missing}"})
        raise BillingError(f"refused: {action} on {target} needs {missing}. Nothing was changed.")


def refund(charge_id: str, *, reason: str, amount_cents: int | None = None,
           confirm: bool = False, approved_by: str | None = None) -> dict:
    guard("refund", charge_id, confirm, approved_by, reason)
    kwargs = {"charge": charge_id, "metadata": {"approved_by": approved_by, "reason": reason}}
    if amount_cents:
        kwargs["amount"] = amount_cents
    rf = stripe.Refund.create(**kwargs)
    audit({"action": "refund", "target": charge_id, "reason": reason, "approved_by": approved_by,
           "executed": True, "stripe_id": rf.id, "amount_usd": _usd(rf.amount), "status": rf.status})
    return {"refund": rf.id, "amount_usd": _usd(rf.amount), "status": rf.status}


def cancel(subscription_id: str, *, reason: str, confirm: bool = False,
           approved_by: str | None = None) -> dict:
    """Cancel at period end (the customer keeps what they paid for; KB-15)."""
    guard("cancel", subscription_id, confirm, approved_by, reason)
    sub = stripe.Subscription.modify(subscription_id, cancel_at_period_end=True,
                                     metadata={"cancel_approved_by": approved_by, "cancel_reason": reason})
    audit({"action": "cancel", "target": subscription_id, "reason": reason, "approved_by": approved_by,
           "executed": True, "cancel_at_period_end": sub.cancel_at_period_end})
    return {"subscription": sub.id, "cancel_at_period_end": sub.cancel_at_period_end}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    lk = sp.add_parser("lookup"); lk.add_argument("email")
    for name in ("refund", "cancel"):
        p = sp.add_parser(name)
        p.add_argument("target")
        p.add_argument("--reason", required=True)
        p.add_argument("--confirm", action="store_true")
        p.add_argument("--approved-by")
        if name == "refund":
            p.add_argument("--amount-cents", type=int)
    a = ap.parse_args(argv)
    try:
        configure()
        if a.cmd == "lookup":
            out = lookup(a.email)
        elif a.cmd == "refund":
            out = refund(a.target, reason=a.reason, amount_cents=a.amount_cents,
                         confirm=a.confirm, approved_by=a.approved_by)
        else:
            out = cancel(a.target, reason=a.reason, confirm=a.confirm, approved_by=a.approved_by)
    except BillingError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
