"""Run the whole pipeline on data/tickets.json and grade it against expected/expected.json.

    ./run.sh run_all.py              (Stripe key from the encrypted env file; see README)
    python run_all.py --no-stripe    (skip the billing lookups; billing drafts will be weaker)
    python run_all.py --no-cache     (call the model again for every step)
    python run_all.py --set heldout  (the 8 held-out tickets; results go to results/heldout/)

For each ticket: classify -> (tier 2: read-only billing lookup) -> draft a cited reply, or
(tier 3) write an engineering handoff. Then one digest over the week, then the grade.
Nothing in this file can refund or cancel anything: it never calls billing.refund or billing.cancel.
Outputs go to results/.
"""
import argparse
import datetime as dt
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import classify
import digest
import draft
import escalate
import grade
import llm
from tickets import load_tickets

HERE = Path(__file__).resolve().parent
ID_RE = re.compile(r"\b(cus|ch|sub|in|re|pi|pm|prod|price)_[A-Za-z0-9]{8,}\b")


def mask(text: str) -> str:
    """Sandbox object ids are not secrets, but the public results do not need them."""
    return ID_RE.sub(lambda m: f"{m.group(1)}_****{m.group(0)[-4:]}", text)


def process(ticket: dict, use_cache: bool, stripe_on: bool) -> dict:
    t0 = time.monotonic()
    calls = []
    row = {"id": ticket["id"], "subject": ticket["subject"], "body": ticket["body"], "error": None}
    try:
        c = classify.classify(ticket, use_cache)
        calls.append(c)
        cls = c["output"]
        row.update(tier=cls["tier"], topic=cls["topic"], urgency=cls["urgency"], reason=cls["reason"])
        account = None
        if stripe_on and (cls["tier"] == 2 or cls["topic"].startswith("billing-")):
            import billing
            account = billing.lookup(ticket["email"])
        row["account_looked_up"] = account is not None and account.get("customer") is not None
        if cls["tier"] == 3:
            e = escalate.escalate(ticket, cls, use_cache)
            calls.append(e)
            row["escalation"] = e["note"]
            row["escalation_md"] = escalate.to_markdown(ticket, cls, e["note"])
            d = None
        else:
            dr = draft.draft(ticket, account, use_cache)
            calls.append(dr)
            d = dr["draft"]
            row["draft"] = d
        row["action"] = grade.final_action(cls["tier"], d)
        row["cited"] = d["cited_articles"] if d else []
        ba = d["proposed_billing_action"]["type"] if d else "none"
        row["billing_action"] = None if ba == "none" else ba
    except llm.LLMError as exc:
        row.update(error=str(exc), tier=None, topic=None, action="error", cited=[], billing_action=None)
    row["calls"] = [{"cost_usd": k["cost_usd"], "duration_ms": k["duration_ms"], "models": k["models"],
                     "cached": k["cached"]} for k in calls]
    row["seconds"] = round(time.monotonic() - t0, 1)
    return row


def refunds_since(start_ts: int) -> int:
    import stripe
    return len(list(stripe.Refund.list(created={"gte": start_ts}, limit=100).auto_paging_iter()))


def read_audit(start_iso: str) -> list[dict]:
    import billing
    if not billing.AUDIT_LOG.exists():
        return []
    rows = [json.loads(l) for l in billing.AUDIT_LOG.read_text().splitlines() if l.strip()]
    return [r for r in rows if r["at"] >= start_iso]


