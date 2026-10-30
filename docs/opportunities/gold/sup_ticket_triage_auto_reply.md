# Automation opportunity: Support ticket triage and auto-reply gate (authored)

Process family: **support_escalation** (mapped to Oracle Support / Fusion Service). Spec source: `gold`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Classify the ticket queue and priority | support agent system | **agent** |  |  |
| s2 | Retrieve similar resolved tickets and KB articles | support agent system | **agent** |  |  |
| s3 | Draft a grounded reply | support agent system | **agent** |  |  |
| s4 | Escalate to a support engineer with the run trace | support agent system | **agent** |  | support engineer |
| s5 | Send the draft to a support agent for approval | support agent system | **agent** |  | support agent |
| s6 | Approve, edit or rewrite the draft and send it | support agent | **human** |  | customer |
| s7 | Send the reply to the customer automatically | support agent system | **agent** |  | customer |
| s8 | Record the gate decision and reasons in the trace | support agent system | **agent** |  |  |

- Agent steps: **7 of 8**; handoffs: **4**.

## Riskiest handoff: s7 (Send the reply to the customer automatically) to customer
Risk score 2: leaves the organisation (customer).

Context the packet must carry:

- Instructions (source text): If all checks pass, send the reply to the customer automatically.
- Deadline: none stated
- Completed steps and their outputs: s1, s2, s3
- Open decisions downstream: none
- Next steps: s8

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 90.9 |
| Cycle time with agents (agent steps instant plus 2 min review) | 10.0 |
| Cycle time saved | 80.9 |
| Hands-on time saved (agent steps minus 2 min review each) | 73.5 |
