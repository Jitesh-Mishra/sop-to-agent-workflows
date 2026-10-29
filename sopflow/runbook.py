"""Render a WorkflowSpec as a runbook: step table, Mermaid flowchart, and handoff checklist.

python -m sopflow.runbook --specs reports/specs   ->  docs/runbooks/<sop_id>.md
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from .runtime import DEADLINE
from .spec import ROOT, WorkflowSpec, all_ids, load_gold, load_sop


def mermaid(spec: WorkflowSpec) -> str:
    def label(t):
        return re.sub(r'["\[\](){}<>|]', "", t)[:60]
    out = ["flowchart TD"]
    for s in spec.steps:
        shape = f'{s.id}(["{s.id}: {label(s.action)}"])' if s.executor == "agent" else f'{s.id}["{s.id}: {label(s.action)}"]'
        out.append(f"  {shape}")
    for e in spec.edges:
        out.append(f"  {e.from_} -->|{label(e.condition)}| {e.to}" if e.condition else f"  {e.from_} --> {e.to}")
    out += ["  classDef agent fill:#e3eefb,stroke:#2a78d6", "  classDef human fill:#fde8de,stroke:#eb6834"]
    for kind in ("agent", "human"):
        ids = [s.id for s in spec.steps if s.executor == kind]
        if ids:
            out.append(f"  class {','.join(ids)} {kind}")
    return "\n".join(out)


def render(sop_id: str, spec: WorkflowSpec, source: str) -> str:
    sop = load_sop(sop_id)
    rows = ["| Step | Action | Owner | Executor | Hands to | Deadline | Source lines |", "|---|---|---|---|---|---|---|"]
    for s in spec.steps:
        text = " ".join(sop.lines[i - 1] for i in s.lines if 1 <= i <= len(sop.lines))
        dl = "; ".join(m.group(0) for m in DEADLINE.finditer(text))
        rows.append(f"| {s.id} | {s.action} | {s.role} | {s.executor} | {s.handoff_to or ''} | {dl} | "
                    f"{', '.join(f'L{i}' for i in s.lines)} |")
    hand = [f"- **{s.id}** {s.role} to **{s.handoff_to}**: {s.action}" for s in spec.steps if s.handoff_to]
    return "\n".join([f"# Runbook: {sop.title}", "", f"Source: {sop.source}", "",
                      f"Generated from the `{source}` workflow spec. Rounded boxes are agent steps, square boxes are human steps.",
                      "", "```mermaid", mermaid(spec), "```", "", *rows, "", "## Handoffs", "", *(hand or ["- none"]), ""])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--specs", default=None)
    a = ap.parse_args()
    out = ROOT / "docs" / "runbooks"
    out.mkdir(parents=True, exist_ok=True)
    for sop_id in all_ids():
        p = Path(a.specs) / f"{sop_id}.json" if a.specs else None
        if p and p.exists():
            spec, src = WorkflowSpec.model_validate(json.loads(p.read_text())), "LLM-compiled"
        else:
            spec, src = load_gold(sop_id), "gold"
        (out / f"{sop_id}.md").write_text(render(sop_id, spec, src))
    print("runbooks:", len(all_ids()))


if __name__ == "__main__":
    main()
