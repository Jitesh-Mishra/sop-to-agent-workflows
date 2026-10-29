# Automation opportunity: Medicare Advantage expedited organization determination

Process family: **prior_authorization** (mapped to Oracle Health (payer and provider prior authorization)). Spec source: `gold`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Request an expedited determination | enrollee or physician | **human** |  | MA organization |
| s2 | Document the oral request in the case file | MA organization | **agent** |  |  |
| s3 | Decide whether to expedite | MA organization | **human** |  |  |
| s4 | Transfer the request to a standard determination | MA organization | **agent** |  |  |
| s5 | Give oral notice and a written letter within 3 days explaining the denial of expedite | MA organization | **agent** |  | enrollee |
| s6 | Request medical information from noncontract providers within 24 hours | MA organization | **agent** |  | noncontract providers |
| s7 | Make the determination and notify within 72 hours | MA organization | **human** |  | enrollee |
| s8 | Mail written confirmation of an oral adverse decision within 3 days | MA organization | **agent** |  | enrollee |

- Agent steps: **5 of 8**; handoffs: **5**.

## Riskiest handoff: s1 (Request an expedited determination) to enrollee or physician
Risk score 4: leaves the organisation (enrollee or physician), 1 open decision(s) downstream, a person must act.

Context the packet must carry:

- Instructions (source text): An enrollee or a physician may request that an MA organization expedite an organization determination by submitting an oral or written request directly to the MA organization.
- Deadline: none stated
- Completed steps and their outputs: none (first step)
- Open decisions downstream: Which applies: oral request?
- Next steps: s2, s3

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 275.5 |
| Cycle time with agents (agent steps instant plus 2 min review) | 276.7 |
| Cycle time saved | 25.9 |
| Hands-on time saved (agent steps minus 2 min review each) | 38.8 |
