# Automation opportunity: Medicare Part D coverage determination

Process family: **prior_authorization** (mapped to Oracle Health (payer and provider prior authorization)). Spec source: `gold`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Make the coverage determination and notify within 72 hours | Part D plan sponsor | **human** |  | enrollee and prescriber |
| s2 | Decide whether to expedite | Part D plan sponsor | **human** |  |  |
| s3 | Make the expedited determination and notify within 24 hours | Part D plan sponsor | **human** |  | enrollee and prescriber |
| s4 | Send written notice of a favorable decision | Part D plan sponsor | **agent** |  | enrollee |
| s5 | Send the denial notice with reasons and redetermination rights | Part D plan sponsor | **agent** |  | enrollee |
| s6 | Forward the request to the IRE within 24 hours of a missed deadline | Part D plan sponsor | **agent** |  | IRE |

- Agent steps: **3 of 6**; handoffs: **5**.

## Riskiest handoff: s1 (Make the coverage determination and notify within 72 hours) to Part D plan sponsor
Risk score 6: deadline (no later than 72 hours after receipt of the request), 3 open decision(s) downstream, a person must act.

Context the packet must carry:

- Instructions (source text): When a party makes a request for a drug benefit, the Part D plan sponsor must notify the enrollee and the prescriber of its determination as expeditiously as the enrollee's health condition requires, but no later than 72 hours after receipt of the request.
- Deadline: no later than 72 hours after receipt of the request
- Completed steps and their outputs: s2
- Open decisions downstream: Which applies: favorable?; Which applies: denied?; Which applies: timeframe missed?
- Next steps: s4, s5, s6

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 83.2 |
| Cycle time with agents (agent steps instant plus 2 min review) | 68.1 |
| Cycle time saved | 14.9 |
| Hands-on time saved (agent steps minus 2 min review each) | 14.9 |
