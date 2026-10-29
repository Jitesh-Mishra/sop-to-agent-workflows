"""State-aware workflow runtime on LangGraph.

The graph is a two-node loop, plan -> execute -> plan, so every SOP step is its own super-step and gets its own
SQLite checkpoint. Handoff steps pause with interrupt() and carry a context packet; a human (or an MCP client)
resumes them. Side effects go through an idempotent ledger keyed by (run_id, step_id), so a step re-executed
after a crash never commits twice."""
from __future__ import annotations

import os
import random
import re
import sqlite3
import uuid
from typing import Any, Callable, Optional, TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

from .graph import frontier
from .spec import SOP, WorkflowSpec

DEADLINE = re.compile(r"\b(?:within|no later than|not later than)\b[^.;,]*", re.I)


class RunState(TypedDict, total=False):
    run_id: str
    sop_id: str
    current: Optional[str]
    done: list[str]
    taken: list[list[str]]
    outputs: dict[str, str]
    branch_choices: dict[str, str]
    force_handoff: dict[str, str]
    packets: list[dict]


class Ledger:
    """Side-effect store. commit() is idempotent per (run_id, step_id) unless idempotent=False (ablation)."""

    def __init__(self, path: str, idempotent: bool = True):
        self.db = sqlite3.connect(path, check_same_thread=False, isolation_level=None)
        self.db.execute("CREATE TABLE IF NOT EXISTS effects (run_id TEXT, step_id TEXT, output TEXT)")
        self.db.execute("CREATE TABLE IF NOT EXISTS attempts (run_id TEXT, step_id TEXT)")
        if idempotent:
            self.db.execute("CREATE UNIQUE INDEX IF NOT EXISTS ux ON effects(run_id, step_id)")
        self.idempotent = idempotent

    def attempt(self, run_id, step_id):
        self.db.execute("INSERT INTO attempts VALUES (?, ?)", (run_id, step_id))

    def commit(self, run_id, step_id, output):
        verb = "INSERT OR IGNORE" if self.idempotent else "INSERT"
        self.db.execute(f"{verb} INTO effects VALUES (?, ?, ?)", (run_id, step_id, output))

    def effects(self, run_id) -> dict[str, int]:
        rows = self.db.execute("SELECT step_id, COUNT(*) FROM effects WHERE run_id=? GROUP BY step_id", (run_id,))
        return dict(rows.fetchall())

    def attempts(self, run_id) -> dict[str, int]:
        rows = self.db.execute("SELECT step_id, COUNT(*) FROM attempts WHERE run_id=? GROUP BY step_id", (run_id,))
        return dict(rows.fetchall())


def default_executor(step, state) -> str:
    """Stand-in for an agent or tool doing the step; deterministic so runs can be compared."""
    return f"{step.role} completed: {step.action}"


def handoff_packet(spec: WorkflowSpec, sop: SOP | None, state: RunState, step, to_role: str) -> dict:
    src = " ".join(sop.lines[i - 1] for i in step.lines if sop and 1 <= i <= len(sop.lines))
    outs = [e for e in spec.edges if e.from_ == step.id]
    return {
        "packet_version": 1,
        "run_id": state["run_id"], "sop_id": state["sop_id"], "step_id": step.id,
        "action": step.action, "from_role": step.role, "to_role": to_role,
        "instructions": src or step.action,
        "deadline": "; ".join(m.group(0).strip() for m in DEADLINE.finditer(src)) or None,
        "completed_steps": list(state.get("done", [])),
        "prior_outputs": {k: state["outputs"][k] for k in state.get("done", [])},
        "open_questions": [f"Which applies: {e.condition}?" for e in outs if e.condition],
        "next_steps": [e.to for e in outs],
    }


REQUIRED_PACKET_FIELDS = ("run_id", "sop_id", "step_id", "action", "from_role", "to_role", "instructions")


def packet_complete(p: dict) -> bool:
    if any(not p.get(k) for k in REQUIRED_PACKET_FIELDS):
        return False
    # context must cover every completed step
    return set(p["prior_outputs"]) == set(p["completed_steps"])


