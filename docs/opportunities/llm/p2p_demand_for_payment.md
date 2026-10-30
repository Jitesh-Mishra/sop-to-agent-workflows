# Automation opportunity: Contract debts: demand for payment

Process family: **procure_to_pay** (mapped to Oracle Fusion Cloud ERP (Procurement, Payables)). Spec source: `llm (specs)`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Issue the demand for payment | contracting officer | **agent** | Compiling and drafting a demand for payment from known facts. | null |
| s2 | Issue the demand for payment | contracting officer | **human** | Needs a professional judgment and signature to issue the demand for payment. | null |
| s3 | Issue the demand for payment | contracting officer | **agent** | Compiling and sending a notice from known facts. | null |
| s4 | Include a description of the debt | contracting officer | **agent** | Compiling a description of the debt from known facts. | null |
| s5 | Issue the demand for payment | contracting officer | **agent** | Compiling and sending a demand for payment based on known facts. | null |
| s6 | Advise contractor to contact | contracting officer | **human** | Needs a professional judgment and communication. | contractor |
| s7 | Furnish a copy of the demand | contracting officer | **human** | Needs physical action such as sending a certified mail. | contractor |
| s8 | Forward a copy of the demand | contracting officer | **agent** | Compiling and forwarding a document. | payment office |

- Agent steps: **5 of 8**; handoffs: **8**.
- Agent flags that the (draft) gold labels confirm: **3 of 5**. Unconfirmed flags are where the model over-automates; treat them as candidates for review, not decisions.
- Agreement of these executor calls with the gold labels is scored in `reports/results.csv`.

## Riskiest handoff: s2 (Issue the demand for payment) to contracting officer
Risk score 1: a person must act.

Context the packet must carry:

- Instructions (source text): Issue the demand for payment even if the contractor has agreed to repay the debt.
- Deadline: none stated
- Completed steps and their outputs: s1
- Open decisions downstream: none
- Next steps: s4

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 183.4 |
| Cycle time with agents (agent steps instant plus 2 min review) | 108.3 |
| Cycle time saved | 74.2 |
| Hands-on time saved (agent steps minus 2 min review each) | 74.2 |