def write_results(rows, dig, dig_md, g, run, ticket_set="main"):
    out_dir = HERE / "results" if ticket_set == "main" else HERE / "results" / ticket_set
    out_dir.mkdir(exist_ok=True)
    (out_dir / "escalations").mkdir(exist_ok=True)
    exp = grade.load_expected(ticket_set)

    def yn(ok):
        return "yes" if ok else "**no**"

    table = ["| Ticket | Subject | Tier (exp/got) | Topic (exp / got) | Action (exp / got) | Cited | Right? |",
             "|---|---|---|---|---|---|---|"]
    for r in rows:
        e = exp[r["id"]]
        ok = r["tier"] == e["tier"] and r["topic"] == e["topic"] and r["action"] == e["action"]
        topic = r["topic"] if r["topic"] == e["topic"] else f"{e['topic']} / **{r['topic']}**"
        action = r["action"] if r["action"] == e["action"] else f"{e['action']} / **{r['action']}**"
        tier = f"{e['tier']}/{r['tier']}" if r["tier"] == e["tier"] else f"{e['tier']}/**{r['tier']}**"
        table.append(f"| {r['id']} | {r['subject']} | {tier} | {topic} | {action} | "
                     f"{', '.join(r['cited']) or '-'} | {yn(ok)} |")
    (out_dir / "tickets.md").write_text("# Per-ticket results\n\nBold marks a miss against "
                                        "the answer key in `expected/`.\n\n" + "\n".join(table) + "\n")

    out = ["# Drafts and routing, ticket by ticket", "",
           "Every reply below is a draft for a human to review. Billing actions are proposals only; "
           "the command shown is what a person would run after checking.", ""]
    for r in rows:
        out += [f"## {r['id']}: {r['subject']}", "",
                f"Tier {r['tier']}, {r['topic']}, urgency {r.get('urgency')}. Outcome: **{r['action']}**. "
                f"{r.get('reason', '')}", ""]
        if r.get("error"):
            out += [f"Error: {r['error']}", ""]
        elif r["action"] == "escalate-engineering":
            out += [f"Handoff note: [escalations/{r['id']}.md](escalations/{r['id']}.md)", ""]
        else:
            d = r["draft"]
            if d["status"] == draft.NO_SOURCE:
                out += [f"`{draft.NO_SOURCE}`. Missing from the KB: {d['missing_from_kb']}", ""]
            else:
                if d["status"] == draft.MANUAL_REVIEW:
                    out += [f"`{draft.MANUAL_REVIEW}`: {d['manual_review_reason']}. The reply below is "
                            "for a person to rework, not to send.", ""]
                out += [f"Cites {', '.join(d['cited_articles'])}.", "",
                        "> " + d["reply"].replace("\n", "\n> "), ""]
            pa = d["proposed_billing_action"]
            if pa.get("type") != "none" and pa.get("blocked"):
                out += [f"Proposed billing action **blocked**: {pa['type']} ${pa.get('amount_usd', 0):.2f}. "
                        f"{pa['blocked']}. No command is offered.", ""]
            elif pa.get("type") != "none":
                cmd = (f"python billing.py {pa['type']} {pa['target_id']} --reason \"{pa['why']}\" "
                       f"--confirm --approved-by \"<your name>\"")
                checks = pa.get("unverified_conditions") or []
                out += [f"Proposed billing action, **waiting for a human**: {pa['type']} "
                        f"${pa.get('amount_usd', 0):.2f}. Reason: {pa['why']}", ""]
                if checks:
                    out += ["Check before approving (not in the account data): " + "; ".join(checks), ""]
                out += [f"`{cmd}`", ""]
                if pa.get("also_cancel_subscription_id"):
                    out += ["The policy also cancels the plan. After the refund, run:", "",
                            f"`python billing.py cancel {pa['also_cancel_subscription_id']} --reason \"{pa['why']}\" "
                            f"--confirm --approved-by \"<your name>\"`", ""]
            if d.get("note_for_agent"):
                out += [f"Note for the reviewer: {d['note_for_agent']}", ""]
    (out_dir / "replies.md").write_text(mask("\n".join(out)))

    for r in rows:
        if r.get("escalation_md"):
            (out_dir / "escalations" / f"{r['id']}.md").write_text(mask(r["escalation_md"]))
    (out_dir / "digest.md").write_text(dig_md)

    w = g["wrong"]
    gm = ["# Grade", "", f"Run {run['started']}, model {', '.join(run['models'])}, "
          f"{run['llm_calls']} model calls, cost ${run['cost_usd_cold']:.4f} (list price), "
          f"wall time {run['wall_seconds']}s with {run['workers']} tickets in parallel.", "",
          "| Measure | Result |", "|---|---|"]
    for k in ("tier_accuracy", "topic_accuracy", "action_accuracy", "drafts_sent_for_review",
              "drafts_citing_a_kb_article", "drafts_citing_an_expected_article", "escalations_correct",
              "escalations_missed", "escalations_not_needed", "billing_proposals_correct",
              "billing_proposals_unexpected", "unapproved_billing_writes", "stripe_refunds_created_during_run"):
        gm.append(f"| {k.replace('_', ' ')} | {g[k]} |")
    gm += ["", "## Misses", ""]
    for kind in ("tier", "topic", "action"):
        gm.append(f"**{kind}:** " + ("; ".join(w[kind]) if w[kind] else "none"))
        gm.append("")
    (out_dir / "grade.md").write_text("\n".join(gm))

    slim = [{k: v for k, v in r.items() if k not in ("escalation_md", "body")} for r in rows]
    (out_dir / "run.json").write_text(mask(json.dumps({"run": run, "grade": g, "tickets": slim,
                                                       "digest": dig}, indent=2)) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-cache", action="store_true")
    ap.add_argument("--no-stripe", action="store_true")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--set", dest="ticket_set", choices=["main", "heldout"], default="main")
    a = ap.parse_args()
    use_cache, stripe_on = not a.no_cache, not a.no_stripe
    if stripe_on:
        import billing
        billing.configure()

    started = dt.datetime.now(dt.UTC).replace(microsecond=0)
    start_ts = int(started.timestamp())
    t0 = time.monotonic()
    tickets = list(load_tickets(a.ticket_set).values())
    with ThreadPoolExecutor(max_workers=a.workers) as pool:
        rows = list(pool.map(lambda t: process(t, use_cache, stripe_on), tickets))
    for r in rows:
        print(f"{r['id']} tier={r['tier']} topic={r['topic']} action={r['action']} "
              f"cited={','.join(r['cited']) or '-'} {r['seconds']}s" + (f" ERROR {r['error']}" if r['error'] else ""))

    gaps = [{"id": r["id"], "missing": r["draft"]["missing_from_kb"]} for r in rows
            if r.get("draft") and r["draft"]["status"] == draft.NO_SOURCE]
    ok_rows = [r for r in rows if not r["error"]]
    d = digest.build([{**r, "body": r["body"]} for r in ok_rows], use_cache)
    week = f"{min(t['received'] for t in tickets)[:10]} to {max(t['received'] for t in tickets)[:10]}"
    dig_md = digest.to_markdown(d["digest"], gaps, week)
    wall = round(time.monotonic() - t0, 1)

    calls = [c for r in rows for c in r["calls"]] + [{"cost_usd": d["cost_usd"], "duration_ms": d["duration_ms"],
                                                       "models": d["models"], "cached": d["cached"]}]
    audit = read_audit(started.isoformat()) if stripe_on else []
    refunds = refunds_since(start_ts) if stripe_on else None
    results = {r["id"]: r for r in rows}
    g = grade.grade(results, grade.load_expected(a.ticket_set), audit, refunds or 0)
    run = {
        "ticket_set": a.ticket_set, "started": started.isoformat(), "wall_seconds": wall, "workers": a.workers,
        "llm_calls": len(calls), "cached_calls": sum(c["cached"] for c in calls),
        "cost_usd_this_run": round(sum(c["cost_usd"] for c in calls if not c["cached"]), 4),
        "cost_usd_cold": round(sum(c["cost_usd"] for c in calls), 4),
        "model_seconds_total": round(sum(c["duration_ms"] for c in calls) / 1000, 1),
        "models": sorted({m for c in calls for m in c["models"]}),
        "stripe_lookups": sum(1 for r in rows if r.get("account_looked_up")),
        "errors": [r["id"] for r in rows if r["error"]],
    }
    write_results(rows, d["digest"], dig_md, g, run, a.ticket_set)
    print(json.dumps({"run": run, "grade": {k: v for k, v in g.items() if k != "wrong"}}, indent=2))


if __name__ == "__main__":
    main()
