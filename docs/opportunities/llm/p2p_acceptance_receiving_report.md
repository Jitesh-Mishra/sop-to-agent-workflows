# Automation opportunity: Acceptance of supplies or services and the receiving report

Process family: **procure_to_pay** (mapped to Oracle Fusion Cloud ERP (Procurement, Payables)). Spec source: `llm (specs)`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Acknowledge conformity | contracting officer | **human** | A professional judgment and attestation is required. |  |
| s2 | Wait for QA | contracting officer | **human** | Needs presence to wait for QA results and make a decision. |  |
| s3 | Accept responsibility | contracting officer | **human** | A professional judgment and attestation. |  |
| s4 | Assign to office | contracting officer | **human** | A professional judgment and acceptance is required. | cognizant contract administration office |
| s5 | Evidence acceptance | contracting officer | **human** | Needs physical action such as signing or attesting to the certificate. |  |
| s6 | Include contract info | contracting officer | **human** | Needs a signature, attestation or certification from a designated Government official. |  |
| s7 | Forward report | agency receiving official | **agent** | Compiling and forwarding documents. | designated payment office |

- Agent steps: **1 of 7**; handoffs: **2**.
- Agent flags that the (draft) gold labels confirm: **1 of 1**. Unconfirmed flags are where the model over-automates; treat them as candidates for review, not decisions.
- Agreement of these executor calls with the gold labels is scored in `reports/results.csv`.

## Riskiest handoff: s1 (Acknowledge conformity) to contracting officer
Risk score 1: a person must act.

Context the packet must carry:

- Instructions (source text): Acceptance constitutes acknowledgment that the supplies or services conform with applicable contract quality and quantity requirements.
- Deadline: none stated
- Completed steps and their outputs: none (first step)
- Open decisions downstream: none
- Next steps: s2

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 360.3 |
| Cycle time with agents (agent steps instant plus 2 min review) | 201.9 |
| Cycle time saved | 161.3 |
| Hands-on time saved (agent steps minus 2 min review each) | 14.7 |
