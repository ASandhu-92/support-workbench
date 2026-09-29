"""Write a tier 3 handoff note for engineering, with the evidence from the ticket.

    python escalate.py T-23

The model summarizes; the code checks that every "evidence" line is quoted word for word from the
ticket, so the note cannot put words in the customer's mouth, and flags a holding reply that claims
support saw or checked something (this tool has no access to deploys, logs or projects).
"""
import argparse
import json
import re

import kb
import llm
from tickets import load_tickets

SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "severity": {"type": "string", "enum": ["sev1", "sev2", "sev3"]},
        "customer_impact": {"type": "string"},
        "evidence": {"type": "array", "items": {"type": "string"}},
        "already_tried": {"type": "array", "items": {"type": "string"}},
        "kb_checked": {"type": "array", "items": {"type": "string", "pattern": "^KB-[0-9]{2}$"}},
        "why_not_tier_1_or_2": {"type": "string"},
        "suspected_area": {"type": "string"},
        "questions_for_engineering": {"type": "array", "items": {"type": "string"}},
        "holding_reply_to_customer": {"type": "string"},
    },
    "required": ["title", "severity", "customer_impact", "evidence", "already_tried", "kb_checked",
                 "why_not_tier_1_or_2", "suspected_area", "questions_for_engineering",
                 "holding_reply_to_customer"],
    "additionalProperties": False,
}

# Phrases that claim support looked at the customer's systems. The tool never has.
SEEN_CLAIM = re.compile(r"\bwe(?:'ve| have)? (?:can )?(?:see|seen|checked|looked|confirmed|noticed)\b", re.I)

SYSTEM = """You write handoff notes from Buildbox support to engineering. Buildbox is an AI app
builder. An engineer should be able to start work from the note without reading the ticket.

- severity, by impact:
  sev1 = data loss, money taken wrongly at scale, or an outage that may affect many customers.
    One report counts if it points past this customer (several projects stuck at once, a status
    page that says all is well while it fails); keep sev1 until engineering rules it out.
  sev2 = one customer blocked with no workaround, and nothing points to it being wider.
  sev3 = degraded, a workaround exists.
  Unclear wording alone is not a reason to raise severity.
- evidence: short exact quotes copied character for character from the ticket (error messages, ids,
  counts, times). Do not paraphrase inside evidence.
- already_tried: what the customer says they already did.
- kb_checked: the KB articles that cover this area, and in why_not_tier_1_or_2 say in one sentence
  why the documented answer does not solve it.
- questions_for_engineering: at most three, specific.
- holding_reply_to_customer: under 80 words, honest, no promised fix time, no em dashes, signed
  "Buildbox Support". Support cannot see the customer's deploys, logs or projects: say "you've
  told us", never "we can see" or "we checked".
Plain sentences. No em dashes."""


def escalate(ticket: dict, classification: dict, use_cache: bool = True) -> dict:
    prompt = (f"KNOWLEDGE BASE\n\n{kb.as_prompt(kb.load())}\n\n"
              f"TRIAGE: tier {classification['tier']}, topic {classification['topic']}, "
              f"urgency {classification['urgency']}\n\n"
              f"TICKET {ticket['id']} from {ticket['email']} received {ticket['received']}\n"
              f"Subject: {ticket['subject']}\n\n{ticket['body']}")
    res = llm.ask(SYSTEM, prompt, SCHEMA, use_cache=use_cache)
    note = res["output"]
    note["evidence_verified"] = [q for q in note["evidence"] if q in ticket["body"] or q in ticket["subject"]]
    note["evidence_unverified"] = [q for q in note["evidence"] if q not in note["evidence_verified"]]
    note["holding_reply_flags"] = [m.group(0) for m in SEEN_CLAIM.finditer(note["holding_reply_to_customer"])]
    return {**res, "note": note}


def to_markdown(ticket: dict, classification: dict, note: dict) -> str:
    def bullets(items):
        return "\n".join(f"- {x}" for x in items) or "- none"
    unverified = ""
    if note["evidence_unverified"]:
        unverified = ("\n\nNot found word for word in the ticket (check before relying on it):\n"
                      + bullets(note["evidence_unverified"]))
    flags = ""
    if note.get("holding_reply_flags"):
        flags = (" (rewrite before sending: claims support saw something: "
                 + ", ".join(f'"{f}"' for f in note["holding_reply_flags"]) + ")")
    return f"""# {ticket['id']}: {note['title']}

| | |
|---|---|
| Severity | {note['severity']} |
| Customer | {ticket['email']} |
| Received | {ticket['received']} |
| Triage | tier {classification['tier']}, {classification['topic']}, urgency {classification['urgency']} |
| Suspected area | {note['suspected_area']} |

**Customer impact.** {note['customer_impact']}

**Evidence (quoted from the ticket)**
{bullets(note['evidence_verified'])}{unverified}

**Already tried by the customer**
{bullets(note['already_tried'])}

**KB checked:** {', '.join(note['kb_checked']) or 'none'}. {note['why_not_tier_1_or_2']}

**Questions for engineering**
{bullets(note['questions_for_engineering'])}

**Holding reply sent to the customer (draft)**{flags}

> {note['holding_reply_to_customer'].replace(chr(10), chr(10) + '> ')}
"""


if __name__ == "__main__":
    import classify
    ap = argparse.ArgumentParser()
    ap.add_argument("ticket_id")
    ap.add_argument("--no-cache", action="store_true")
    a = ap.parse_args()
    t = load_tickets()[a.ticket_id]
    c = classify.classify(t, not a.no_cache)["output"]
    print(to_markdown(t, c, escalate(t, c, not a.no_cache)["note"]))
