# Automation opportunity: Medicare Advantage standard organization determination (prior authorization)

Process family: **prior_authorization** (mapped to Oracle Health (payer and provider prior authorization)). Spec source: `gold`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Physician reviews an expected adverse medical necessity decision | physician reviewer | **human** |  |  |
| s2 | Notify the enrollee of the determination within 7 calendar days | MA organization | **agent** |  | enrollee |
| s3 | Extend the timeframe up to 14 days | MA organization | **human** |  |  |
| s4 | Send the written denial notice with reasons and reconsideration rights | MA organization | **agent** |  | enrollee and provider |

- Agent steps: **2 of 4**; handoffs: **2**.

## Riskiest handoff: s2 (Notify the enrollee of the determination within 7 calendar days) to enrollee
Risk score 4: deadline (no later than 7 calendar days after receiving the request for the standard organization determination), leaves the organisation (enrollee).

Context the packet must carry:

- Instructions (source text): For a service or item subject to the prior authorization rules, the MA organization must notify the enrollee of its determination no later than 7 calendar days after receiving the request for the standard organization determination.
- Deadline: no later than 7 calendar days after receiving the request for the standard organization determination
- Completed steps and their outputs: s3, s1
- Open decisions downstream: none
- Next steps: end of workflow

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 473.8 |
| Cycle time with agents (agent steps instant plus 2 min review) | 211.3 |
| Cycle time saved | 179.2 |
| Hands-on time saved (agent steps minus 2 min review each) | 14.9 |
