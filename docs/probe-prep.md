# Probe prep (answers come only from what this build actually did)

Before an interview:
- Run `pytest -q` and `python -m sopflow.eval.crash_resume`.
- Start the MCP server and click through one run in an MCP client (Claude Desktop: add `python -m sopflow.mcp_server`).
- Read `reports/experiments.csv` top to bottom.

## How the code works, in 5 lines
1. `compiler.py` sends the SOP as numbered lines to Qwen2.5-3B, with prompt v2 (rules for steps, handoffs, agent vs human, edges, and one worked example). llama.cpp's JSON-schema grammar forces parseable output.
2. `validator.py` + `graph.py` (hand-written Kahn topological sort, three-colour DFS cycle finder, OR-join frontier) check the spec. `postprocess.autofix` fixes mechanical errors. Anything left goes back to the LLM as sentences (up to 2 repairs). Then a focused pass classifies each step agent or human.
3. `eval/score.py` matches predicted to gold steps by the lines they cite (Jaccard >= 0.5, Hungarian) and computes step, edge and handoff F1 plus executor accuracy. Splits were fixed before any run, and test ran once.
4. `runtime.py` compiles the spec into a LangGraph `plan -> execute` loop, so every SOP step gets its own SQLite checkpoint. Human steps `interrupt()` with a context packet. Side effects go through an idempotent ledger.
5. `service.py` backs `mcp_server.py` (official MCP Python SDK: start_workflow, get_state, complete_step, request_handoff), `api.py` (FastAPI) and `cli.py` (Typer). Tests call every MCP tool through a real MCP client.

## Probes

**Q: How do you know the LLM output is right?**
- 15s: It isn't trusted; it's scored. Every step must cite SOP lines, and I match those citations to hand labels. On 13 held-out SOPs: step F1 0.874 vs 0.554 for a rule baseline, handoff F1 0.701 vs 0.548.
- 60s: I fixed dev and test splits before any run, chose prompt and model on dev, declared the configuration in a file, then ran test once. The intervals are honest: with 13 SOPs the handoff gain's CI includes zero. The labels are my drafts until reviewed. Evidence: `reports/results.csv`, `reports/bootstrap_ci.json`, `reports/final_test_runs.json`.

**Q: What does the validator catch, and does the repair loop work?**
- Unknown line numbers, edges to missing steps, cycles, self-loops, duplicate ids, steps with no owner or executor, and handoffs to yourself.
- Honest finding: at temperature 0 the model often returned the identical JSON after seeing its errors. What fixed validity was deterministic autofix (dev 9 of 11 → 11 of 11). The LLM is re-prompted only for what autofix can't decide.

**Q: Walk me through a crash.**
- The worker is killed with `os._exit(137)`, either mid-step or right after the side effect commits but before the checkpoint. A new process reads the SQLite checkpoint and continues.
- 432 of 432 runs ended in the same state as an uncrashed run, with 0 duplicate side effects.
- Without the idempotency key, 216 of 216 after-commit crashes double-committed.
- The harness also found that LangGraph's default async checkpointing lost the pending step in 57 of 432 crashes, so the run silently ended early. Sync durability fixed it.

**Q: What's in a handoff packet, and why?**
- Instructions (the source SOP text), the deadline extracted from it, completed steps with their outputs, open decisions downstream, and next steps.
- The person picking it up shouldn't have to open five systems. The crash tests check the packets are byte-identical after resume.

**Q: Which steps would you automate, and how do you avoid over-automating?**
- That's the weak spot. The 3B flags 103 of 137 compiled steps as agent work; the draft gold agrees with 54. Agent vs human accuracy on test is 0.60.
- So the system treats agent flags as candidates: human-executor steps always pause, and `request_handoff` lets anyone escalate a future agent step.
- The opportunity numbers use the reviewed (gold) split: 67 of 115 steps, median 45 hands-on minutes per run, simulated.
- Next: an abstaining classifier that sends "unsure" to a person.

**Q: Your executor second pass helped on dev but hurt on test. Why keep it?**
- I kept the configuration I declared before the test run and reported the drop (0.688 single-pass vs 0.600 two-pass on test). 11 dev SOPs were too few to choose that component reliably.
- Next time: cross-validate component choices across dev folds, not one dev split.

**Q: Why MCP?**
- Any agent (Claude Desktop, an internal assistant) can start a workflow, read its state and complete the human steps without custom glue. The REST API and CLI wrap the same service, so behaviour can't drift between interfaces.

**Q: Why not GPT-4 or Claude for the compiler?**
- The build environment can't reach hosted LLM APIs. I ran an open model in GitHub Actions so every number is reproducible from the Actions tab. `GroqBackend` is wired in; a larger model is the next run through the same harness.

**Q: How does this map to Oracle?**
- Procure-to-pay maps to Fusion ERP, onboarding to HCM, incident handling to OCI security ops, prior authorization to Oracle Health, and support escalation to Oracle Support.
- The documents are public government templates, not Oracle SOPs, and the README says so.
