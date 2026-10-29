# Decisions

**D1 Business grounding: public templates, mapped to Oracle product areas**
- 18 SOPs are grouped in 5 process families, each mapped to the Oracle product area that runs that process:
  - procure-to-pay (FAR, Prompt Payment) -> Fusion ERP Procurement and Payables
  - onboarding (OPM, Form I-9, FEHB) -> Fusion HCM
  - incident handling (NIST SP 800-61, CISA playbooks) -> OCI security operations
  - prior authorization (CMS) -> Oracle Health
  - support escalation -> Oracle Support and Fusion Service
- These are public US government templates, not Oracle internal SOPs, and the README says so.
- The two support SOPs are authored from agent-replay-console's gate policy and marked authored.
- The original 20 government SOPs stay as an out-of-domain test set.

**D2 No hosted LLM is reachable from the build environment, so the LLM runs in GitHub Actions**
- Hugging Face and Groq are blocked from the workspace and from the linked laptop VM.
- `.github/workflows/llm.yml` downloads the official `Qwen/Qwen2.5-{1.5B,3B}-Instruct-GGUF` (Q4_K_M) from Hugging Face on the runner and runs it with llama.cpp on the CPU.
- It commits every raw attempt to the `llm-runs` branch. Scoring is offline and deterministic (`python -m sopflow.eval.report`).
- Anyone can re-run it from the Actions tab. `GroqBackend` exists, but no Groq numbers are claimed.

**D3 Constrained decoding plus a validator repair loop**
- llama.cpp enforces the JSON schema with a grammar, so outputs parse. The failures left are structural: line numbers that do not exist, edges to unknown steps, cycles, a missing owner or executor.
- `validator.py` turns each failure into a plain sentence. The compiler re-prompts with those sentences and the previous JSON, up to 2 times.
- The report shows validity before and after repair, and F1 on the first attempt vs the final spec.

**D4 Scoring by cited lines**
- Every step cites the SOP lines it comes from. Predicted and gold steps are matched one-to-one by the Jaccard overlap of their line sets (>= 0.5, Hungarian assignment).
- Edges count when both endpoints match a gold edge in the same direction. Handoffs and executor are scored on matched steps.
- This needs no fuzzy text matching and is the same for the LLM and the rule baseline.

**D5 Protocol**
- Splits were fixed before any LLM run on this schema (`data/splits.json`):
  - dev = 1 SOP per family + 6 out-of-domain; used for prompt and model choice
  - test = the other 13 family SOPs; run once for the headline
  - test_ood = 14 out-of-domain SOPs; run once
- The rule baseline was written before the family SOPs existed and is frozen. Its keyword lists were drafted after reading the first 20 SOPs, which helps it on the out-of-domain set; that is conservative for the LLM comparison.

**D6 Gold labels are drafts until Jitesh reviews them**
Claude drafted all gold labels from the written guidelines in `data/LABELING.md`. The same agent-vs-human policy is in prompt v2. Every number is reported "against draft gold" until the review lands.

**D7 Runtime: one SOP step per LangGraph super-step**
- The graph is `plan -> execute -> plan`. `plan` computes the ready frontier (an OR-join over the live branches, written by hand in `graph.py`), and `execute` runs one step. So each step gets its own SQLite checkpoint.
- Human steps call `interrupt()` with a context packet. Agent steps run automatically and emit a packet when they hand off.
- Side effects go through a ledger keyed by (run_id, step_id).

**D8 Crash/resume: synchronous checkpoint durability**
- The crash harness kills the worker with `os._exit(137)` mid-step or right after the side effect commits, then resumes in a fresh process.
- With LangGraph's default async durability, some resumed runs silently stopped early: the latest checkpoint was written without its pending next node. That is the async-durability ablation in `reports/crash_resume_summary.json`.
- `durability="sync"` fixed every case.
- The idempotency key is what prevents duplicate side effects when a step re-executes after a post-commit crash. The no-key ablation shows the duplicates.

**D9 Time savings are SIMULATED with an assumed model**
- The workflows run 200 times each through the real runtime with random branches. An assumed time model is applied to the executed paths:
  - agent-eligible steps take 5 to 30 min by hand today and 2 min of review with an agent
  - human steps take 10 to 60 min either way
  - an exponential wait (mean 240 min) is added each time work changes hands between people
- Common random numbers keep the comparison paired.
- These are not measurements. Hands-on minutes saved depend least on the queue assumption and are the number used.
