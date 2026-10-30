"""WorkflowService: one API over the LangGraph runtime, shared by the MCP server, the REST API and the CLI.
State lives in SQLite (checkpoints + ledger + run index), so any process can pick a run back up."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from langgraph.types import Command

from .runtime import Ledger, build_graph, random_branches, sqlite_checkpointer, new_run_id
from .spec import ROOT, WorkflowSpec, load_gold, load_sop

SPECS = ROOT / "reports" / "specs"


class WorkflowError(ValueError):
    pass


class WorkflowService:
    def __init__(self, db_dir: str | Path = ROOT / "runs_local", spec_source: str = "gold"):
        self.dir = Path(db_dir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.ledger = Ledger(str(self.dir / "ledger.db"))
        self.cp = sqlite_checkpointer(str(self.dir / "checkpoints.db"))
        self.idx = sqlite3.connect(str(self.dir / "runs.db"), check_same_thread=False, isolation_level=None)
        self.idx.execute("CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, sop_id TEXT, spec_source TEXT)")
        self.idx.execute("CREATE TABLE IF NOT EXISTS escalations (run_id TEXT, step_id TEXT, to_role TEXT, note TEXT)")
        self.spec_source = spec_source
        self._graphs = {}

    # ---- helpers
    def _spec(self, sop_id: str, source: str) -> WorkflowSpec:
        if source == "gold":
            return load_gold(sop_id)
        # "llm": the compiled spec exported by sopflow.eval.export_specs
        path = SPECS / f"{sop_id}.json"
        if not path.exists():
            raise WorkflowError(f"no compiled spec for {sop_id}; run the compiler first")
        return WorkflowSpec.model_validate(json.loads(path.read_text()))

    def _graph(self, sop_id: str, source: str):
        key = (sop_id, source)
        if key not in self._graphs:
            self._graphs[key] = build_graph(self._spec(sop_id, source), load_sop(sop_id), self.ledger, self.cp)
        return self._graphs[key]

    def _run(self, run_id: str):
        row = self.idx.execute("SELECT sop_id, spec_source FROM runs WHERE run_id=?", (run_id,)).fetchone()
        if not row:
            raise WorkflowError(f"unknown run {run_id}")
        return row[0], self._graph(*row), {"configurable": {"thread_id": run_id}}

    def _advance(self, graph, cfg, payload):
        graph.invoke(payload, cfg, durability="sync")
        snap = graph.get_state(cfg)
        while snap.next and not snap.interrupts:          # resume after a crash left a pending super-step
            graph.invoke(None, cfg, durability="sync")
            snap = graph.get_state(cfg)

    # ---- public API
    def start_workflow(self, sop_id: str, branch_choices: dict | None = None, seed: int = 0) -> dict:
        source = self.spec_source
        spec = self._spec(sop_id, source)
        load_sop(sop_id)
        run_id = new_run_id()
        self.idx.execute("INSERT INTO runs VALUES (?, ?, ?)", (run_id, sop_id, source))
        graph = self._graph(sop_id, source)
        init = {"run_id": run_id, "sop_id": sop_id, "done": [], "taken": [], "outputs": {}, "packets": [],
                "branch_choices": branch_choices if branch_choices is not None else random_branches(spec, seed),
                "force_handoff": {}}
        self._advance(graph, {"configurable": {"thread_id": run_id}}, init)
        return self.get_state(run_id)

    def get_state(self, run_id: str) -> dict:
        sop_id, graph, cfg = self._run(run_id)
        snap = graph.get_state(cfg)
        v = snap.values
        pending = snap.interrupts[0].value if snap.interrupts else None
        status = "waiting_for_human" if pending else ("completed" if not snap.next else "running")
        return {"run_id": run_id, "sop_id": sop_id, "status": status, "completed_steps": v.get("done", []),
                "outputs": v.get("outputs", {}), "pending_handoff": pending,
                "handoffs_so_far": len(v.get("packets", [])) + (1 if pending else 0)}

    def complete_step(self, run_id: str, step_id: str, output: str, branch: str | None = None) -> dict:
        _, graph, cfg = self._run(run_id)
        snap = graph.get_state(cfg)
        if not snap.interrupts:
            raise WorkflowError("no step is waiting for a human in this run")
        pending = snap.interrupts[0].value
        if pending["step_id"] != step_id:
            raise WorkflowError(f"step {step_id} is not the pending step (pending: {pending['step_id']})")
        reply = {"output": output}
        if branch:
            reply["branch"] = branch
        # escalations requested while the run was paused are applied together with the resume
        esc = dict(self.idx.execute("SELECT step_id, to_role FROM escalations WHERE run_id=?", (run_id,)).fetchall())
        forced = {**snap.values.get("force_handoff", {}), **esc}
        self._advance(graph, cfg, Command(resume=reply, update={"force_handoff": forced}))
        return self.get_state(run_id)

    def request_handoff(self, run_id: str, step_id: str, to_role: str, note: str = "") -> dict:
        """Escalate a step that has not run yet: when the run reaches it, it pauses for `to_role`
        with a context packet instead of being executed automatically."""
        sop_id, graph, cfg = self._run(run_id)
        v = graph.get_state(cfg).values
        ids = {s.id for s in self._spec(sop_id, self.idx.execute(
            "SELECT spec_source FROM runs WHERE run_id=?", (run_id,)).fetchone()[0]).steps}
        if step_id not in ids:
            raise WorkflowError(f"unknown step {step_id}")
        if step_id in v.get("done", []):
            raise WorkflowError(f"step {step_id} already completed")
        self.idx.execute("INSERT INTO escalations VALUES (?, ?, ?, ?)", (run_id, step_id, to_role, note))
        return {"run_id": run_id, "step_id": step_id, "to_role": to_role, "note": note, "status": "handoff_scheduled"}
