# Automation opportunity: Prior authorization for hospital outpatient department services

Process family: **prior_authorization** (mapped to Oracle Health (payer and provider prior authorization)). Spec source: `gold`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Submit the prior authorization request with documentation before service | provider | **agent** |  | CMS or contractor |
| s2 | Review the request against coverage, coding and payment rules | CMS contractor | **human** |  |  |
| s3 | Issue provisional affirmation or non-affirmation within 7 days | CMS contractor | **agent** |  | provider |
| s4 | Complete an expedited review within 2 business days | CMS contractor | **human** |  |  |
| s5 | Resubmit the request | provider | **agent** |  | CMS or contractor |

- Agent steps: **3 of 5**; handoffs: **3**.

## Riskiest handoff: s4 (Complete an expedited review within 2 business days) to CMS contractor
Risk score 5: deadline (within 2 business days), leaves the organisation (CMS contractor), a person must act.

Context the packet must carry:

- Instructions (source text): Upon receipt of a request for expedited review, CMS or its contractor will complete an expedited review if a delay could seriously jeopardize the beneficiary's life, health, or ability to regain maximum function, and issue a decision within 2 business days.
- Deadline: within 2 business days
- Completed steps and their outputs: s1
- Open decisions downstream: none
- Next steps: s3

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 506.2 |
| Cycle time with agents (agent steps instant plus 2 min review) | 37.6 |
| Cycle time saved | 466.2 |
| Hands-on time saved (agent steps minus 2 min review each) | 46.0 |
