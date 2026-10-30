# Automation opportunity: Support ticket triage and auto-reply gate (authored)

Process family: **support_escalation** (mapped to Oracle Support / Fusion Service). Spec source: `llm (specs)`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Classify ticket into support queues and predict priority | system | **agent** | Information work an AI agent with system access could do: searching and correlating information, classifying or routing. |  |
| s2 | Retrieve similar resolved tickets and knowledge base articles | system | **agent** | Searching and correlating information. |  |
| s3 | Draft a reply | system | **agent** | Information work an AI agent with system access could do: drafting a reply. |  |
| s4 | Escalate ticket to support engineer | system | **agent** | Escalation to a support engineer is an information work that an AI agent can do. | support engineer |
| s5 | Send draft to support agent for approval | system | **agent** | Compiling and forwarding documents for review. | support agent |
| s6 | Support agent approves, edits, or rewrites draft | support agent | **agent** | AI agent can support agent in drafting and editing tasks. |  |
| s7 | Send reply to customer automatically | system | **agent** | Automated drafting and sending of a reply from known facts. | customer |
| s8 | Record gate decision and reasons | system | **agent** | Classifying or routing the gate decision and reasons. |  |

- Agent steps: **8 of 8**; handoffs: **3**.
- Agent flags that the (draft) gold labels confirm: **7 of 8**. Unconfirmed flags are where the model over-automates; treat them as candidates for review, not decisions.
- Agreement of these executor calls with the gold labels is scored in `reports/results.csv`.

## Riskiest handoff: s5 (Send draft to support agent for approval) to support agent
Risk score 2: 2 open decision(s) downstream.

Context the packet must carry:

- Instructions (source text): If route confidence is below 0.6, the predicted priority is high, or retrieval similarity is below 0.5, send the draft to a support agent for approval.
- Deadline: none stated
- Completed steps and their outputs: s1, s2, s3
- Open decisions downstream: Which applies: route confidence below 0.6 or retrieval similarity below 0.5?; Which applies: validation check passes?
- Next steps: s6, s7, s8

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 93.6 |
| Cycle time with agents (agent steps instant plus 2 min review) | 10.0 |
| Cycle time saved | 83.3 |
| Hands-on time saved (agent steps minus 2 min review each) | 79.6 |
