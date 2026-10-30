# Automation opportunity: Medicare Advantage standard organization determination (prior authorization)

Process family: **prior_authorization** (mapped to Oracle Health (payer and provider prior authorization)). Spec source: `llm (specs)`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Notify the enrollee | MA organization | **agent** | Compiling and sending a notice from known facts. | enrollee |
| s2 | Extend the timeframe | MA organization | **agent** | AI can determine if the extension is justified and in the enrollee's interest. |  |
| s3 | Review by a physician | MA organization | **human** | A professional, clinical, or accountable judgment is required. |  |
| s4 | Deny a service or item | MA organization | **human** | Needs a professional judgment and a written notice to the enrollee and the physician or provider involved. | enrollee and physician |
| s5 | Provide notice language | MA organization | **agent** | Compiling and drafting a notice from known facts and guidelines. | enrollee |
| s6 | Appeal the failure | MA organization | **human** | Needs a professional judgment and decision to appeal. |  |

- Agent steps: **3 of 6**; handoffs: **3**.
- Agent flags that the (draft) gold labels confirm: **1 of 3**. Unconfirmed flags are where the model over-automates; treat them as candidates for review, not decisions.
- Agreement of these executor calls with the gold labels is scored in `reports/results.csv`.

## Riskiest handoff: s1 (Notify the enrollee) to enrollee
Risk score 4: deadline (no later than 7 calendar days after receiving the request for the standard organization determination), leaves the organisation (enrollee).

Context the packet must carry:

- Instructions (source text): For a service or item subject to the prior authorization rules, the MA organization must notify the enrollee of its determination no later than 7 calendar days after receiving the request for the standard organization determination.
- Deadline: no later than 7 calendar days after receiving the request for the standard organization determination
- Completed steps and their outputs: none (first step)
- Open decisions downstream: none
- Next steps: s2

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 151.6 |
| Cycle time with agents (agent steps instant plus 2 min review) | 107.2 |
| Cycle time saved | 44.1 |
| Hands-on time saved (agent steps minus 2 min review each) | 44.1 |
