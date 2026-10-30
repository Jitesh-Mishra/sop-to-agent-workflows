"""Export the primary configuration's final specs (3B, v3) to reports/specs/<sop_id>.json for the runbooks, the
opportunity report and the service (SOPFLOW_SPECS=llm).   python -m sopflow.eval.export_specs"""
from __future__ import annotations

import json

from ..spec import ROOT
from .report import load_records

OUT = ROOT / "reports" / "specs"


def main(model="3b", prompt="v3"):
    OUT.mkdir(parents=True, exist_ok=True)
    recs = [r for r in load_records() if r["model"] == model and r["prompt"] == prompt and r["final_spec"]]
    # the latest run per SOP wins (dev SOPs come from the dev run, test SOPs from the single test run)
    for r in sorted(recs, key=lambda r: r["run_dir"].rsplit("-", 1)[-1]):
        (OUT / f"{r['sop_id']}.json").write_text(json.dumps(r["final_spec"], indent=1))
    print("exported", len({r['sop_id'] for r in recs}), "specs")


if __name__ == "__main__":
    main()
