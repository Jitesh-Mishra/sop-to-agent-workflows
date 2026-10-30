# Automation opportunity: High-priority ticket escalation (authored)

Process family: **support_escalation** (mapped to Oracle Support / Fusion Service). Spec source: `llm (specs)`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Confirm priority and queue | support agent | **agent** | Searching and correlating information to confirm priority and queue. |  |
| s2 | Notify on-call engineer | support agent | **agent** | Compiling and forwarding the priority and queue information to the on-call engineer. | on-call engineer |
| s3 | Open incident | on-call engineer | **agent** | Compiling and checking information to open an incident. |  |
| s4 | Post status update | on-call engineer | **agent** | Posting a status update is information work an AI agent can do. |  |
| s5 | Forward ticket to billing team | support agent | **agent** | Compiling and forwarding documents. | billing team |
| s6 | Send acknowledgement | support agent | **agent** | Sending a notice from known facts. | customer |
| s7 | Document fix in knowledge base | owning team | **agent** | Routine record keeping. |  |
| s8 | Close ticket | owning team | **agent** | Routine record keeping and ticket closure. |  |

- Agent steps: **8 of 8**; handoffs: **3**.
- Agent flags that the (draft) gold labels confirm: **3 of 8**. Unconfirmed flags are where the model over-automates; treat them as candidates for review, not decisions.
- Agreement of these executor calls with the gold labels is scored in `reports/results.csv`.

## Riskiest handoff: s2 (Notify on-call engineer) to on-call engineer
Risk score 4: deadline (within 1 hour of arrival), 2 open decision(s) downstream.

Context the packet must carry:

- Instructions (source text): The support agent confirms the priority and the queue within 1 hour of arrival.
- Deadline: within 1 hour of arrival
- Completed steps and their outputs: s1
- Open decisions downstream: Which applies: ticket reports a service outage?; Which applies: ticket reports a service outage?
- Next steps: s3, s6

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 504.0 |
| Cycle time with agents (agent steps instant plus 2 min review) | 14.0 |
| Cycle time saved | 491.0 |
| Hands-on time saved (agent steps minus 2 min review each) | 96.8 |
