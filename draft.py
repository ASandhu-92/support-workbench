"""Draft a customer reply that cites the knowledge base, or say "escalate: no source".

    python draft.py T-07
    python draft.py T-13 --lookup      also pull the customer's sandbox billing data (needs the key)

The model is told to answer only from the KB articles and the account data it is given. The code
then enforces it: a reply with no valid KB article id is thrown away and the ticket becomes
"escalate: no source". A proposed refund or cancellation is only a proposal; its target id must
appear in the account data, and nothing is executed here.
"""
import argparse
import json
import re

import kb
import llm
from tickets import load_tickets

NO_SOURCE = "escalate: no source"

SCHEMA = {
    "type": "object",
    "properties": {
        "can_answer_from_kb": {"type": "boolean"},
        "cited_articles": {"type": "array", "items": {"type": "string", "pattern": "^KB-[0-9]{2}$"}},
        "reply": {"type": "string"},
        "missing_from_kb": {"type": "string"},
        "proposed_billing_action": {
            "type": "object",
            "properties": {
                "type": {"type": "string", "enum": ["none", "refund", "cancel"]},
                "target_id": {"type": "string"},
                "amount_usd": {"type": "number"},
                "why": {"type": "string"},
            },
            "required": ["type", "target_id", "amount_usd", "why"],
            "additionalProperties": False,
        },
        "note_for_agent": {"type": "string"},
    },
    "required": ["can_answer_from_kb", "cited_articles", "reply", "missing_from_kb",
                 "proposed_billing_action", "note_for_agent"],
    "additionalProperties": False,
}

SYSTEM = """You draft replies for Buildbox support (Buildbox is an AI app builder). A human support
agent reviews every draft before it is sent.

Rules:
1. Use only the knowledge base articles and the account data you are given. If they do not contain
   what the customer needs, set can_answer_from_kb to false, leave reply empty, and say in
   missing_from_kb what fact is missing. Do not guess, and do not answer from general knowledge.
2. List in cited_articles every KB article id your reply relies on. A reply with no citation will
   be discarded.
3. Never say a refund, cancellation or other account change has been done unless the account data
   shows it already happened. If one is needed, put it in proposed_billing_action (target_id must
   be a charge id "ch_..." for a refund or a subscription id "sub_..." for a cancel, copied from the
   account data) and tell the customer a teammate will confirm it shortly. Otherwise set type
   "none", target_id "", amount_usd 0, why "".
4. The account data comes from a test sandbox that was set up on the day of this run, so its dates
   will not match the ticket's dates. Do not mention that or treat it as a problem.
5. Style: plain, warm and short (under 150 words), second person, no jargon, no em dashes, no
   bullet lists unless there are steps. Do not include ids like ch_ or sub_ in the reply. Sign off
   "Buildbox Support".
6. note_for_agent: one or two sentences for the human reviewer (what you checked, anything to
   verify). Empty string if nothing."""


def enforce(out: dict, kb_ids: set, account: dict | None) -> dict:
    """Apply the guardrails in code, whatever the model said."""
    cited = [c for c in out.get("cited_articles", []) if c in kb_ids]
    invented = [c for c in out.get("cited_articles", []) if c not in kb_ids]
    reply = (out.get("reply") or "").strip()
    action = dict(out.get("proposed_billing_action") or {"type": "none"})
    if action.get("type") != "none":
        target = action.get("target_id") or ""
        known = json.dumps(account or {})
        action["target_in_account_data"] = bool(re.fullmatch(r"(ch|sub)_[A-Za-z0-9]+", target)) and target in known
    grounded = bool(out.get("can_answer_from_kb")) and bool(cited) and bool(reply)
    return {
        "status": "draft" if grounded else NO_SOURCE,
        "reply": reply if grounded else "",
        "cited_articles": cited,
        "invented_citations": invented,
        "missing_from_kb": out.get("missing_from_kb", "") if not grounded else "",
        "proposed_billing_action": action if grounded else {"type": "none"},
        "note_for_agent": out.get("note_for_agent", ""),
    }


def draft(ticket: dict, account: dict | None = None, use_cache: bool = True) -> dict:
    articles = kb.load()
    prompt = (f"KNOWLEDGE BASE\n\n{kb.as_prompt(articles)}\n\n"
              f"ACCOUNT DATA (read-only lookup from the billing system)\n"
              f"{json.dumps(account, indent=1) if account else 'none looked up'}\n\n"
              f"TICKET {ticket['id']} from {ticket['email']}\nSubject: {ticket['subject']}\n\n{ticket['body']}")
    res = llm.ask(SYSTEM, prompt, SCHEMA, use_cache=use_cache)
    return {**res, "draft": enforce(res["output"], set(articles), account)}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("ticket_id")
    ap.add_argument("--lookup", action="store_true")
    ap.add_argument("--no-cache", action="store_true")
    a = ap.parse_args()
    t = load_tickets()[a.ticket_id]
    account = None
    if a.lookup:
        import billing
        billing.configure()
        account = billing.lookup(t["email"])
    print(json.dumps(draft(t, account, not a.no_cache)["draft"], indent=2))
