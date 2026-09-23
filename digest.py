"""Voice-of-customer weekly digest: themes, counts, ticket ids, one quote each, a proposed action.

Normally called by run_all.py with the triaged tickets. The model groups and words the themes;
the code computes the counts from the ticket ids, drops unknown ids, and checks each quote is
copied word for word from the ticket it names.
"""
import json

import llm

SCHEMA = {
    "type": "object",
    "properties": {
        "headline": {"type": "string"},
        "themes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "theme": {"type": "string"},
                    "ticket_ids": {"type": "array", "items": {"type": "string"}},
                    "quote_ticket_id": {"type": "string"},
                    "quote": {"type": "string"},
                    "proposed_product_action": {"type": "string"},
                    "owner": {"type": "string", "enum": ["product", "engineering", "billing", "support/KB", "sales"]},
                },
                "required": ["theme", "ticket_ids", "quote_ticket_id", "quote",
                             "proposed_product_action", "owner"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["headline", "themes"],
    "additionalProperties": False,
}

SYSTEM = """You write the weekly voice-of-customer digest for the whole Buildbox company (an AI app
builder). Readers are product managers, engineers and founders with two minutes to spare.

- Group the tickets into 5 to 8 themes by what the customer experienced, not by our internal
  tiers. Every ticket belongs to exactly one theme.
- quote: one short sentence copied character for character from the body of the ticket named in
  quote_ticket_id. Pick the line that shows the customer's feeling or impact best.
- proposed_product_action: one concrete change a team could ship or decide (not "investigate").
- headline: one sentence, the single most important thing this week.
Plain sentences, no em dashes, no marketing words."""


def build(rows: list[dict], use_cache: bool = True) -> dict:
    """rows: [{id, subject, body, tier, topic, action}]"""
    by_id = {r["id"]: r for r in rows}
    prompt = "TICKETS THIS WEEK\n\n" + "\n\n".join(
        f"{r['id']} | tier {r['tier']} | {r['topic']} | outcome {r['action']}\n"
        f"Subject: {r['subject']}\n{r['body']}" for r in rows)
    res = llm.ask(SYSTEM, prompt, SCHEMA, use_cache=use_cache)
    out = res["output"]
    seen = []
    for th in out["themes"]:
        th["ticket_ids"] = [i for i in th["ticket_ids"] if i in by_id]
        th["count"] = len(th["ticket_ids"])
        src = by_id.get(th["quote_ticket_id"], {})
        th["quote_verified"] = bool(th["quote"]) and th["quote"] in (src.get("body", "") + src.get("subject", ""))
        seen += th["ticket_ids"]
    out["themes"].sort(key=lambda t: -t["count"])
    out["unassigned"] = sorted(set(by_id) - set(seen))
    out["assigned_twice"] = sorted({i for i in seen if seen.count(i) > 1})
    return {**res, "digest": out}


def to_markdown(digest: dict, kb_gaps: list[dict], week: str) -> str:
    lines = [f"# Voice of customer, {week}", "", f"**{digest['headline']}**", "",
             "| Theme | Tickets | Count | Owner | Proposed action |", "|---|---|---|---|---|"]
    for th in digest["themes"]:
        lines.append(f"| {th['theme']} | {', '.join(th['ticket_ids'])} | {th['count']} | {th['owner']} | "
                     f"{th['proposed_product_action']} |")
    lines += ["", "## In their words", ""]
    for th in digest["themes"]:
        flag = "" if th["quote_verified"] else " (quote not found word for word in the ticket)"
        lines.append(f"- **{th['theme']}** ({th['quote_ticket_id']}): \"{th['quote']}\"{flag}")
    lines += ["", "## Knowledge base gaps", ""]
    if kb_gaps:
        lines += [f"- {g['id']}: {g['missing']}" for g in kb_gaps]
    else:
        lines.append("- none this week")
    if digest["unassigned"] or digest["assigned_twice"]:
        lines += ["", f"Check: unassigned {digest['unassigned']}, in two themes {digest['assigned_twice']}"]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    # Rebuild the digest from the last run's triage (results/run.json); cached, so usually free.
    import argparse
    from pathlib import Path
    from tickets import load_tickets
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-cache", action="store_true")
    a = ap.parse_args()
    tickets = load_tickets()
    run = json.loads((Path(__file__).resolve().parent / "results" / "run.json").read_text())
    rows = [{**r, "body": tickets[r["id"]]["body"]} for r in run["tickets"] if not r["error"]]
    gaps = [{"id": r["id"], "missing": r["draft"]["missing_from_kb"]} for r in rows
            if r.get("draft") and r["draft"]["status"] != "draft"]
    week = f"{min(t['received'] for t in tickets.values())[:10]} to {max(t['received'] for t in tickets.values())[:10]}"
    print(to_markdown(build(rows, not a.no_cache)["digest"], gaps, week))
