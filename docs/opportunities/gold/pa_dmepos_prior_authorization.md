# Automation opportunity: Prior authorization for DMEPOS items

Process family: **prior_authorization** (mapped to Oracle Health (payer and provider prior authorization)). Spec source: `gold`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Submit the request with order, records and supplier documentation before furnishing | supplier | **agent** |  | CMS or contractor |
| s2 | Review the request against Medicare rules | CMS contractor | **human** |  |  |
| s3 | Issue a provisional affirmation | CMS contractor | **agent** |  | requester |
| s4 | Issue a non-affirmation decision | CMS contractor | **agent** |  | requester |
| s5 | Resubmit the request | supplier | **agent** |  | CMS or contractor |
| s6 | Attach jeopardy documentation for expedited review | supplier | **agent** |  |  |

- Agent steps: **5 of 6**; handoffs: **4**.

## Riskiest handoff: s2 (Review the request against Medicare rules) to CMS contractor
Risk score 5: leaves the organisation (CMS contractor), 2 open decision(s) downstream, a person must act.

Context the packet must carry:

- Instructions (source text): After receipt of a prior authorization request, CMS or its contractor reviews the prior authorization request for compliance with applicable Medicare coverage, coding, and payment rules.
- Deadline: none stated
- Completed steps and their outputs: s1, s6
- Open decisions downstream: Which applies: rules met?; Which applies: rules not met?
- Next steps: s3, s4

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 357.1 |
| Cycle time with agents (agent steps instant plus 2 min review) | 41.0 |
| Cycle time saved | 319.9 |
| Hands-on time saved (agent steps minus 2 min review each) | 51.2 |
