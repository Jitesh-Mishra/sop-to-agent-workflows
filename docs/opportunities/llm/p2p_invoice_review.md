# Automation opportunity: Invoice receipt, review and payment

Process family: **procure_to_pay** (mapped to Oracle Fusion Cloud ERP (Procurement, Payables)). Spec source: `llm (specs)`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Payment based on proper invoice and contract performance | designated payment office | **agent** | AI can check and forward invoices and correlate contract performance. |  |
| s2 | Annotate invoice date | designated payment office | **agent** | Compiling and annotating dates from known invoice and receiving report details. |  |
| s3 | Review invoice | designated agency office | **agent** | Routine invoice review. |  |
| s4 | Invoice includes required elements | designated agency office | **agent** | Compiling and checking if the invoice includes required elements. |  |
| s5 | Return improper invoice | designated agency office | **agent** | Compiling and forwarding documents. | vendor |
| s6 | Identify defects and specify reasons | designated agency office | **agent** | Searching and correlating information to identify defects and specify reasons. |  |
| s7 | Support invoice payment with receiving report | designated agency office | **agent** | Compiling and checking documents. |  |
| s8 | Pay interest for late payments | designated agency office | **agent** | Routine payment processing. |  |

- Agent steps: **8 of 8**; handoffs: **1**.
- Agent flags that the (draft) gold labels confirm: **5 of 8**. Unconfirmed flags are where the model over-automates; treat them as candidates for review, not decisions.
- Agreement of these executor calls with the gold labels is scored in `reports/results.csv`.

## Riskiest handoff: s5 (Return improper invoice) to vendor
Risk score 4: deadline (no later than 7 days after receipt), leaves the organisation (vendor).

Context the packet must carry:

- Instructions (source text): When an invoice is determined to be improper, the agency shall return the invoice to the vendor as soon as practicable after receipt, but no later than 7 days after receipt.
- Deadline: no later than 7 days after receipt
- Completed steps and their outputs: s1, s2, s3, s4
- Open decisions downstream: none
- Next steps: s6

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 283.0 |
| Cycle time with agents (agent steps instant plus 2 min review) | 16.0 |
| Cycle time saved | 267.0 |
| Hands-on time saved (agent steps minus 2 min review each) | 112.2 |
