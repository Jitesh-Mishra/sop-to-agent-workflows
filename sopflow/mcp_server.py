"""MCP server (official Python SDK v2, MCPServer) exposing the workflow runtime as tools.

    python -m sopflow.mcp_server            # stdio transport, for Claude Desktop or any MCP client
"""
from __future__ import annotations

import os

from mcp.server.mcpserver import MCPServer

from .service import WorkflowService
from .spec import all_ids, family_of, load_sop

mcp = MCPServer("sop-workflows")
_svc: WorkflowService | None = None


def svc() -> WorkflowService:
    global _svc
    if _svc is None:
        _svc = WorkflowService(os.environ.get("SOPFLOW_DB_DIR", "runs_local"), os.environ.get("SOPFLOW_SPECS", "gold"))
    return _svc


@mcp.tool()
def list_workflows() -> list[dict]:
    """List the SOP workflows that can be started, with their process family."""
    return [{"sop_id": i, "title": load_sop(i).title, "family": family_of(i)} for i in all_ids()]


@mcp.tool()
def start_workflow(sop_id: str, seed: int = 0) -> dict:
    """Start a run of an SOP workflow. Agent steps run automatically; the run pauses at the first human handoff."""
    return svc().start_workflow(sop_id, seed=seed)


@mcp.tool()
def get_state(run_id: str) -> dict:
    """Current state of a run: status, completed steps, outputs, and the pending handoff packet if any."""
    return svc().get_state(run_id)


@mcp.tool()
def complete_step(run_id: str, step_id: str, output: str, branch: str | None = None) -> dict:
    """Complete the step that is waiting for a human. `branch` optionally picks the next step id at a decision."""
    return svc().complete_step(run_id, step_id, output, branch)


@mcp.tool()
def request_handoff(run_id: str, step_id: str, to_role: str, note: str = "") -> dict:
    """Escalate a future step to a human role; the run will pause there with a full context packet."""
    return svc().request_handoff(run_id, step_id, to_role, note)


if __name__ == "__main__":
    mcp.run()
