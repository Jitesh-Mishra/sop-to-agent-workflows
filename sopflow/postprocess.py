"""Deterministic clean-up applied to every LLM spec before (and between) repair prompts.

ground_citations: re-cite a step to the SOP line its action text matches best when the cited lines do not contain
                  that line (small models often cite the SOP's own "(1)" numbering instead of L-numbers).
autofix:          fix errors that need no judgment: self-handoffs, out-of-range lines, dangling or self edges,
                  duplicate ids, duplicate edges, and back edges that close a cycle (dropped in reading order).
Everything it changes is logged so the report can separate LLM work from rule fixes."""
from __future__ import annotations

import math
import re
from collections import Counter

from .graph import find_cycle
from .spec import SOP, Edge, WorkflowSpec

TOKEN = re.compile(r"[a-z0-9]+")
STOP = set("the a an of to and or in on for by with is are be shall must may will that this any its it as at from".split())


def _tok(t):
    return [w for w in TOKEN.findall(t.lower()) if w not in STOP]


def _cos(a: Counter, b: Counter, idf):
    num = sum(a[w] * b[w] * idf.get(w, 1.0) ** 2 for w in a if w in b)
    na = math.sqrt(sum((c * idf.get(w, 1.0)) ** 2 for w, c in a.items()))
    nb = math.sqrt(sum((c * idf.get(w, 1.0)) ** 2 for w, c in b.items()))
    return num / (na * nb) if na and nb else 0.0


def ground_citations(spec: WorkflowSpec, sop: SOP, min_sim: float = 0.25) -> tuple[WorkflowSpec, list[str]]:
    docs = [Counter(_tok(l)) for l in sop.lines]
    df = Counter(w for d in docs for w in d)
    idf = {w: math.log((1 + len(docs)) / (1 + c)) + 1 for w, c in df.items()}
    log, steps = [], []
    for s in spec.steps:
        q = Counter(_tok(s.action))
        sims = [_cos(q, d, idf) for d in docs]
        best = max(range(len(sims)), key=sims.__getitem__) + 1 if sims else None
        cited_ok = [l for l in s.lines if 1 <= l <= len(sop.lines)]
        if best and sims[best - 1] >= min_sim and best not in cited_ok:
            log.append(f"{s.id}: lines {s.lines} -> [{best}]")
            s = s.model_copy(update={"lines": [best]})
        steps.append(s)
    return spec.model_copy(update={"steps": steps}), log


def autofix(spec: WorkflowSpec, sop: SOP) -> tuple[WorkflowSpec, list[str]]:
    log, steps, seen = [], [], set()
    rename = {}
    for s in spec.steps:
        upd = {}
        if s.id in seen:
            new = f"{s.id}_{len(seen)}"
            rename.setdefault(s.id, [])
            upd["id"] = new
            log.append(f"duplicate id {s.id} -> {new}")
        seen.add(upd.get("id", s.id))
        lines = [l for l in s.lines if 1 <= l <= len(sop.lines)]
        if lines != s.lines:
            upd["lines"] = lines
            log.append(f"{s.id}: dropped out-of-range lines")
        if s.handoff_to and s.handoff_to.strip().lower() == s.role.strip().lower():
            upd["handoff_to"] = None
            log.append(f"{s.id}: self-handoff removed")
        if s.executor not in ("agent", "human"):
            upd["executor"] = "human"
            log.append(f"{s.id}: missing executor -> human (safe default)")
        if not s.role.strip():
            upd["role"] = "unspecified"
            log.append(f"{s.id}: empty role -> unspecified")
        steps.append(s.model_copy(update=upd))
    steps = [s for s in steps if s.lines] or steps
    ids = {s.id for s in steps}
    edges, pairs = [], set()
    for e in spec.edges:
        if e.from_ not in ids or e.to not in ids or e.from_ == e.to or (e.from_, e.to) in pairs:
            log.append(f"dropped edge {e.from_}->{e.to}")
            continue
        pairs.add((e.from_, e.to))
        edges.append(e)
    first_line = {s.id: min(s.lines) for s in steps}
    order = [s.id for s in steps]
    while (cyc := find_cycle(order, [(e.from_, e.to) for e in edges])):
        ring = list(zip(cyc, cyc[1:] + cyc[:1]))
        back = max(ring, key=lambda ab: first_line[ab[0]] - first_line[ab[1]])
        edges = [e for e in edges if (e.from_, e.to) != back]
        log.append(f"dropped back edge {back[0]}->{back[1]} (cycle)")
    if len(steps) > 1 and not edges:
        srt = sorted(steps, key=lambda s: min(s.lines))
        edges = [Edge(**{"from": a.id, "to": b.id}) for a, b in zip(srt, srt[1:])]
        log.append("no edges: linked steps in reading order")
    return WorkflowSpec(steps=steps, edges=edges), log


def postprocess(spec: WorkflowSpec, sop: SOP) -> tuple[WorkflowSpec, list[str]]:
    spec, l1 = ground_citations(spec, sop)
    spec, l2 = autofix(spec, sop)
    return spec, l1 + l2
