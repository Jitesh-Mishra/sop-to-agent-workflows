# Automation opportunity: New employee health benefits enrollment (FEHB)

Process family: **onboarding** (mapped to Oracle Fusion Cloud HCM (Onboarding, Benefits)). Spec source: `gold`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Elect to enroll or not within 60 days | employee | **human** |  | employing office |
| s2 | Set the enrollment effective date | employing office | **agent** |  |  |
| s3 | Determine belated-enrollment eligibility and advise the employee | employing office | **human** |  | employee |

- Agent steps: **1 of 3**; handoffs: **2**.

## Riskiest handoff: s1 (Elect to enroll or not within 60 days) to employee
Risk score 4: deadline (within 60 days after becoming eligible), 1 open decision(s) downstream, a person must act.

Context the packet must carry:

- Instructions (source text): An employee who becomes eligible may elect to enroll or not to enroll within 60 days after becoming eligible.
- Deadline: within 60 days after becoming eligible
- Completed steps and their outputs: none (first step)
- Open decisions downstream: Which applies: employee enrolls?
- Next steps: s2

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 226.3 |
| Cycle time with agents (agent steps instant plus 2 min review) | 211.3 |
| Cycle time saved | 14.9 |
| Hands-on time saved (agent steps minus 2 min review each) | 14.9 |
