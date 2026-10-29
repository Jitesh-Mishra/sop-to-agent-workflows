"""REST API over the same WorkflowService.   uvicorn sopflow.api:app --port 8000"""
from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .service import WorkflowError, WorkflowService
from .spec import all_ids, family_of, load_sop

app = FastAPI(title="SOP-to-Agent Workflow Engine")
svc = WorkflowService(os.environ.get("SOPFLOW_DB_DIR", "runs_local"), os.environ.get("SOPFLOW_SPECS", "gold"))


class StartBody(BaseModel):
    sop_id: str
    seed: int = 0


class CompleteBody(BaseModel):
    output: str
    branch: str | None = None


class HandoffBody(BaseModel):
    step_id: str
    to_role: str
    note: str = ""


def _call(fn, *a):
    try:
        return fn(*a)
    except WorkflowError as e:
        raise HTTPException(409, str(e))
    except FileNotFoundError as e:
        raise HTTPException(404, str(e))


@app.get("/workflows")
def workflows():
    return [{"sop_id": i, "title": load_sop(i).title, "family": family_of(i)} for i in all_ids()]


@app.post("/runs")
def start(b: StartBody):
    return _call(svc.start_workflow, b.sop_id, None, b.seed)


@app.get("/runs/{run_id}")
def state(run_id: str):
    return _call(svc.get_state, run_id)


@app.post("/runs/{run_id}/steps/{step_id}/complete")
def complete(run_id: str, step_id: str, b: CompleteBody):
    return _call(svc.complete_step, run_id, step_id, b.output, b.branch)


@app.post("/runs/{run_id}/handoffs")
def handoff(run_id: str, b: HandoffBody):
    return _call(svc.request_handoff, run_id, b.step_id, b.to_role, b.note)
