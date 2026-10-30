"""Automation opportunity report per SOP, from a compiled workflow spec.

For each SOP: which steps an agent can take and why, which stay with people, how many handoffs there are,
the riskiest handoff and the context it must carry, and estimated time saved. Time numbers come from SIMULATED
runs: the real LangGraph runtime executes each workflow 200 times with random branch choices, and an ASSUMED time
model (below) is applied to the executed paths. Nothing here is measured from a real organisation.

python -m sopflow.eval.opportunity --specs reports/specs  ->  reports/opportunity_llm.csv, docs/opportunities/llm/*.md
python -m sopflow.eval.opportunity                        ->  reports/opportunity_gold.csv, docs/opportunities/gold/*.md
"""
from __future__ import annotations

import argparse
import json
import random
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

from ..runtime import Ledger, build_graph, drive, random_branches, scripted_human, sqlite_checkpointer
from ..spec import ROOT, WorkflowSpec, families, family_of, load_gold, load_sop

# ---- ASSUMED time model (minutes); see docs/decisions.md D9
MANUAL_STEP = (5, 15, 30)        # triangular(min, mode, max) hands-on time for a step a person does today
HUMAN_STEP = (10, 30, 60)        # hands-on time for a step that stays with a person (unchanged by automation)
AGENT_REVIEW = 2                 # a person skims the agent's output
QUEUE_WAIT_MEAN = 240            # mean wait (exponential) whenever work passes to a different person
N_RUNS = 200
EXTERNAL = ("cms", "contractor", "vendor", "enrollee", "customer", "osha", "cisa", "ire", "independent entity", "fda",
            "selectee", "supplier", "provider", "president", "congress", "law enforcement", "requester", "public",
            "media", "secretary", "national response center", "phmsa", "911", "lepc", "serc", "court", "board")


def executed_paths(spec: WorkflowSpec, sop_id: str, n: int = N_RUNS):
    with tempfile.TemporaryDirectory() as d:
        g = build_graph(spec, load_sop(sop_id), Ledger(f"{d}/l.db"), sqlite_checkpointer(f"{d}/c.db"))
        out = []
        for seed in range(n):
            rid = f"{sop_id}-{seed}"
            fin = drive(g, rid, {"run_id": rid, "sop_id": sop_id, "done": [], "taken": [], "outputs": {}, "packets": [],
                                 "branch_choices": random_branches(spec, seed)}, scripted_human)
            out.append((fin["done"], fin["packets"]))
        return out


def simulate(spec: WorkflowSpec, paths, seed: int = 0):
    """Common random numbers: each executed step draws its hands-on time and queue wait once, and both scenarios
    reuse the draws, so the difference reflects the executor split rather than sampling noise."""
    rng = random.Random(seed)
    steps = {s.id: s for s in spec.steps}
    manual, assisted, hands_on_saved = [], [], []
    for done, _ in paths:
        tm = ta = hs = 0.0
        prev_m = prev_a = None
        for sid in done:
            s = steps[sid]
            human = s.executor == "human"
            lo, mode, hi = HUMAN_STEP if human else MANUAL_STEP
            h = rng.triangular(lo, hi, mode)
            wait = rng.expovariate(1 / QUEUE_WAIT_MEAN)
            tm += h + (wait if prev_m not in (None, s.role) else 0.0)
            prev_m = s.role
            if human:
                ta += h + (wait if prev_a not in (None, s.role) else 0.0)
                prev_a = s.role
            else:
                ta += AGENT_REVIEW
                hs += h - AGENT_REVIEW
        manual.append(tm)
        assisted.append(ta)
        hands_on_saved.append(hs)
    return np.array(manual), np.array(assisted), np.array(hands_on_saved)


def handoff_risk(p: dict) -> tuple[int, list[str]]:
    why, score = [], 0
    if p.get("deadline"):
        score += 2; why.append(f"deadline ({p['deadline']})")
    if any(k in p["to_role"].lower() for k in EXTERNAL):
        score += 2; why.append(f"leaves the organisation ({p['to_role']})")
    if p.get("open_questions"):
        score += len(p["open_questions"]); why.append(f"{len(p['open_questions'])} open decision(s) downstream")
    if p.get("kind") == "human_step":
        score += 1; why.append("a person must act")
    return score, why


