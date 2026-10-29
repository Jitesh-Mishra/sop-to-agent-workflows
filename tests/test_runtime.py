import multiprocessing as mp

import pytest

from sopflow.eval.crash_resume import run_case
from sopflow.runtime import packet_complete
from sopflow.service import WorkflowError, WorkflowService


def test_human_step_pauses_with_complete_packet(tmp_path):
    svc = WorkflowService(tmp_path)
    st = svc.start_workflow("sup_ticket_triage_auto_reply", branch_choices={"s3": "s5"})
    assert st["status"] == "waiting_for_human"
    p = st["pending_handoff"]
    assert p["step_id"] == "s6" and p["kind"] == "human_step" and packet_complete(p)
    assert set(p["completed_steps"]) == {"s1", "s2", "s3", "s5"}
    with pytest.raises(WorkflowError):
        svc.complete_step(st["run_id"], "s7", "wrong step")
    st = svc.complete_step(st["run_id"], "s6", "approved")
    assert st["status"] == "completed" and st["completed_steps"][-1] == "s8"


def test_request_handoff_escalates_an_agent_step(tmp_path):
    svc = WorkflowService(tmp_path)
    st = svc.start_workflow("p2p_invoice_review", branch_choices={"s2": "s4", "s4": "s5"})
    assert st["status"] == "completed"           # all agent steps
    st = svc.start_workflow("p2p_acceptance_receiving_report")
    run = st["run_id"]
    assert st["pending_handoff"]["step_id"] == "s1"          # s1 and s2 are human steps, s3 is an agent step
    svc.request_handoff(run, "s3", "payments supervisor", "check the vendor first")
    st = svc.complete_step(run, "s1", "accepted")
    assert st["pending_handoff"]["step_id"] == "s2"
    st = svc.complete_step(run, "s2", "signed")
    assert st["pending_handoff"]["step_id"] == "s3" and st["pending_handoff"]["kind"] == "escalation"
    assert svc.complete_step(run, "s3", "forwarded after check")["status"] == "completed"


def test_state_survives_a_new_service_instance(tmp_path):
    run = WorkflowService(tmp_path).start_workflow("onb_form_i9_verification")["run_id"]
    st = WorkflowService(tmp_path).get_state(run)        # new process-equivalent: fresh connections
    assert st["status"] == "waiting_for_human" and st["pending_handoff"]["step_id"] == "s1"


@pytest.mark.parametrize("phase", ["before_commit", "after_commit"])
def test_hard_crash_resumes_without_duplicate_effects(phase):
    if "fork" not in mp.get_all_start_methods():
        pytest.skip("needs fork")
    _, _, ref, _, _ = run_case("hipaa_breach_notification", 3, None)
    crashed, code, fin, eff, _ = run_case("hipaa_breach_notification", 3, ("s2", phase))
    assert crashed and code == 0
    assert fin["done"] == ref["done"] and fin["packets"] == ref["packets"]
    assert all(v == 1 for v in eff.values())
