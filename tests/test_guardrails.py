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


def test_billing_target_must_exist_in_account_data():
    account = {"charges": [{"id": "ch_realone123"}]}
    ok = draft.enforce(model_out(proposed_billing_action={"type": "refund", "target_id": "ch_realone123",
                                                          "amount_usd": 10, "why": "dup"}), KB, account)
    bad = draft.enforce(model_out(proposed_billing_action={"type": "refund", "target_id": "ch_madeup999",
                                                           "amount_usd": 10, "why": "dup"}), KB, account)
    assert ok["proposed_billing_action"]["target_in_account_data"] is True
    assert bad["proposed_billing_action"]["target_in_account_data"] is False


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
