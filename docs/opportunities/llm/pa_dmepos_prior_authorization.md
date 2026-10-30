# Automation opportunity: Prior authorization for DMEPOS items

Process family: **prior_authorization** (mapped to Oracle Health (payer and provider prior authorization)). Spec source: `llm (specs)`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Include all relevant documentation | requester | **agent** | Compiling and checking documents is an information work an AI agent can do with system access. |  |
| s2 | Submit before item is furnished | requester | **agent** | Submitting a request is information work that an AI agent can do. |  |
| s3 | Review by CMS or contractor | CMS or contractor | **agent** | Searching and correlating information to review a prior authorization request. |  |
| s4 | Provisional affirmation if rules met | CMS or contractor | **agent** | Checking and verifying rules to determine if a provisional affirmation is issued. |  |
| s5 | Non-affirmation decision if rules not met | CMS or contractor | **human** | Requires a professional judgment and decision. |  |
| s6 | Resubmit if non-affirmation | requester | **agent** | Resubmitting a request is an information work that an AI agent can do. |  |
| s7 | Include expedited review documentation | requester | **agent** | Compiling and checking documents. |  |

- Agent steps: **6 of 7**; handoffs: **0**.
- Agent flags that the (draft) gold labels confirm: **4 of 6**. Unconfirmed flags are where the model over-automates; treat them as candidates for review, not decisions.
- Agreement of these executor calls with the gold labels is scored in `reports/results.csv`.

## Riskiest handoff: s5 (Non-affirmation decision if rules not met) to CMS or contractor
Risk score 3: leaves the organisation (CMS or contractor), a person must act.

Context the packet must carry:

- Instructions (source text): If applicable rules are not met, CMS or its contractor issues a non-affirmation decision to the requester.
- Deadline: none stated
- Completed steps and their outputs: s1, s2, s3
- Open decisions downstream: none
- Next steps: s6

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 355.2 |
| Cycle time with agents (agent steps instant plus 2 min review) | 8.0 |
| Cycle time saved | 325.9 |
| Hands-on time saved (agent steps minus 2 min review each) | 65.0 |
