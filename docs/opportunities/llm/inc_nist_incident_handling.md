# Automation opportunity: Incident handling checklist

Process family: **incident_handling** (mapped to OCI security operations). Spec source: `llm (specs)`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Determine if an incident has occurred | handler | **agent** | Information work an AI agent with system access could do: searching and correlating information. |  |
| s2 | Document the investigation and gather evidence | handler | **agent** | Information work an AI agent with system access could do: drafting and sending a notice from known facts, compiling, checking or forwarding documents, recording, logging or tracking, searching and correlating information, classifying or routing. |  |
| s3 | Prioritize handling | handler | **agent** | Compiling and prioritizing based on known factors. |  |
| s4 | Report incident | handler | **human** | Needs hands-on communication and coordination with internal and external parties. | internal personnel and external organizations |
| s5 | Acquire, preserve, secure, and document evidence | handler | **agent** | Information work an AI agent with system access could do. |  |
| s6 | Contain the incident | handler | **human** | Needs hands-on action to contain the incident. |  |
| s7 | Eradicate the incident | handler | **agent** | Eradicating the incident involves information work such as identifying and mitigating vulnerabilities, which an AI agent with system access can do. |  |
| s8 | Repeat detection and analysis | handler | **agent** | Repeating detection and analysis is an information work that an AI agent with system access could do. |  |
| s9 | Recover from the incident | handler | **agent** | Recovering from an incident is typically an automated process for an AI agent with system access. |  |
| s10 | Confirm affected systems are functioning normally | handler | **agent** | Checking and confirming system status is an information work an AI agent can do. |  |
| s11 | Create a follow-up report | handler | **agent** | Routine report creation. |  |
| s12 | Hold a lessons learned meeting | handler | **agent** | Routine meeting recording and documentation. |  |

- Agent steps: **10 of 12**; handoffs: **1**.
- Agent flags that the (draft) gold labels confirm: **3 of 10**. Unconfirmed flags are where the model over-automates; treat them as candidates for review, not decisions.
- Agreement of these executor calls with the gold labels is scored in `reports/results.csv`.

## Riskiest handoff: s4 (Report incident) to handler
Risk score 1: a person must act.

Context the packet must carry:

- Instructions (source text): Report the incident to the appropriate internal personnel and external organizations.
- Deadline: none stated
- Completed steps and their outputs: s1, s2, s3
- Open decisions downstream: none
- Next steps: s5

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 232.7 |
| Cycle time with agents (agent steps instant plus 2 min review) | 88.5 |
| Cycle time saved | 145.2 |
| Hands-on time saved (agent steps minus 2 min review each) | 145.2 |
