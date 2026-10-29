import json

from sopflow.compiler import FakeBackend, compile_sop
from sopflow.spec import load_sop


def step(i, line, ex="agent"):
    return {"id": i, "lines": [line], "action": "x", "role": "r", "handoff_to": None, "executor": ex, "executor_reason": "r"}


def test_repair_loop_feeds_validator_errors_back():
    sop = load_sop("cdc_handwashing")
    broken = json.dumps({"steps": [step("s1", 2), step("s2", 40)],
                         "edges": [{"from": "s1", "to": "s2", "condition": None}, {"from": "s2", "to": "s1", "condition": None}]})
    fixed = json.dumps({"steps": [step("s1", 2), step("s2", 3)], "edges": [{"from": "s1", "to": "s2", "condition": None}]})
    fb = FakeBackend([broken, fixed])
    r = compile_sop(sop, fb, "v2")
    assert not r.valid_first and r.valid_final and len(r.attempts) == 2
    repair_msg = fb.calls[1][-1]["content"]
    assert "cycle" in repair_msg and "do not exist" in repair_msg


def test_unparseable_output_is_an_error_not_a_crash():
    r = compile_sop(load_sop("cdc_handwashing"), FakeBackend(["not json", "{}", "[]"]), "v1", max_repairs=2)
    assert r.spec is None and not r.valid_final and len(r.attempts) == 3
