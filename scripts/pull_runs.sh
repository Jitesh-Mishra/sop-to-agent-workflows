#!/usr/bin/env bash
# Copy LLM outputs from the llm-runs branch into reports/llm_runs/ (only runs whose name matches $1, default all).
set -e
cd "$(dirname "$0")/.."
git fetch -q origin +refs/heads/llm-runs:refs/remotes/origin/llm-runs
for d in $(git ls-tree --name-only origin/llm-runs runs/ | grep -E "${1:-.}"); do
  out=reports/llm_runs/$(basename $d); mkdir -p $out
  for f in $(git ls-tree --name-only origin/llm-runs $d/); do git show origin/llm-runs:$f > $out/$(basename $f); done
done
ls reports/llm_runs
