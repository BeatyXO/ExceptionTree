from pathlib import Path

CONTRACT_SOURCE = (Path(__file__).parents[1] / "contracts" / "exceptiontree.py").read_text(encoding="utf-8")

ALLOW = 1
DENY = 2
NO_DECISION = 3


def deploy(direct_vm, direct_deploy):
    direct_vm.check_pickling = True
    return direct_deploy("contracts/exceptiontree.py")


def assessments(*statuses):
    mapping = []
    for index, status in enumerate(statuses, start=1):
        mapping.append({"rule_id": index, "status": status, "reason_code": "TEST"})
    return {"assessments": mapping}


def build_refund_rules(c):
    rs = c.create_ruleset(
        "Refund Policy",
        "Resolve whether a supplied purchase fact pattern is refundable under the sealed rules.",
        NO_DECISION,
    )
    root = c.add_root_rule(rs, "Within 30 days", "The purchase was made no more than 30 days ago.", ALLOW, 10)
    perish = c.add_exception(root, "Perishable exclusion", "The purchased item is perishable.", DENY, 10)
    defect = c.add_exception(perish, "Defect override", "The perishable item is materially defective.", ALLOW, 10)
    timely = c.add_exception(defect, "Late report exclusion", "The defect was reported more than 48 hours after discovery.", DENY, 10)
    dh = c.seal_ruleset(rs)
    return rs, root, perish, defect, timely, dh


def test_contract_shape_is_standalone_reusable_primitive():
    assert "class ExceptionTree(gl.Contract)" in CONTRACT_SOURCE
    assert "run_nondet_unsafe" in CONTRACT_SOURCE
    assert "deterministic_resolve" in CONTRACT_SOURCE
    assert "seal_ruleset" in CONTRACT_SOURCE
    assert "is_outcome" in CONTRACT_SOURCE
    assert "frontend" not in CONTRACT_SOURCE.lower()


