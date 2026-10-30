# Automation opportunity: Contract debts: demand for payment

Process family: **procure_to_pay** (mapped to Oracle Fusion Cloud ERP (Procurement, Payables)). Spec source: `gold`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Determine the debt and amount and issue a demand | contracting officer | **human** |  |  |
| s2 | Prepare the demand with debt, accounting lines, interest and dispute contact | contracting officer | **agent** |  |  |
| s3 | Provide the accounting distribution by the stated date | contracting officer | **agent** |  |  |
| s4 | Send the demand to the contractor by certified mail | contracting officer | **agent** |  | contractor |
| s5 | Forward a copy of the demand to the payment office | contracting officer | **agent** |  | payment office |
| s6 | Request installment payments or deferment | contractor | **human** |  | contracting officer |

- Agent steps: **4 of 6**; handoffs: **3**.

## Riskiest handoff: s4 (Send the demand to the contractor by certified mail) to contractor
Risk score 3: leaves the organisation (contractor), 1 open decision(s) downstream.

Context the packet must carry:

- Instructions (source text): The contracting officer shall furnish a copy of the demand for payment to the contractor by certified mail, return receipt requested, or by any other method that provides evidence of receipt.
- Deadline: none stated
- Completed steps and their outputs: s1, s2, s3
- Open decisions downstream: Which applies: payment not practicable or amount disputed?
- Next steps: s5, s6

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 317.9 |
| Cycle time with agents (agent steps instant plus 2 min review) | 257.6 |
| Cycle time saved | 59.0 |
| Hands-on time saved (agent steps minus 2 min review each) | 59.0 |
