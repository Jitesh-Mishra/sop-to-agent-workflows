# Automation opportunity: Federal incident coordination with CISA

Process family: **incident_handling** (mapped to OCI security operations). Spec source: `gold`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Notify CISA within 1 hour of incident determination | agency | **agent** |  | CISA |
| s2 | Notify Congressional Committees, OIG and OMB OFCIO | agency | **agent** |  | Congress, OIG and OMB |
| s3 | Issue a tracking number and NCISS risk rating | CISA | **agent** |  | agency |
| s4 | Share logs, indicators and defensive measures | agency | **agent** |  | CISA and sharing partners |
| s5 | Share coordinated cyber intelligence | CISA | **human** |  | involved organizations |
| s6 | Report to federal law enforcement | agency | **human** |  | federal law enforcement |
| s7 | Decide whether to escalate to a Cyber UCG | CISA or FBI | **human** |  |  |
| s8 | Send post-incident updates and the final incident report | agency | **agent** |  | CISA |
| s9 | Submit completed checklists and incident report to close the ticket | agency | **agent** |  | CISA |
| s10 | Evaluate and close the ticket or request more actions | CISA | **human** |  | agency |

- Agent steps: **6 of 10**; handoffs: **9**.

## Riskiest handoff: s1 (Notify CISA within 1 hour of incident determination) to CISA
Risk score 5: deadline (within 1 hour of incident determination as directed by OMB M-20-04), leaves the organisation (CISA), 1 open decision(s) downstream.

Context the packet must carry:

- Instructions (source text): The agency notifies CISA within 1 hour of incident determination as directed by OMB M-20-04.
- Deadline: within 1 hour of incident determination as directed by OMB M-20-04
- Completed steps and their outputs: none (first step)
- Open decisions downstream: Which applies: where applicable?
- Next steps: s2, s3

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 1875.0 |
| Cycle time with agents (agent steps instant plus 2 min review) | 800.5 |
| Cycle time saved | 1049.5 |
| Hands-on time saved (agent steps minus 2 min review each) | 87.0 |
