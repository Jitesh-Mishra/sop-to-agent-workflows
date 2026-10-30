# Automation opportunity: Simplified acquisition: award and documentation

Process family: **procure_to_pay** (mapped to Oracle Fusion Cloud ERP (Procurement, Payables)). Spec source: `llm (specs)`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Determine price reasonableness | contracting officer | **human** | A professional judgment is required to determine price reasonableness. |  |
| s2 | Use competitive quotations | contracting officer | **agent** | Compiling and checking offers or quotations. |  |
| s3 | Include price reasonableness statement | contracting officer | **agent** | Compiling a statement based on known facts. | contract file |
| s4 | Inform requiring activity | contracting officer | **agent** | Informing the requiring activity requires compiling and communicating information, which an AI agent can do with system access. | requiring activity |
| s5 | Document final action | contracting officer | **agent** | Recording the final action in the file. | file |
| s6 | Keep documentation minimal | contracting officer | **agent** | Routine record keeping and documentation management. |  |
| s7 | Notify unsuccessful suppliers | contracting officer | **agent** | Compiling and sending a notice based on known facts and requests. | unsuccessful suppliers |
| s8 | Provide explanation | contracting officer | **agent** | Compiling a brief explanation from known factors. | payment office |
| s9 | Annotate oral solicitation | contracting officer | **agent** | Compiling and annotating information from the oral solicitation. | payment office |

- Agent steps: **8 of 9**; handoffs: **6**.
- Agent flags that the (draft) gold labels confirm: **6 of 8**. Unconfirmed flags are where the model over-automates; treat them as candidates for review, not decisions.
- Agreement of these executor calls with the gold labels is scored in `reports/results.csv`.

## Riskiest handoff: s7 (Notify unsuccessful suppliers) to unsuccessful suppliers
Risk score 2: leaves the organisation (unsuccessful suppliers).

Context the packet must carry:

- Instructions (source text): Notification to unsuccessful suppliers shall be given only if requested or required.
- Deadline: none stated
- Completed steps and their outputs: s1, s2, s3, s4, s5, s8, s9
- Open decisions downstream: none
- Next steps: s6

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 167.5 |
| Cycle time with agents (agent steps instant plus 2 min review) | 49.5 |
| Cycle time saved | 118.5 |
| Hands-on time saved (agent steps minus 2 min review each) | 118.5 |
