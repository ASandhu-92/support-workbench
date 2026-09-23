import json
from types import SimpleNamespace

import pytest

import billing
from conftest import LIVE_KEY, RESTRICTED_LIVE_KEY, TEST_KEY


def entries(path):
    return [json.loads(l) for l in path.read_text().splitlines()] if path.exists() else []


@pytest.mark.parametrize("key", [LIVE_KEY, RESTRICTED_LIVE_KEY, "pk_test_x", "not-a-key", ""])
def test_non_test_keys_are_refused(key, monkeypatch):
    monkeypatch.setenv("STRIPE_TEST_SECRET_KEY", key)
    with pytest.raises(billing.BillingError):
        billing.configure()


def test_test_key_is_accepted(monkeypatch):
    monkeypatch.setenv("STRIPE_TEST_SECRET_KEY", TEST_KEY)
    billing.configure()


def test_live_key_refused_by_cli_before_any_write(monkeypatch, audit_log, no_stripe_writes):
    monkeypatch.setenv("STRIPE_TEST_SECRET_KEY", LIVE_KEY)
    rc = billing.main(["refund", "ch_abc12345", "--reason", "x", "--confirm", "--approved-by", "lead"])
    assert rc == 2
    assert no_stripe_writes == []
    assert entries(audit_log) == []


def test_refund_without_confirm_is_refused_and_logged(audit_log, no_stripe_writes):
    with pytest.raises(billing.BillingError, match="--confirm"):
        billing.refund("ch_abc12345", reason="duplicate charge", approved_by="lead")
    assert no_stripe_writes == []
    [e] = entries(audit_log)
    assert e["executed"] is False and e["action"] == "refund" and "confirm" in e["refused"]


def test_refund_with_confirm_but_no_approver_is_refused(audit_log, no_stripe_writes):
    for who in (None, "", "   "):
        with pytest.raises(billing.BillingError, match="--approved-by"):
            billing.refund("ch_abc12345", reason="x", confirm=True, approved_by=who)
    assert no_stripe_writes == []
    assert all(e["executed"] is False for e in entries(audit_log))


def test_cancel_without_confirm_is_refused(audit_log, no_stripe_writes):
    with pytest.raises(billing.BillingError):
        billing.cancel("sub_abc12345", reason="customer asked")
    assert no_stripe_writes == []


def test_cli_refusal_exit_code(monkeypatch, audit_log, no_stripe_writes):
    monkeypatch.setenv("STRIPE_TEST_SECRET_KEY", TEST_KEY)
    assert billing.main(["refund", "ch_abc12345", "--reason", "x"]) == 2
    assert no_stripe_writes == []


def test_confirmed_refund_records_the_approver(monkeypatch, audit_log):
    import stripe
    seen = {}

    def fake_create(**kw):
        seen.update(kw)
        return SimpleNamespace(id="re_fake0001", amount=1000, status="succeeded")
    monkeypatch.setattr(stripe.Refund, "create", fake_create)
    out = billing.refund("ch_abc12345", reason="duplicate", confirm=True, approved_by="lead")
    assert out["amount_usd"] == 10.0
    assert seen["metadata"]["approved_by"] == "lead"
    [e] = entries(audit_log)
    assert e["executed"] is True and e["approved_by"] == "lead"
