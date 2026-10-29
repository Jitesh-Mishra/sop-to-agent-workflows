# Automation opportunity: Incident handling checklist

Process family: **incident_handling** (mapped to OCI security operations). Spec source: `gold`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Determine whether an incident occurred (indicators, correlation, research) | incident handler | **human** |  |  |
| s2 | Start documenting the investigation and gathering evidence | incident handler | **agent** |  |  |
| s3 | Prioritize the incident by impact and recoverability | incident handler | **human** |  |  |
| s4 | Report the incident to internal personnel and external organizations | incident handler | **agent** |  | internal personnel and external organizations |
| s5 | Acquire, preserve and document evidence | incident handler | **human** |  |  |
| s6 | Contain the incident | incident handler | **human** |  |  |
| s7 | Eradicate: mitigate exploited vulnerabilities and remove malware | incident handler | **human** |  |  |
| s8 | Repeat detection, containment and eradication for newly found hosts | incident handler | **human** |  |  |
| s9 | Return affected systems to operation | incident handler | **human** |  |  |
| s10 | Confirm systems are functioning normally | incident handler | **agent** |  |  |
| s11 | Write the follow-up report | incident handler | **agent** |  |  |
| s12 | Hold a lessons learned meeting | incident response team | **human** |  |  |

- Agent steps: **4 of 12**; handoffs: **1**.

## Riskiest handoff: s1 (Determine whether an incident occurred (indicators, correlation, research)) to incident handler
Risk score 2: 1 open decision(s) downstream, a person must act.

Context the packet must carry:

- Instructions (source text): Determine whether an incident has occurred: analyze the precursors and indicators, look for correlating information, and perform research (e.g., search engines, knowledge base).
- Deadline: none stated
- Completed steps and their outputs: none (first step)
- Open decisions downstream: Which applies: incident occurred?
- Next steps: s2

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 512.5 |
| Cycle time with agents (agent steps instant plus 2 min review) | 457.8 |
| Cycle time saved | 59.5 |
| Hands-on time saved (agent steps minus 2 min review each) | 59.5 |
