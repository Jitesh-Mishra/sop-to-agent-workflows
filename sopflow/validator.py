"""Structural checks on a compiled WorkflowSpec. Each error is a plain sentence the repair prompt can quote."""
from __future__ import annotations

from .graph import find_cycle
from .spec import WorkflowSpec


def validate(spec: WorkflowSpec, n_lines: int) -> list[str]:
    errs = []
    ids = [s.id for s in spec.steps]
    if not spec.steps:
        return ["The workflow has no steps."]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        errs.append(f"Duplicate step ids: {', '.join(dup)}. Every step id must be unique.")
    for s in spec.steps:
        if not s.action.strip():
            errs.append(f"Step {s.id} has an empty action.")
        if not s.role.strip():
            errs.append(f"Step {s.id} has no role. Every step needs an owner.")
        if s.executor not in ("agent", "human"):
            errs.append(f"Step {s.id} needs executor \"agent\" or \"human\".")
        if not s.lines:
            errs.append(f"Step {s.id} cites no SOP lines.")
        bad = [l for l in s.lines if not 1 <= l <= n_lines]
        if bad:
            errs.append(f"Step {s.id} cites lines {bad} that do not exist (the SOP has lines 1 to {n_lines}).")
        if s.handoff_to is not None and s.handoff_to.strip().lower() == s.role.strip().lower():
            errs.append(f"Step {s.id} hands off to its own role ({s.role}); a handoff must go to a different party.")
    idset = set(ids)
    for e in spec.edges:
        for end in (e.from_, e.to):
            if end not in idset:
                errs.append(f"Edge {e.from_} -> {e.to} refers to unknown step {end}.")
        if e.from_ == e.to:
            errs.append(f"Edge {e.from_} -> {e.to} is a self-loop.")
    pairs = [(e.from_, e.to) for e in spec.edges]
    if len(set(pairs)) < len(pairs):
        errs.append("Some edges are duplicated.")
    good = [(a, b) for a, b in pairs if a in idset and b in idset and a != b]
    cyc = find_cycle(list(dict.fromkeys(ids)), good)
    if cyc:
        errs.append(f"The workflow has a cycle: {' -> '.join(cyc + [cyc[0]])}. It must be a directed acyclic graph.")
    if len(spec.steps) > 1 and not spec.edges:
        errs.append("The workflow has several steps but no edges; connect the steps in execution order.")
    return errs
