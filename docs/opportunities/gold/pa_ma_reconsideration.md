# Automation opportunity: Medicare Advantage standard reconsideration of an adverse determination

Process family: **prior_authorization** (mapped to Oracle Health (payer and provider prior authorization)). Spec source: `gold`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | File a written reconsideration request within 60 days | party | **human** |  | MA organization |
| s2 | File a late request stating why it was late | party | **human** |  | MA organization |
| s3 | Issue a completely favorable reconsidered determination within 30 days | MA organization | **human** |  | enrollee |
| s4 | Send the written explanation and case file to the independent entity within 30 days | MA organization | **agent** |  | independent entity |
| s5 | Help gather and forward information to the independent entity | MA organization | **agent** |  | independent entity |

- Agent steps: **2 of 5**; handoffs: **5**.

## Riskiest handoff: s1 (File a written reconsideration request within 60 days) to party
Risk score 5: deadline (within 60 calendar days after receipt of the written organization determination notice), 2 open decision(s) downstream, a person must act.

Context the packet must carry:

- Instructions (source text): A party to an organization determination must ask for a reconsideration of the determination by making a written request to the MA organization that made the organization determination. A request for reconsideration must be filed within 60 calendar days after receipt of the written organization determination notice.
- Deadline: within 60 calendar days after receipt of the written organization determination notice
- Completed steps and their outputs: none (first step)
- Open decisions downstream: Which applies: completely favorable?; Which applies: adverse decision affirmed?
- Next steps: s3, s4

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 285.2 |
| Cycle time with agents (agent steps instant plus 2 min review) | 217.6 |
| Cycle time saved | 27.9 |
| Hands-on time saved (agent steps minus 2 min review each) | 26.0 |
