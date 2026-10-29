"""Command line:  python -m sopflow.cli --help"""
from __future__ import annotations

import json

import typer

from .baseline import extract
from .service import WorkflowService
from .spec import all_ids, load_gold, load_sop
from .validator import validate

app = typer.Typer(add_completion=False, help="SOP-to-Agent Workflow Engine")


def _svc(db: str):
    return WorkflowService(db)


@app.command("list")
def list_sops():
    """List SOP ids."""
    for i in all_ids():
        typer.echo(f"{i:40s} {load_sop(i).title}")


@app.command()
def show(sop_id: str, source: str = typer.Option("gold", help="gold | baseline")):
    """Print a workflow spec and its validator result."""
    sop = load_sop(sop_id)
    spec = load_gold(sop_id) if source == "gold" else extract(sop)
    typer.echo(json.dumps(spec.dump(), indent=1))
    typer.echo(f"validator: {validate(spec, len(sop.lines)) or 'ok'}")


@app.command()
def start(sop_id: str, seed: int = 0, db: str = "runs_local"):
    """Start a run; prints state (pauses at the first human handoff)."""
    typer.echo(json.dumps(_svc(db).start_workflow(sop_id, seed=seed), indent=1))


@app.command()
def state(run_id: str, db: str = "runs_local"):
    typer.echo(json.dumps(_svc(db).get_state(run_id), indent=1))


@app.command()
def complete(run_id: str, step_id: str, output: str, branch: str = typer.Option(None), db: str = "runs_local"):
    typer.echo(json.dumps(_svc(db).complete_step(run_id, step_id, output, branch), indent=1))


@app.command()
def handoff(run_id: str, step_id: str, to_role: str, note: str = "", db: str = "runs_local"):
    typer.echo(json.dumps(_svc(db).request_handoff(run_id, step_id, to_role, note), indent=1))


if __name__ == "__main__":
    app()
