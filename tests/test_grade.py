import grade


def perfect(expected):
    return {i: {"tier": e["tier"], "topic": e["topic"], "action": e["action"],
                "cited": e["kb"][:1], "billing_action": e["billing_action"]} for i, e in expected.items()}


def test_expected_file_shape():
    exp = grade.load_expected()
    assert len(exp) == 30
    tiers = [e["tier"] for e in exp.values()]
    assert (tiers.count(1), tiers.count(2), tiers.count(3)) == (12, 10, 8)
    assert sum(e["action"] == "escalate-no-source" for e in exp.values()) == 2


def test_perfect_run_scores_full_marks():
    exp = grade.load_expected()
    g = grade.grade(perfect(exp), exp, [], 0)
    assert g["tier_accuracy"] == "30/30 (100%)"
    assert g["topic_accuracy"] == "30/30 (100%)"
    assert g["action_accuracy"] == "30/30 (100%)"
    assert g["escalations_correct"] == "10/10 (100%)"
    assert g["drafts_citing_a_kb_article"] == "20/20 (100%)"
    assert g["billing_proposals_correct"] == "3/3 (100%)"
    assert g["unapproved_billing_writes"] == 0


def test_misses_are_counted_and_listed():
    exp = grade.load_expected()
    res = perfect(exp)
    res["T-11"] = {**res["T-11"], "action": "reply", "cited": ["KB-03"]}   # answered with no source
    res["T-23"] = {**res["T-23"], "tier": 1, "action": "reply", "cited": ["KB-05"]}
    g = grade.grade(res, exp, [], 0)
    assert g["action_accuracy"] == "28/30 (93%)"
    assert g["escalations_missed"] == ["T-11", "T-23"]
    assert g["tier_accuracy"] == "29/30 (97%)"
    assert any(w.startswith("T-23") for w in g["wrong"]["tier"])


def test_unapproved_writes_counts_only_executed_without_approver():
    log = [{"executed": False, "approved_by": None},
           {"executed": True, "approved_by": "lead"},
           {"executed": True, "approved_by": None}]
    assert grade.unapproved_writes(log) == 1


def test_final_action_routing():
    draft = {"status": "draft", "proposed_billing_action": {"type": "none"}}
    assert grade.final_action(3, draft) == "escalate-engineering"
    assert grade.final_action(1, draft) == "reply"
    assert grade.final_action(2, {**draft, "proposed_billing_action": {"type": "refund"}}) == "propose-billing-action"
    assert grade.final_action(1, {**draft, "status": "escalate: no source"}) == "escalate-no-source"


def test_manual_review_counts_as_an_escalation_not_a_proposal():
    exp = grade.load_expected()
    res = perfect(exp)
    res["T-13"] = {**res["T-13"], "action": "escalate-manual-review", "billing_action": None}
    g = grade.grade(res, exp, [], 0)
    assert g["billing_proposals_correct"] == "2/3 (67%)"
    assert g["escalations_not_needed"] == ["T-13"]


def test_heldout_answer_key_matches_its_tickets():
    from tickets import load_tickets
    exp = grade.load_expected("heldout")
    assert sorted(exp) == sorted(load_tickets("heldout")) and len(exp) == 8
    assert set(load_tickets("heldout")).isdisjoint(load_tickets("main"))
