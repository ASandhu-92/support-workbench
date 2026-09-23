import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Fake keys are assembled at runtime so the repo never contains a key-shaped literal.
TEST_KEY = "_".join(["sk", "test", "unit0never0calls0the0network"])
LIVE_KEY = "_".join(["sk", "live", "unit0never0calls0the0network"])
RESTRICTED_LIVE_KEY = "_".join(["rk", "live", "unit0never0calls0the0network"])


@pytest.fixture()
def audit_log(tmp_path, monkeypatch):
    import billing
    path = tmp_path / "billing_actions.jsonl"
    monkeypatch.setattr(billing, "AUDIT_LOG", path)
    return path


@pytest.fixture()
def no_stripe_writes(monkeypatch):
    """Make any Stripe write blow up, so a test fails loudly if the guard lets one through."""
    import stripe
    calls = []

    def boom(*a, **k):
        calls.append((a, k))
        raise AssertionError("a Stripe write was attempted")
    monkeypatch.setattr(stripe.Refund, "create", boom)
    monkeypatch.setattr(stripe.Subscription, "modify", boom)
    return calls
