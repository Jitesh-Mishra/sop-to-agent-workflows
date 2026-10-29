# Automation opportunity: Simplified acquisition: award and documentation

Process family: **procure_to_pay** (mapped to Oracle Fusion Cloud ERP (Procurement, Payables)). Spec source: `gold`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Determine the price is fair and reasonable | contracting officer | **human** |  |  |
| s2 | Add a price reasonableness statement to the file | contracting officer | **agent** |  |  |
| s3 | Send minimum-order facts to the requiring activity to confirm or alter the requirement | contracting officer | **agent** |  | requiring activity |
| s4 | Document the final action in the file | contracting officer | **agent** |  |  |
| s5 | Notify unsuccessful suppliers | contracting officer | **agent** |  | unsuccessful suppliers |
| s6 | Explain the basis of a non-price award to the supplier | contracting officer | **agent** |  | supplier |
| s7 | Annotate the award copy with TIN and send to the payment office | contracting officer | **agent** |  | payment office |

- Agent steps: **6 of 7**; handoffs: **4**.

## Riskiest handoff: s1 (Determine the price is fair and reasonable) to contracting officer
Risk score 3: 2 open decision(s) downstream, a person must act.

Context the packet must carry:

- Instructions (source text): Before making award, the contracting officer must determine that the proposed price is fair and reasonable. Whenever possible, base price reasonableness on competitive quotations or offers.
- Deadline: none stated
- Completed steps and their outputs: none (first step)
- Open decisions downstream: Which applies: only one response?; Which applies: minimum order exceeds requirement?
- Next steps: s2, s3, s4

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 83.2 |
| Cycle time with agents (agent steps instant plus 2 min review) | 38.2 |
| Cycle time saved | 44.0 |
| Hands-on time saved (agent steps minus 2 min review each) | 44.0 |
