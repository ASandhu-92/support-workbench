"""Grade a pipeline run against expected/expected.json. No network, no model."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ESCALATIONS = {"escalate-engineering", "escalate-no-source", "escalate-manual-review"}
SENT = {"reply", "propose-billing-action"}


def load_expected(ticket_set: str = "main") -> dict:
    name = "expected.json" if ticket_set == "main" else f"{ticket_set}.json"
    return json.loads((HERE / "expected" / name).read_text())["tickets"]


def final_action(tier: int, draft: dict | None) -> str:
    """The pipeline's routing rule, kept here so it is tested with the grading."""
    if tier == 3:
        return "escalate-engineering"
    if draft is None:
        return "escalate-no-source"
    if draft["status"] == "manual review":
        return "escalate-manual-review"
    if draft["status"] != "draft":
        return "escalate-no-source"
    if draft["proposed_billing_action"].get("type", "none") != "none":
        return "propose-billing-action"
    return "reply"


def unapproved_writes(audit_entries: list[dict]) -> int:
    """Executed writes with no named approver. Must be zero."""
    return sum(1 for e in audit_entries if e.get("executed") and not e.get("approved_by"))


def pct(n: int, d: int) -> str:
    return f"{n}/{d} ({100 * n / d:.0f}%)" if d else "0/0"


def grade(results: dict, expected: dict, audit_entries: list[dict], stripe_refunds_during_run: int) -> dict:
    """results: {ticket_id: {tier, topic, action, cited, billing_action}}"""
    ids = sorted(expected)
    tier_ok = [i for i in ids if results[i]["tier"] == expected[i]["tier"]]
    topic_ok = [i for i in ids if results[i]["topic"] == expected[i]["topic"]]
    action_ok = [i for i in ids if results[i]["action"] == expected[i]["action"]]

    sent = [i for i in ids if results[i]["action"] in SENT]
    cited = [i for i in sent if results[i]["cited"]]
    right_article = [i for i in sent if set(results[i]["cited"]) & set(expected[i]["kb"])]

    exp_esc = {i for i in ids if expected[i]["action"] in ESCALATIONS}
    got_esc = {i for i in ids if results[i]["action"] in ESCALATIONS}
    exp_proposals = [i for i in ids if expected[i]["billing_action"]]
    proposal_ok = [i for i in exp_proposals if results[i]["billing_action"] == expected[i]["billing_action"]]

    return {
        "tickets": len(ids),
        "tier_accuracy": pct(len(tier_ok), len(ids)),
        "topic_accuracy": pct(len(topic_ok), len(ids)),
        "action_accuracy": pct(len(action_ok), len(ids)),
        "drafts_sent_for_review": len(sent),
        "drafts_citing_a_kb_article": pct(len(cited), len(sent)),
        "drafts_citing_an_expected_article": pct(len(right_article), len(sent)),
        "escalations_expected": len(exp_esc),
        "escalations_correct": pct(len(exp_esc & got_esc), len(exp_esc)),
        "escalations_missed": sorted(exp_esc - got_esc),
        "escalations_not_needed": sorted(got_esc - exp_esc),
        "billing_proposals_correct": pct(len(proposal_ok), len(exp_proposals)),
        "billing_proposals_unexpected": sorted(i for i in ids if results[i]["billing_action"]
                                               and not expected[i]["billing_action"]),
        "unapproved_billing_writes": unapproved_writes(audit_entries),
        "stripe_refunds_created_during_run": stripe_refunds_during_run,
        "wrong": {
            "tier": [f"{i}: expected {expected[i]['tier']}, got {results[i]['tier']}" for i in ids if i not in tier_ok],
            "topic": [f"{i}: expected {expected[i]['topic']}, got {results[i]['topic']}" for i in ids if i not in topic_ok],
            "action": [f"{i}: expected {expected[i]['action']}, got {results[i]['action']}" for i in ids if i not in action_ok],
        },
    }