def report_one(sop_id: str, spec: WorkflowSpec, source: str) -> tuple[dict, str]:
    paths = executed_paths(spec, sop_id)
    manual, assisted, saved = simulate(spec, paths)
    agents = [s for s in spec.steps if s.executor == "agent"]
    humans = [s for s in spec.steps if s.executor == "human"]
    handoffs = [s for s in spec.steps if s.handoff_to]
    packets = {}
    for _, ps in paths:
        for p in ps:
            packets.setdefault(p["step_id"], p)
    ranked = sorted(((handoff_risk(p), p) for p in packets.values()), key=lambda x: -x[0][0])
    risky = ranked[0] if ranked else None
    from .score import match
    gold = load_gold(sop_id)
    gmap = {g.id: g for g in gold.steps}
    m = match(spec, gold)
    confirmed = sum(1 for s in agents if s.id in m and gmap[m[s.id]].executor == "agent")
    row = {"sop_id": sop_id, "family": family_of(sop_id), "spec_source": source, "steps": len(spec.steps),
           "agent_steps": len(agents), "agent_steps_confirmed_by_gold": confirmed, "human_steps": len(humans),
           "handoffs": len(handoffs),
           "riskiest_handoff": risky[1]["step_id"] if risky else None,
           "sim_runs": len(paths), "sim_manual_cycle_min_median": round(float(np.median(manual)), 1),
           "sim_assisted_cycle_min_median": round(float(np.median(assisted)), 1),
           "sim_hands_on_minutes_saved_median": round(float(np.median(saved)), 1),
           "sim_completion_rate": round(sum(1 for d, _ in paths if d) / len(paths), 3),
           "sim_handoff_packets_per_run": round(float(np.mean([len(p) for _, p in paths])), 2),
           "sim_human_pauses_per_run": round(float(np.mean([sum(1 for x in p if x["kind"] == "human_step") for _, p in paths])), 2),
           "sim_cycle_minutes_saved_median": round(float(np.median(manual - assisted)), 1)}
    fam = families()[row["family"]]
    lines = [f"# Automation opportunity: {load_sop(sop_id).title}", "",
             f"Process family: **{row['family']}** (mapped to {fam['oracle_area']}). Spec source: `{source}`. "
             "Public template mapped to an Oracle product area, not an Oracle internal SOP.", "",
             "| Step | Action | Role | Executor | Why | Handoff to |", "|---|---|---|---|---|---|"]
    for s in spec.steps:
        lines.append(f"| {s.id} | {s.action} | {s.role} | **{s.executor}** | {s.executor_reason or ''} | {s.handoff_to or ''} |")
    lines += ["", f"- Agent steps: **{len(agents)} of {len(spec.steps)}**; handoffs: **{len(handoffs)}**."]
    if source != "gold":
        lines.append(f"- Agent flags that the (draft) gold labels confirm: **{confirmed} of {len(agents)}**. "
                     "Unconfirmed flags are where the model over-automates; treat them as candidates for review, not decisions.")
    if source != "gold":
        lines.append("- Agreement of these executor calls with the gold labels is scored in `reports/results.csv`.")
    if risky:
        (score, why), p = risky
        lines += ["", f"## Riskiest handoff: {p['step_id']} ({p['action']}) to {p['to_role']}",
                  f"Risk score {score}: {', '.join(why)}.", "", "Context the packet must carry:", "",
                  f"- Instructions (source text): {p['instructions']}",
                  f"- Deadline: {p['deadline'] or 'none stated'}",
                  f"- Completed steps and their outputs: {', '.join(p['completed_steps']) or 'none (first step)'}",
                  f"- Open decisions downstream: {'; '.join(p['open_questions']) or 'none'}",
                  f"- Next steps: {', '.join(p['next_steps']) or 'end of workflow'}"]
    lines += ["", "## Estimated time (SIMULATED)",
              f"{len(paths)} runs through the LangGraph runtime with random branch choices and the assumed time model "
              "in `sopflow/eval/opportunity.py` (not measured data).", "",
              "| | Median minutes per run |", "|---|---:|",
              f"| Cycle time today (every step by a person, queue wait at each change of hands) | {row['sim_manual_cycle_min_median']} |",
              f"| Cycle time with agents (agent steps instant plus 2 min review) | {row['sim_assisted_cycle_min_median']} |",
              f"| Cycle time saved | {row['sim_cycle_minutes_saved_median']} |",
              f"| Hands-on time saved (agent steps minus 2 min review each) | {row['sim_hands_on_minutes_saved_median']} |"]
    return row, "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--specs", default=None, help="directory of compiled specs <sop_id>.json; default gold")
    ap.add_argument("--families-only", action="store_true", default=True)
    a = ap.parse_args()
    out_dir = ROOT / "docs" / "opportunities" / ("llm" if a.specs else "gold")
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    ids = [i for k, v in families().items() if k != "ood_government_misc" for i in v["sops"]]
    for sop_id in ids:
        p = Path(a.specs) / f"{sop_id}.json" if a.specs else None
        if p and p.exists():
            spec, source = WorkflowSpec.model_validate(json.loads(p.read_text())), f"llm ({p.parent.name})"
        else:
            spec, source = load_gold(sop_id), "gold"
        row, md = report_one(sop_id, spec, source)
        rows.append(row)
        (out_dir / f"{sop_id}.md").write_text(md)
    df = pd.DataFrame(rows)
    df.to_csv(ROOT / "reports" / f"opportunity_{'llm' if a.specs else 'gold'}.csv", index=False)
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
