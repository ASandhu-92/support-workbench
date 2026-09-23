"""Classify a ticket: tier, topic, urgency.

    python classify.py T-05            one ticket from data/tickets.json
    python classify.py T-05 --no-cache
"""
import argparse
import json

import llm
from tickets import load_tickets

TOPICS = [
    "editor-and-generation", "credits-and-usage", "plans-and-pricing", "deploys",
    "custom-domains", "github-sync", "environment-variables", "team-and-account",
    "data-and-backups", "security-and-compliance", "billing-charges", "billing-refunds",
    "billing-invoices", "billing-payment-failed", "billing-plan-changes",
]

SCHEMA = {
    "type": "object",
    "properties": {
        "tier": {"type": "integer", "enum": [1, 2, 3]},
        "topic": {"type": "string", "enum": TOPICS},
        "urgency": {"type": "string", "enum": ["low", "normal", "high"]},
        "reason": {"type": "string"},
    },
    "required": ["tier", "topic", "urgency", "reason"],
    "additionalProperties": False,
}

SYSTEM = """You triage support tickets for Buildbox, an AI app builder (prompt-to-app, deploys,
custom domains, GitHub sync, credits and plans).

Tiers:
1 = a question about how the product works that documentation can answer (how-to, plans, limits,
    what a message means when the product is behaving as documented).
2 = billing or account administration that needs someone to look at this customer's account:
    charges, refunds, invoices, failed payments, plan changes or cancellation, email change,
    workspace ownership.
3 = the product is not behaving as documented and an engineer has to investigate: outages, stuck
    jobs, data loss, bugs, anything where the documented fix was already tried.

Urgency: high if the customer is losing money or data now, or a stated deadline is within about a
day; low for general questions with no impact; otherwise normal.

Pick the single topic that best describes what the ticket is about. Keep "reason" to one plain
sentence. Do not use em dashes."""


def classify(ticket: dict, use_cache: bool = True) -> dict:
    prompt = f"Ticket {ticket['id']}\nSubject: {ticket['subject']}\n\n{ticket['body']}"
    return llm.ask(SYSTEM, prompt, SCHEMA, use_cache=use_cache)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("ticket_id")
    ap.add_argument("--no-cache", action="store_true")
    a = ap.parse_args()
    print(json.dumps(classify(load_tickets()[a.ticket_id], not a.no_cache), indent=2))
