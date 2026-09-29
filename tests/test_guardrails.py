import json
import subprocess

import pytest

import draft
import llm

KB = {"KB-02", "KB-13"}


def model_out(**over):
    base = {"can_answer_from_kb": True, "cited_articles": ["KB-13"], "reply": "Hi, sorted.",
            "missing_from_kb": "", "note_for_agent": "",
            "proposed_billing_action": {"type": "none", "target_id": "", "amount_usd": 0, "why": ""}}
    return {**base, **over}


def test_reply_without_citation_becomes_no_source():
    d = draft.enforce(model_out(cited_articles=[]), KB, None)
    assert d["status"] == draft.NO_SOURCE and d["reply"] == ""


def test_invented_article_does_not_count_as_a_source():
    d = draft.enforce(model_out(cited_articles=["KB-99"]), KB, None)
    assert d["status"] == draft.NO_SOURCE
    assert d["invented_citations"] == ["KB-99"]


def test_model_saying_it_cannot_answer_wins():
    d = draft.enforce(model_out(can_answer_from_kb=False), KB, None)
    assert d["status"] == draft.NO_SOURCE


ACCOUNT = {"customer": {"id": "cus_dana0001"},
           "charges": [{"id": "ch_realone123"}], "subscriptions": [{"id": "sub_realone123"}],
           "invoices": [{"id": "in_realone123", "lines": [{"description": "ch_otherone99 mentioned in text"}]}]}


def proposal(kind, target, conditions=()):
    return model_out(proposed_billing_action={"type": kind, "target_id": target, "amount_usd": 10,
                                              "why": "dup", "unverified_conditions": list(conditions)})


def test_refund_on_the_customers_charge_is_ready_for_approval():
    d = draft.enforce(proposal("refund", "ch_realone123"), KB, ACCOUNT)
    pa = d["proposed_billing_action"]
    assert d["status"] == "draft" and pa["blocked"] is None and pa["ready_for_approval"] is True


@pytest.mark.parametrize("kind,target", [
    ("refund", "ch_madeup999"),       # invented
    ("refund", "sub_realone123"),     # real id, wrong type for a refund
    ("cancel", "ch_realone123"),      # real id, wrong type for a cancel
    ("refund", "ch_otherone99"),      # appears in the account data, but only inside free text
    ("refund", "ch_realone12"),       # prefix of a real id
    ("refund", ""),
])
def test_proposal_on_a_target_not_in_the_right_list_goes_to_manual_review(kind, target):
    d = draft.enforce(proposal(kind, target), KB, ACCOUNT)
    assert d["status"] == draft.MANUAL_REVIEW
    assert d["proposed_billing_action"]["ready_for_approval"] is False
    assert d["proposed_billing_action"]["blocked"]
    import grade
    assert grade.final_action(2, d) == "escalate-manual-review"


def test_proposal_without_an_account_lookup_goes_to_manual_review():
    d = draft.enforce(proposal("refund", "ch_realone123"), KB, None)
    assert d["status"] == draft.MANUAL_REVIEW and "no customer account" in d["manual_review_reason"]


def test_unverified_policy_condition_keeps_the_proposal_but_not_ready():
    d = draft.enforce(proposal("refund", "ch_realone123", ["credits used since the charge", " "]), KB, ACCOUNT)
    pa = d["proposed_billing_action"]
    assert d["status"] == "draft" and pa["ready_for_approval"] is False
    assert pa["unverified_conditions"] == ["credits used since the charge"]
    import grade
    assert grade.final_action(2, d) == "propose-billing-action"


def fake_run(stdout, rc=0):
    def run(*a, **k):
        return subprocess.CompletedProcess(a, rc, stdout=stdout, stderr="")
    return run


def test_llm_error_result_raises(monkeypatch, tmp_path):
    monkeypatch.setattr(llm, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(subprocess, "run", fake_run(json.dumps({"is_error": True, "subtype": "error"}), 1))
    with pytest.raises(llm.LLMError):
        llm.ask("s", "p", {"type": "object"})


def test_llm_non_json_raises(monkeypatch, tmp_path):
    monkeypatch.setattr(llm, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(subprocess, "run", fake_run("not json", 1))
    with pytest.raises(llm.LLMError):
        llm.ask("s", "p", {"type": "object"})


def test_llm_caches_and_strips_em_dashes(monkeypatch, tmp_path):
    monkeypatch.setattr(llm, "CACHE_DIR", tmp_path)
    body = {"is_error": False, "structured_output": {"reply": "a" + chr(0x2014) + "b"}, "total_cost_usd": 0.01,
            "duration_ms": 5, "modelUsage": {"claude-sonnet-5": {}}}
    monkeypatch.setattr(subprocess, "run", fake_run(json.dumps(body)))
    first = llm.ask("s", "p", {"type": "object"})
    assert first["output"]["reply"] == "a - b" and first["cached"] is False
    monkeypatch.setattr(subprocess, "run", fake_run("should not be called", 1))
    again = llm.ask("s", "p", {"type": "object"})
    assert again["cached"] is True and again["cost_usd"] == 0.01


def test_command_has_no_tools_and_no_settings():
    cmd = llm.command("sys", "prompt", {"type": "object"})
    for flag in ("--tools", "--no-session-persistence", "--setting-sources", "--strict-mcp-config",
                 "--disable-slash-commands", "--json-schema"):
        assert flag in cmd
    assert cmd[cmd.index("--tools") + 1] == ""


def test_holding_reply_that_claims_we_saw_something_is_flagged():
    import escalate
    for text, n in [("We can see your deploys have been queued.", 1), ("We've checked your logs.", 1),
                    ("You've told us your deploys are queued. We have passed this on.", 0)]:
        assert len(escalate.SEEN_CLAIM.findall(text)) == n, text


def test_digest_flags_answered_how_to_filed_as_a_defect(monkeypatch):
    import digest
    rows = [{"id": "T-04", "subject": "s", "body": "where do I put my key", "tier": 1, "topic": "t",
             "action": "reply"},
            {"id": "T-29", "subject": "s", "body": "env var missing in prod", "tier": 3, "topic": "t",
             "action": "escalate-engineering"}]
    out = {"headline": "h", "themes": [{"theme": "Deploys fail", "kind": "product defect",
                                        "ticket_ids": ["T-04", "T-29", "T-99"], "quote_ticket_id": "T-29",
                                        "quote": "env var missing in prod", "proposed_product_action": "x",
                                        "owner": "engineering"}]}
    monkeypatch.setattr(llm, "ask", lambda *a, **k: {"output": out})
    d = digest.build(rows)["digest"]
    th = d["themes"][0]
    assert th["ticket_ids"] == ["T-04", "T-29"] and th["count"] == 2 and th["quote_verified"]
    assert th["answered_by_kb"] == ["T-04"]
    assert "filed as a defect but answered from the help center" in digest.to_markdown(d, [], "w")