def build_graph(spec: WorkflowSpec, sop: SOP | None, ledger: Ledger, checkpointer,
                executor: Callable = default_executor, crash: tuple[str, str] | None = None):
    steps = {s.id: s for s in spec.steps}
    ids = [s.id for s in spec.steps]
    pairs = [(e.from_, e.to) for e in spec.edges]

    def plan(state: RunState):
        ready = frontier(ids, pairs, set(state.get("done", [])), {tuple(t) for t in state.get("taken", [])})
        return {"current": ready[0] if ready else None}

    def route(state: RunState):
        return "execute" if state.get("current") else END

    def execute(state: RunState):
        sid = state["current"]
        step = steps[sid]
        to_role = state.get("force_handoff", {}).get(sid) or step.handoff_to
        branch = state.get("branch_choices", {}).get(sid)
        if to_role:
            packet = handoff_packet(spec, sop, state, step, to_role)
            reply = interrupt(packet)            # pauses here; resumed with Command(resume=...)
            output = reply.get("output", "")
            branch = reply.get("branch") or branch
            packets = state.get("packets", []) + [packet]
        else:
            output = executor(step, state)
            packets = state.get("packets", [])
        ledger.attempt(state["run_id"], sid)
        if crash == (sid, "before_commit"):
            os._exit(137)
        ledger.commit(state["run_id"], sid, output)
        if crash == (sid, "after_commit"):
            os._exit(137)                        # effect committed, checkpoint not yet written
        outs = [e for e in spec.edges if e.from_ == sid]
        cond = [e for e in outs if e.condition]
        take = [e for e in outs if not e.condition]
        if cond:
            pick = next((e for e in cond if e.to == branch), cond[0])
            take.append(pick)
        return {"done": state.get("done", []) + [sid], "outputs": {**state.get("outputs", {}), sid: output},
                "taken": state.get("taken", []) + [[e.from_, e.to] for e in take], "packets": packets,
                "current": None}

    g = StateGraph(RunState)
    g.add_node("plan", plan)
    g.add_node("execute", execute)
    g.add_edge(START, "plan")
    g.add_conditional_edges("plan", route, ["execute", END])
    g.add_edge("execute", "plan")
    return g.compile(checkpointer=checkpointer)


def sqlite_checkpointer(path: str) -> SqliteSaver:
    cp = SqliteSaver(sqlite3.connect(path, check_same_thread=False))
    cp.setup()
    return cp


def random_branches(spec: WorkflowSpec, seed: int) -> dict[str, str]:
    """One pre-drawn branch per decision step, so a resumed run follows the same path as the reference."""
    rng = random.Random(seed)
    out = {}
    for s in spec.steps:
        cond = [e.to for e in spec.edges if e.from_ == s.id and e.condition]
        if cond:
            out[s.id] = rng.choice(cond)
    return out


def drive(graph, run_id: str, init: dict, human: Callable[[dict], dict], max_iters: int = 500) -> dict:
    """Run (or resume) to completion: start if no checkpoint, continue after a crash, answer interrupts.
    durability="sync" makes LangGraph persist each checkpoint before the next super-step starts; with the
    default async mode a hard kill can leave a half-written latest checkpoint (found by the crash harness)."""
    cfg = {"configurable": {"thread_id": run_id}}
    for _ in range(max_iters):
        snap = graph.get_state(cfg)
        if not snap.values:
            graph.invoke(init, cfg, durability="sync")
        elif not snap.next:
            return snap.values
        elif snap.interrupts:
            graph.invoke(Command(resume=human(snap.interrupts[0].value)), cfg, durability="sync")
        else:
            graph.invoke(None, cfg, durability="sync")
    raise RuntimeError("workflow did not finish")


def scripted_human(packet: dict) -> dict:
    return {"output": f"{packet['to_role']} acknowledged {packet['step_id']}"}


def new_run_id() -> str:
    return uuid.uuid4().hex[:12]
