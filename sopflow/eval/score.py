"""Score a predicted WorkflowSpec against gold.

Steps are matched one-to-one by the SOP lines they cite (Jaccard of line sets >= 0.5, Hungarian assignment
maximising total overlap). Step F1 counts matched pairs. Edge F1 counts predicted edges whose two endpoints
are matched to the endpoints of a gold edge, in the same direction. Handoff F1 counts matched pairs where
both sides mark a handoff. Micro-averaged over SOPs by summing TP / FP / FN."""
from __future__ import annotations

import numpy as np
from scipy.optimize import linear_sum_assignment

from ..spec import WorkflowSpec

THRESH = 0.5


def jaccard(a, b):
    a, b = set(a), set(b)
    return len(a & b) / len(a | b) if a | b else 0.0


def match(pred: WorkflowSpec, gold: WorkflowSpec) -> dict[str, str]:
    """pred step id -> gold step id."""
    if not pred.steps or not gold.steps:
        return {}
    m = np.array([[jaccard(p.lines, g.lines) for g in gold.steps] for p in pred.steps])
    r, c = linear_sum_assignment(-m)
    return {pred.steps[i].id: gold.steps[j].id for i, j in zip(r, c) if m[i, j] >= THRESH}


def counts(pred: WorkflowSpec, gold: WorkflowSpec) -> dict[str, int]:
    mp = match(pred, gold)
    # duplicate predicted ids would make the mapping ambiguous; keep the first occurrence
    ps = {}
    for s in pred.steps:
        ps.setdefault(s.id, s)
    gs = {s.id: s for s in gold.steps}
    out = {"step_tp": len(mp), "step_fp": len(pred.steps) - len(mp), "step_fn": len(gold.steps) - len(mp)}
    gold_edges = {(e.from_, e.to) for e in gold.edges}
    pred_edges = {(e.from_, e.to) for e in pred.edges}
    hit = {(mp[a], mp[b]) for a, b in pred_edges if a in mp and b in mp} & gold_edges
    out |= {"edge_tp": len(hit), "edge_fp": len(pred_edges) - len(hit), "edge_fn": len(gold_edges) - len(hit)}
    p_h = {s.id for s in ps.values() if s.handoff_to}
    g_h = {s.id for s in gs.values() if s.handoff_to}
    h_tp = sum(1 for p, g in mp.items() if p in p_h and g in g_h)
    out |= {"handoff_tp": h_tp, "handoff_fp": len(p_h) - h_tp, "handoff_fn": len(g_h) - h_tp}
    # executor (agent vs human) agreement on matched steps; agent is the positive class
    ex = [(ps[p].executor, gs[g].executor) for p, g in mp.items()]
    out |= {"exec_n": len(ex), "exec_correct": sum(a == b for a, b in ex),
            "agent_tp": sum(a == b == "agent" for a, b in ex), "agent_fp": sum(a == "agent" != b for a, b in ex),
            "agent_fn": sum(b == "agent" != a for a, b in ex)}
    return out


def prf(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    return p, r, (2 * p * r / (p + r) if p + r else 0.0)


def aggregate(rows: list[dict]) -> dict[str, float]:
    out = {}
    for k in ("step", "edge", "handoff"):
        tp, fp, fn = (sum(r[f"{k}_{x}"] for r in rows) for x in ("tp", "fp", "fn"))
        out[f"{k}_p"], out[f"{k}_r"], out[f"{k}_f1"] = prf(tp, fp, fn)
    n = sum(r.get("exec_n", 0) for r in rows)
    out["executor_acc"] = sum(r.get("exec_correct", 0) for r in rows) / n if n else 0.0
    tp, fp, fn = (sum(r.get(f"agent_{x}", 0) for r in rows) for x in ("tp", "fp", "fn"))
    out["agent_p"], out["agent_r"], out["agent_f1"] = prf(tp, fp, fn)
    return out
