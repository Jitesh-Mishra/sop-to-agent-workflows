# Automation opportunity: Federal incident coordination with CISA

Process family: **incident_handling** (mapped to OCI security operations). Spec source: `llm (specs)`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Notify CISA | agency | **agent** | Compiling and sending a notice based on known facts and directives. | CISA |
| s2 | Notify Congressional Committees, OIG, and OFCIO | agency | **human** | Needs hands-on communication and potentially legal/official attestation. |  |
| s3 | Provide tracking number and risk rating | CISA | **agent** | Compiling and providing a tracking number and risk rating based on known facts. | agency |
| s4 | Share log data, cyber threat indicators, and defensive measures | agency | **agent** | Compiling and sharing information. | CISA and sharing partners |
| s5 | Share cyber intelligence | CISA | **agent** | Compiling and sharing information from known sources. | intelligence community and law enforcement |
| s6 | Report incidents to federal law enforcement | agency | **human** | Requires a professional judgment and communication with external parties. |  |
| s7 | Determine C-UCG escalation | CISA or FBI | **human** | Requires a professional judgment and decision. |  |
| s8 | Provide post-incident updates and final report | agency | **agent** | Routine documentation and reporting. | CISA |
| s9 | Provide incident response checklists and report | agency | **agent** | Generating and providing checklists and reports is an information work that an AI agent can do with system access. |  |
| s10 | Evaluate materials and close ticket | CISA | **agent** | Classifying or routing based on evaluation of materials. |  |

- Agent steps: **7 of 10**; handoffs: **5**.
- Agent flags that the (draft) gold labels confirm: **5 of 7**. Unconfirmed flags are where the model over-automates; treat them as candidates for review, not decisions.
- Agreement of these executor calls with the gold labels is scored in `reports/results.csv`.

## Riskiest handoff: s1 (Notify CISA) to CISA
Risk score 4: deadline (within 1 hour of incident determination as directed by OMB M-20-04), leaves the organisation (CISA).

Context the packet must carry:

- Instructions (source text): The agency notifies CISA within 1 hour of incident determination as directed by OMB M-20-04.
- Deadline: within 1 hour of incident determination as directed by OMB M-20-04
- Completed steps and their outputs: none (first step)
- Open decisions downstream: none
- Next steps: s3, s2

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 1852.4 |
| Cycle time with agents (agent steps instant plus 2 min review) | 300.8 |
| Cycle time saved | 1555.6 |
| Hands-on time saved (agent steps minus 2 min review each) | 101.6 |
