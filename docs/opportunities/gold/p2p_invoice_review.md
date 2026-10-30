# Automation opportunity: Invoice receipt, review and payment

Process family: **procure_to_pay** (mapped to Oracle Fusion Cloud ERP (Procurement, Payables)). Spec source: `gold`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Stamp the actual receipt date on the invoice and receiving report | payment office | **agent** |  |  |
| s2 | Review the invoice for all required elements | agency office | **agent** |  |  |
| s3 | Return the improper invoice within 7 days listing every defect | agency office | **agent** |  | vendor |
| s4 | Match the payment to a receiving report authorizing payment | payment office | **agent** |  |  |
| s5 | Pay late-payment interest automatically | payment office | **agent** |  |  |

- Agent steps: **5 of 5**; handoffs: **1**.

## Riskiest handoff: s3 (Return the improper invoice within 7 days listing every defect) to vendor
Risk score 4: deadline (no later than 7 days after receipt), leaves the organisation (vendor).

Context the packet must carry:

- Instructions (source text): When an invoice is determined to be improper, the agency shall return the invoice to the vendor as soon as practicable after receipt, but no later than 7 days after receipt. The agency will identify all defects that prevent payment and specify all reasons why the invoice is not proper and why it is being returned.
- Deadline: no later than 7 days after receipt
- Completed steps and their outputs: s1, s2
- Open decisions downstream: none
- Next steps: end of workflow

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 292.1 |
| Cycle time with agents (agent steps instant plus 2 min review) | 6.0 |
| Cycle time saved | 285.1 |
| Hands-on time saved (agent steps minus 2 min review each) | 51.0 |
