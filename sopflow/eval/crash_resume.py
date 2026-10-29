"""Crash/resume harness. For every gold workflow and every step on its executed path, kill the worker process
(os._exit(137), no cleanup) either mid-step before the side effect commits, or right after the commit but
before LangGraph writes the checkpoint. A fresh process then resumes from the SQLite checkpoint.

Pass = final state equals an uncrashed reference run (same completed steps, outputs, branches taken and
handoff packets) AND every completed step has exactly one committed side effect.
Ablations: (1) after-commit crashes with a non-idempotent ledger, to show why the idempotency key matters;
(2) LangGraph's default async checkpoint durability instead of durability="sync".

python -m sopflow.eval.crash_resume  ->  reports/crash_resume.csv, reports/crash_resume_summary.json
"""
from __future__ import annotations

import json
import multiprocessing as mp
import tempfile
import time
from pathlib import Path

from ..runtime import Ledger, build_graph, drive, random_branches, scripted_human, sqlite_checkpointer
from ..spec import ROOT, all_ids, load_gold, load_sop

REPORTS = ROOT / "reports"


def _init(spec, sop_id, run_id, seed):
    return {"run_id": run_id, "sop_id": sop_id, "done": [], "taken": [], "outputs": {},
            "branch_choices": random_branches(spec, seed), "packets": []}


def _worker(sop_id, workdir, run_id, seed, crash, idempotent, durability="sync"):
    spec, sop = load_gold(sop_id), load_sop(sop_id)
    g = build_graph(spec, sop, Ledger(f"{workdir}/ledger.db", idempotent), sqlite_checkpointer(f"{workdir}/ckpt.db"),
                    crash=crash)
    drive(g, run_id, _init(spec, sop_id, run_id, seed), scripted_human, durability=durability)


def _final(sop_id, workdir, run_id):
    spec, sop = load_gold(sop_id), load_sop(sop_id)
    led = Ledger(f"{workdir}/ledger.db", idempotent=False)  # read-only use
    g = build_graph(spec, sop, led, sqlite_checkpointer(f"{workdir}/ckpt.db"))
    snap = g.get_state({"configurable": {"thread_id": run_id}})
    return snap.values, led.effects(run_id), led.attempts(run_id)


def run_case(sop_id, seed, crash, idempotent=True, durability="sync"):
    ctx = mp.get_context("fork")
    with tempfile.TemporaryDirectory() as wd:
        run_id = f"{sop_id}-{seed}"
        p = ctx.Process(target=_worker, args=(sop_id, wd, run_id, seed, crash, idempotent, durability))
        p.start(); p.join()
        crashed = p.exitcode == 137
        p = ctx.Process(target=_worker, args=(sop_id, wd, run_id, seed, None, idempotent, durability))  # restart = new process
        p.start(); p.join()
        return crashed, p.exitcode, *_final(sop_id, wd, run_id)


def main(seed: int = 7):
    REPORTS.mkdir(exist_ok=True)
    rows = []
    t0 = time.time()
    for sop_id in all_ids():
        _, _, ref, ref_eff, _ = run_case(sop_id, seed, None)
        key = lambda v: (v["done"], v["outputs"], v["taken"], v["packets"])
        for step in ref["done"]:
            for phase, idem, dur in (("before_commit", True, "sync"), ("after_commit", True, "sync"),
                                     ("after_commit", False, "sync"), ("before_commit", True, "async"),
                                     ("after_commit", True, "async")):
                crashed, code, fin, eff, att = run_case(sop_id, seed, (step, phase), idem, dur)
                dup = sum(1 for v in eff.values() if v > 1)
                rows.append({"sop_id": sop_id, "crash_step": step, "phase": phase, "idempotent_ledger": idem, "durability": dur,
                             "crashed": crashed, "resume_exit": code, "state_matches_reference": key(fin) == key(ref),
                             "steps_committed": len(eff), "duplicate_effects": dup,
                             "reexecuted_steps": sum(1 for v in att.values() if v > 1),
                             "recovered": crashed and code == 0 and key(fin) == key(ref) and dup == 0
                                          and set(eff) == set(ref["done"])})
        print(f"[{time.time() - t0:.0f}s] {sop_id}: {len(ref['done'])} steps", flush=True)
    import csv
    with open(REPORTS / "crash_resume.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    summ = {}
    sync = lambda r: r["durability"] == "sync"
    for name, sel in (("before_commit", lambda r: sync(r) and r["phase"] == "before_commit"),
                      ("after_commit", lambda r: sync(r) and r["phase"] == "after_commit" and r["idempotent_ledger"]),
                      ("ablation_after_commit_no_idempotency_key", lambda r: sync(r) and r["phase"] == "after_commit" and not r["idempotent_ledger"]),
                      ("ablation_async_checkpoint_durability", lambda r: not sync(r))):
        rs = [r for r in rows if sel(r)]
        summ[name] = {"crashes": sum(r["crashed"] for r in rs), "recovered": sum(r["recovered"] for r in rs),
                      "state_matches": sum(r["state_matches_reference"] for r in rs),
                      "runs_with_duplicate_effects": sum(r["duplicate_effects"] > 0 for r in rs),
                      "reexecuted_steps": sum(r["reexecuted_steps"] for r in rs)}
    summ["workflows"] = len(all_ids())
    summ["seconds"] = round(time.time() - t0, 1)
    (REPORTS / "crash_resume_summary.json").write_text(json.dumps(summ, indent=1))
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    main()