def test_root_rule_resolves_allow(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    rs, _, _, _, _, dh = build_refund_rules(c)
    case = c.submit_case(rs, "Bought 10 days ago. Item is non-perishable and works correctly.", dh)
    direct_vm.mock_llm(r"EXCEPTIONTREE / CLASSIFY APPLICABILITY", assessments("APPLIES", "DOES_NOT_APPLY", "DOES_NOT_APPLY", "DOES_NOT_APPLY"))
    assert int(c.resolve_case(case)) == 1
    item = c.get_case(case)
    assert item["outcome_name"] == "ALLOW"
    assert item["winning_rule_id"] == 1
    assert len(item["resolution_hash"]) == 64


def test_exception_overrides_general_rule(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    rs, _, _, _, _, dh = build_refund_rules(c)
    case = c.submit_case(rs, "Bought 5 days ago. Item is perishable and not defective.", dh)
    direct_vm.mock_llm(r"EXCEPTIONTREE / CLASSIFY APPLICABILITY", assessments("APPLIES", "APPLIES", "DOES_NOT_APPLY", "DOES_NOT_APPLY"))
    assert int(c.resolve_case(case)) == 2
    assert c.get_case(case)["winning_rule_id"] == 2


def test_nested_exception_can_reopen_allow(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    rs, _, _, _, _, dh = build_refund_rules(c)
    case = c.submit_case(rs, "Bought 5 days ago. Item is perishable and materially defective. Reported immediately.", dh)
    direct_vm.mock_llm(r"EXCEPTIONTREE / CLASSIFY APPLICABILITY", assessments("APPLIES", "APPLIES", "APPLIES", "DOES_NOT_APPLY"))
    assert int(c.resolve_case(case)) == 1
    assert c.get_case(case)["winning_rule_id"] == 3


def test_deeper_late_report_exception_denies(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    rs, _, _, _, _, dh = build_refund_rules(c)
    case = c.submit_case(rs, "Bought 5 days ago. Perishable and defective. Defect reported 72 hours after discovery.", dh)
    direct_vm.mock_llm(r"EXCEPTIONTREE / CLASSIFY APPLICABILITY", assessments("APPLIES", "APPLIES", "APPLIES", "APPLIES"))
    assert int(c.resolve_case(case)) == 2
    assert c.get_case(case)["winning_rule_id"] == 4


def test_child_cannot_apply_when_parent_path_does_not_apply(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    rs, _, _, _, _, dh = build_refund_rules(c)
    case = c.submit_case(rs, "Bought 5 days ago. Non-perishable item. Narrative happens to mention a defect.", dh)
    direct_vm.mock_llm(r"EXCEPTIONTREE / CLASSIFY APPLICABILITY", assessments("APPLIES", "DOES_NOT_APPLY", "APPLIES", "DOES_NOT_APPLY"))
    assert int(c.resolve_case(case)) == 1
    assert c.get_case(case)["winning_rule_id"] == 1


def test_ambiguity_that_could_overturn_winner_fails_ambiguous(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    rs, _, _, _, _, dh = build_refund_rules(c)
    case = c.submit_case(rs, "Bought 5 days ago. It is unclear whether the product counts as perishable.", dh)
    direct_vm.mock_llm(r"EXCEPTIONTREE / CLASSIFY APPLICABILITY", assessments("APPLIES", "AMBIGUOUS", "DOES_NOT_APPLY", "DOES_NOT_APPLY"))
    assert int(c.resolve_case(case)) == 5
    item = c.get_case(case)
    assert item["outcome_name"] == "AMBIGUOUS"
    assert 2 in item["ambiguous_rule_ids"]


def test_same_effect_ambiguity_does_not_change_stable_outcome(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    rs = c.create_ruleset("Stable allow", "A narrow same-effect exception example.", NO_DECISION)
    root = c.add_root_rule(rs, "Base allow", "Base condition applies.", ALLOW, 10)
    c.add_exception(root, "Narrow allow", "A narrower optional fact may apply.", ALLOW, 10)
    dh = c.seal_ruleset(rs)
    case = c.submit_case(rs, "Base condition clearly applies; narrower fact is uncertain.", dh)
    direct_vm.mock_llm(r"EXCEPTIONTREE / CLASSIFY APPLICABILITY", assessments("APPLIES", "AMBIGUOUS"))
    assert int(c.resolve_case(case)) == 1


def test_equal_rank_opposite_root_rules_conflict(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    rs = c.create_ruleset("Conflict", "Demonstrate explicit contradiction at equal precedence.", NO_DECISION)
    c.add_root_rule(rs, "Allow clause", "Condition A applies.", ALLOW, 10)
    c.add_root_rule(rs, "Deny clause", "Condition B applies.", DENY, 10)
    dh = c.seal_ruleset(rs)
    case = c.submit_case(rs, "Both A and B are established.", dh)
    direct_vm.mock_llm(r"EXCEPTIONTREE / CLASSIFY APPLICABILITY", assessments("APPLIES", "APPLIES"))
    assert int(c.resolve_case(case)) == 4
    assert c.get_case(case)["outcome_name"] == "CONFLICT"


def test_higher_priority_breaks_same_depth_overlap(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    rs = c.create_ruleset("Priority", "Demonstrate deterministic sibling/root priority.", NO_DECISION)
    c.add_root_rule(rs, "Low allow", "Condition A applies.", ALLOW, 10)
    c.add_root_rule(rs, "High deny", "Condition B applies.", DENY, 20)
    dh = c.seal_ruleset(rs)
    case = c.submit_case(rs, "Both A and B are established.", dh)
    direct_vm.mock_llm(r"EXCEPTIONTREE / CLASSIFY APPLICABILITY", assessments("APPLIES", "APPLIES"))
    assert int(c.resolve_case(case)) == 2
    assert c.get_case(case)["winning_rule_id"] == 2


def test_malformed_model_output_canonicalizes_to_fail_closed_ambiguity(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    rs = c.create_ruleset("Malformed", "Malformed semantic output must not become a decisive allow.", DENY)
    c.add_root_rule(rs, "Potential allow", "Special condition applies.", ALLOW, 10)
    dh = c.seal_ruleset(rs)
    case = c.submit_case(rs, "Special condition might apply.", dh)
    direct_vm.mock_llm(r"EXCEPTIONTREE / CLASSIFY APPLICABILITY", {"wrong": "shape"})
    assert int(c.resolve_case(case)) == 5


def test_validator_rejects_forged_applicability_vector(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    rs = c.create_ruleset("Forgery", "Validators must independently classify the same clauses.", DENY)
    c.add_root_rule(rs, "Allow", "Fact X applies.", ALLOW, 10)
    dh = c.seal_ruleset(rs)
    case = c.submit_case(rs, "Fact X is clearly true.", dh)
    direct_vm.mock_llm(r"EXCEPTIONTREE / CLASSIFY APPLICABILITY", assessments("APPLIES"))
    c.resolve_case(case)
    direct_vm.clear_mocks()
    direct_vm.mock_llm(r"EXCEPTIONTREE / CLASSIFY APPLICABILITY", assessments("DOES_NOT_APPLY"))
    assert direct_vm.run_validator() is False


def test_validator_accepts_independent_same_material_classification(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    rs = c.create_ruleset("Agreement", "Validators independently agree on applicability.", DENY)
    c.add_root_rule(rs, "Allow", "Fact X applies.", ALLOW, 10)
    dh = c.seal_ruleset(rs)
    case = c.submit_case(rs, "Fact X is clearly true.", dh)
    direct_vm.mock_llm(r"EXCEPTIONTREE / CLASSIFY APPLICABILITY", assessments("APPLIES"))
    c.resolve_case(case)
    direct_vm.clear_mocks()
    direct_vm.mock_llm(r"EXCEPTIONTREE / CLASSIFY APPLICABILITY", assessments("APPLIES"))
    assert direct_vm.run_validator() is True


def test_sealed_ruleset_rejects_mutation(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    rs = c.create_ruleset("Seal", "Sealed definitions are immutable.", DENY)
    c.add_root_rule(rs, "R", "Condition applies.", ALLOW, 10)
    c.seal_ruleset(rs)
    with direct_vm.expect_revert("ruleset is sealed"):
        c.add_root_rule(rs, "Late", "Late mutation.", DENY, 99)


def test_definition_hash_must_be_pinned_when_submitting_case(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    rs = c.create_ruleset("Pin", "Consumers pin the sealed rule definition.", DENY)
    c.add_root_rule(rs, "R", "Condition applies.", ALLOW, 10)
    c.seal_ruleset(rs)
    with direct_vm.expect_revert("definition hash mismatch"):
        c.submit_case(rs, "Condition applies.", "0" * 64)


def test_is_outcome_rejects_wrong_case_or_definition_hash(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    rs = c.create_ruleset("Read", "Typed consumers can pin both definition and case.", DENY)
    c.add_root_rule(rs, "R", "Condition applies.", ALLOW, 10)
    dh = c.seal_ruleset(rs)
    case = c.submit_case(rs, "Condition applies.", dh)
    direct_vm.mock_llm(r"EXCEPTIONTREE / CLASSIFY APPLICABILITY", assessments("APPLIES"))
    c.resolve_case(case)
    item = c.get_case(case)
    assert c.is_outcome(case, dh, item["case_hash"], 1) is True
    assert c.is_outcome(case, "0" * 64, item["case_hash"], 1) is False
    assert c.is_outcome(case, dh, "0" * 64, 1) is False


def test_resolved_case_cannot_be_re_adjudicated(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    rs = c.create_ruleset("Final", "Resolution is single-shot and immutable.", DENY)
    c.add_root_rule(rs, "R", "Condition applies.", ALLOW, 10)
    dh = c.seal_ruleset(rs)
    case = c.submit_case(rs, "Condition applies.", dh)
    direct_vm.mock_llm(r"EXCEPTIONTREE / CLASSIFY APPLICABILITY", assessments("APPLIES"))
    c.resolve_case(case)
    with direct_vm.expect_revert("case already resolved"):
        c.resolve_case(case)
