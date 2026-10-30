# Automation opportunity: Medicare Advantage standard reconsideration of an adverse determination

Process family: **prior_authorization** (mapped to Oracle Health (payer and provider prior authorization)). Spec source: `llm (specs)`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Make a written request | party to the organization determination | **agent** | Drafting and sending a written request. | MA organization |
| s2 | File within 60 days | party to the organization determination | **agent** | Routine record keeping and tracking of the filing within the specified time frame. |  |
| s3 | File a late request if necessary | party to the organization determination | **agent** | Compiling and drafting a written request for reconsideration. | MA organization |
| s4 | Receive a favorable reconsidered determination | MA organization | **agent** | Compiling and forwarding the determination to the appropriate parties. |  |
| s5 | Receive a reaffirming determination | MA organization | **agent** | Compiling and sending a written explanation and case file. | CMS contracted entity |

- Agent steps: **5 of 5**; handoffs: **3**.
- Agent flags that the (draft) gold labels confirm: **1 of 5**. Unconfirmed flags are where the model over-automates; treat them as candidates for review, not decisions.
- Agreement of these executor calls with the gold labels is scored in `reports/results.csv`.

## Riskiest handoff: s5 (Receive a reaffirming determination) to CMS contracted entity
Risk score 4: deadline (no later than 30 calendar days from the date it receives the request), leaves the organisation (CMS contracted entity).

Context the packet must carry:

- Instructions (source text): If the MA organization affirms, in whole or in part, its adverse organization determination, it must prepare a written explanation and send the case file to the independent entity contracted by CMS no later than 30 calendar days from the date it receives the request.
- Deadline: no later than 30 calendar days from the date it receives the request
- Completed steps and their outputs: s1, s2, s3, s4
- Open decisions downstream: none
- Next steps: end of workflow

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 228.8 |
| Cycle time with agents (agent steps instant plus 2 min review) | 8.0 |
| Cycle time saved | 220.8 |
| Hands-on time saved (agent steps minus 2 min review each) | 63.8 |
