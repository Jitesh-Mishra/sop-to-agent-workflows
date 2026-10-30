# Automation opportunity: High-priority ticket escalation (authored)

Process family: **support_escalation** (mapped to Oracle Support / Fusion Service). Spec source: `gold`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Confirm priority and queue within 1 hour | support agent | **human** |  |  |
| s2 | Notify the on-call engineer and open an incident | support agent | **agent** |  | on-call engineer |
| s3 | Acknowledge the incident and post a status update | on-call engineer | **human** |  | customer |
| s4 | Forward the ticket with account details to billing | support agent | **agent** |  | billing team |
| s5 | Send the customer an acknowledgement with the next update time | support agent | **agent** |  | customer |
| s6 | Document the fix in the knowledge base and close the ticket | owning team | **human** |  |  |

- Agent steps: **3 of 6**; handoffs: **4**.

## Riskiest handoff: s1 (Confirm priority and queue within 1 hour) to support agent
Risk score 5: deadline (within 1 hour of arrival), 2 open decision(s) downstream, a person must act.

Context the packet must carry:

- Instructions (source text): The support agent confirms the priority and the queue within 1 hour of arrival.
- Deadline: within 1 hour of arrival
- Completed steps and their outputs: none (first step)
- Open decisions downstream: Which applies: service outage?; Which applies: billing or payment error?
- Next steps: s2, s4, s5

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 567.0 |
| Cycle time with agents (agent steps instant plus 2 min review) | 403.0 |
| Cycle time saved | 46.3 |
| Hands-on time saved (agent steps minus 2 min review each) | 28.6 |
