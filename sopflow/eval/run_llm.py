"""Generate LLM workflow specs for one split and save every attempt (run in CI by .github/workflows/llm.yml).
Scoring is separate and deterministic: python -m sopflow.eval.report.

python -m sopflow.eval.run_llm --split dev --model 1.5b --prompts v1,v2 --out ci_out
"""
from __future__ import annotations

import argparse
import json
import platform
import time
from pathlib import Path

from ..compiler import LlamaCppBackend, compile_sop
from ..spec import load_sop, split

MODELS = {"1.5b": ("Qwen/Qwen2.5-1.5B-Instruct-GGUF", "qwen2.5-1.5b-instruct-q4_k_m.gguf"),
          "3b": ("Qwen/Qwen2.5-3B-Instruct-GGUF", "qwen2.5-3b-instruct-q4_k_m.gguf")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", required=True)
    ap.add_argument("--model", default="1.5b", choices=MODELS)
    ap.add_argument("--prompts", default="v1,v2")
    ap.add_argument("--max-repairs", type=int, default=2)
    ap.add_argument("--out", default="ci_out")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    backend = LlamaCppBackend(*MODELS[a.model])
    meta = {"split": a.split, "model": backend.name, "model_key": a.model, "prompts": a.prompts.split(","),
            "max_repairs": a.max_repairs, "temperature": 0.0, "machine": platform.platform(),
            "load_seconds": round(time.time() - t0, 1)}
    for version in meta["prompts"]:
        for sop_id in split(a.split):
            r = compile_sop(load_sop(sop_id), backend, version, a.max_repairs)
            rec = {"sop_id": sop_id, "prompt": version, "model": a.model,
                   "attempts": [{"raw": x.raw, "errors": x.errors, "usage": x.usage} for x in r.attempts],
                   "final_spec": r.spec.dump() if r.spec else None}
            (out / f"{a.model}_{version}_{sop_id}.json").write_text(json.dumps(rec, indent=1))
            print(f"[{time.time() - t0:.0f}s] {version} {sop_id} attempts={len(r.attempts)} "
                  f"valid_first={r.valid_first} valid_final={r.valid_final}", flush=True)
    meta["total_seconds"] = round(time.time() - t0, 1)
    (out / f"meta_{a.model}.json").write_text(json.dumps(meta, indent=1))


if __name__ == "__main__":
    main()
