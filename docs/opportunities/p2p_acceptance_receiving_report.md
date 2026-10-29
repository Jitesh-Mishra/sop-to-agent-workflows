# Automation opportunity: Acceptance of supplies or services and the receiving report

Process family: **procure_to_pay** (mapped to Oracle Fusion Cloud ERP (Procurement, Payables)). Spec source: `gold`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Accept the supplies or services | contracting officer | **human** |  |  |
| s2 | Sign the acceptance certificate on the receiving report | designated Government official | **human** |  |  |
| s3 | Forward the receiving report to the payment office by the 5th working day | agency receiving official | **agent** |  | payment office |

- Agent steps: **1 of 3**; handoffs: **1**.

## Riskiest handoff: s1 (Accept the supplies or services) to contracting officer
Risk score 1: a person must act.

Context the packet must carry:

- Instructions (source text): Acceptance of supplies or services is the responsibility of the contracting officer.
- Deadline: none stated
- Completed steps and their outputs: none (first step)
- Open decisions downstream: none
- Next steps: s2

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 473.8 |
| Cycle time with agents (agent steps instant plus 2 min review) | 211.3 |
| Cycle time saved | 179.2 |
| Hands-on time saved (agent steps minus 2 min review each) | 14.9 |
