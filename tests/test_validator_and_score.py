import pytest

from sopflow.baseline import extract
from sopflow.eval.score import aggregate, counts
from sopflow.spec import Edge, Step, WorkflowSpec, all_ids, load_gold, load_sop, split
from sopflow.validator import validate


def spec(steps, edges):
    return WorkflowSpec(steps=[Step(id=i, lines=l, action="a", role="r", handoff_to=h, executor=x) for i, l, h, x in steps],
                        edges=[Edge(**{"from": a, "to": b}) for a, b in edges])


@pytest.mark.parametrize("sop_id", all_ids())
def test_every_gold_spec_is_valid(sop_id):
    assert validate(load_gold(sop_id), len(load_sop(sop_id).lines)) == []


def test_splits_are_disjoint_and_complete():
    d, t, o = (set(split(k)) for k in ("dev", "test", "test_ood"))
    assert not (d & t or d & o or t & o) and d | t | o == set(all_ids())


def test_validator_catches_structural_errors():
    bad = spec([("s1", [1], None, "agent"), ("s1", [99], None, None), ("s3", [2], None, "human")],
               [("s1", "s3"), ("s3", "s1"), ("s3", "s9")])
    errs = " ".join(validate(bad, 5))
    for needle in ("Duplicate step ids", "do not exist", "cycle", "unknown step s9", "executor"):
        assert needle in errs


def test_gold_scores_perfectly_against_itself():
    g = load_gold("hipaa_breach_notification")
    agg = aggregate([counts(g, g)])
    assert agg["step_f1"] == agg["edge_f1"] == agg["handoff_f1"] == agg["executor_acc"] == 1.0


def test_line_matching_and_edge_mapping():
    gold = spec([("g1", [1], None, "human"), ("g2", [2, 3], "x", "agent")], [("g1", "g2")])
    pred = spec([("a", [1], None, "human"), ("b", [3], "y", "human"), ("c", [5], None, "agent")], [("a", "b"), ("b", "c")])
    c = counts(pred, gold)   # b matches g2 (Jaccard 0.5), c is a false positive
    assert (c["step_tp"], c["step_fp"], c["step_fn"]) == (2, 1, 0)
    assert (c["edge_tp"], c["edge_fp"], c["edge_fn"]) == (1, 1, 0)
    assert (c["handoff_tp"], c["exec_correct"], c["exec_n"]) == (1, 1, 2)


def test_baseline_produces_valid_or_empty_specs():
    # the frozen rule baseline finds no steps in a few SOPs (no modal verbs it knows); that is scored, not hidden
    for i in all_ids():
        sop = load_sop(i)
        errs = validate(extract(sop), len(sop.lines))
        assert errs in ([], ["The workflow has no steps."])
