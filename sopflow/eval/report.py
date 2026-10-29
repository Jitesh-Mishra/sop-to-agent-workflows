"""Score LLM runs (pulled from the llm-runs branch into reports/llm_runs/) and the rule baseline.

python -m sopflow.eval.report  ->  reports/results.csv, reports/results_per_sop.csv, reports/results_by_family.csv
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from ..baseline import extract
from ..spec import ROOT, WorkflowSpec, family_of, load_gold, load_sop, split
from ..validator import validate
from .score import aggregate, counts

RUNS = ROOT / "reports" / "llm_runs"
OUT = ROOT / "reports"
SPLITS = ("dev", "test", "test_ood")


def split_of(sop_id):
    return next(s for s in SPLITS if sop_id in split(s))


def load_records(run_dirs=None) -> list[dict]:
    recs = []
    for d in sorted(run_dirs or [p for p in RUNS.glob("*") if p.is_dir()]):
        meta = {}
        for m in d.glob("meta_*.json"):
            meta = json.loads(m.read_text())
        for f in d.glob("*.json"):
            if f.name.startswith("meta_"):
                continue
            r = json.loads(f.read_text())
            r["run_dir"] = d.name
            r["model_name"] = meta.get("model", r["model"])
            recs.append(r)
    return recs


def spec_or_empty(raw_spec):
    return WorkflowSpec.model_validate(raw_spec) if raw_spec else WorkflowSpec(steps=[], edges=[])


def first_spec(rec):
    try:
        return WorkflowSpec.model_validate(json.loads(rec["attempts"][0]["raw"]))
    except Exception:
        return WorkflowSpec(steps=[], edges=[])


def per_sop_rows(recs):
    rows = []
    for r in recs:
        gold = load_gold(r["sop_id"])
        for stage, spec in (("final", spec_or_empty(r["final_spec"])), ("first_attempt", first_spec(r))):
            c = counts(spec, gold)
            rows.append({"system": f"llm:{r['model']}:{r['prompt']}", "stage": stage, "sop_id": r["sop_id"],
                         "split": split_of(r["sop_id"]), "family": family_of(r["sop_id"]), "run_dir": r["run_dir"],
                         "attempts": len(r["attempts"]), "valid_first": not r["attempts"][0]["errors"],
                         "valid_final": not r["attempts"][-1]["errors"],
                         "seconds": sum(a["usage"].get("seconds", 0) for a in r["attempts"]), **c})
    return rows


def baseline_rows(sop_ids):
    rows = []
    for i in sop_ids:
        sop = load_sop(i)
        spec = extract(sop)
        c = counts(spec, load_gold(i))
        ok = not validate(spec, len(sop.lines))
        rows.append({"system": "rule_baseline", "stage": "final", "sop_id": i, "split": split_of(i),
                     "family": family_of(i), "run_dir": "", "attempts": 1, "valid_first": ok, "valid_final": ok,
                     "seconds": 0.0, **c})
    return rows


def summarize(df: pd.DataFrame, keys) -> pd.DataFrame:
    out = []
    for k, g in df.groupby(keys, sort=False):
        agg = aggregate(g.to_dict("records"))
        out.append({**dict(zip(keys, k if isinstance(k, tuple) else (k,))), "n_sops": len(g),
                    **{m: round(agg[m], 3) for m in ("step_f1", "edge_f1", "handoff_f1", "executor_acc", "agent_f1",
                                                      "step_p", "step_r", "handoff_p", "handoff_r")},
                    "valid_first_rate": round(g["valid_first"].mean(), 3), "valid_final_rate": round(g["valid_final"].mean(), 3),
                    "mean_attempts": round(g["attempts"].mean(), 2), "mean_seconds": round(g["seconds"].mean(), 1)})
    return pd.DataFrame(out)


def main():
    recs = load_records()
    llm = pd.DataFrame(per_sop_rows(recs))
    sops = sorted({r["sop_id"] for r in recs}) or [i for s in SPLITS for i in split(s)]
    base = pd.DataFrame(baseline_rows([i for s in SPLITS for i in split(s)]))
    allrows = pd.concat([base, llm], ignore_index=True) if len(llm) else base
    allrows.to_csv(OUT / "results_per_sop.csv", index=False)
    res = summarize(allrows, ["split", "system", "stage"])
    res.to_csv(OUT / "results.csv", index=False)
    fam = summarize(allrows[allrows["stage"] == "final"], ["split", "family", "system"])
    fam.to_csv(OUT / "results_by_family.csv", index=False)
    with pd.option_context("display.width", 220, "display.max_columns", 30):
        print(res[res["stage"] == "final"].drop(columns=["stage"]).to_string(index=False))
    return res


if __name__ == "__main__":
    main()
