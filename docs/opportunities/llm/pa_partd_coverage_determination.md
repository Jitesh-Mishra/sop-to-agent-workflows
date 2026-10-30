# Automation opportunity: Medicare Part D coverage determination

Process family: **prior_authorization** (mapped to Oracle Health (payer and provider prior authorization)). Spec source: `llm (specs)`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Notify the enrollee and prescriber | Part D plan sponsor | **agent** | Compiling and sending a notice from known facts. | enrollee |
| s2 | Provide an expedited determination | Part D plan sponsor | **human** | Requires a professional judgment and decision. | enrollee |
| s3 | Make a completely favorable decision | Part D plan sponsor | **human** | A professional judgment and decision is required. | enrollee |
| s4 | Give written notice | Part D plan sponsor | **human** | Needs a physical action (signature, attestation) and a conversation (interview or counseling). | enrollee |
| s5 | Inform of right to redetermination | Part D plan sponsor | **human** | Needs a professional judgment and communication to the enrollee. | enrollee |
| s6 | Forward the request to IRE | Part D plan sponsor | **agent** | Compiling and forwarding the request based on known facts. | IRE |

- Agent steps: **2 of 6**; handoffs: **6**.
- Agent flags that the (draft) gold labels confirm: **1 of 2**. Unconfirmed flags are where the model over-automates; treat them as candidates for review, not decisions.
- Agreement of these executor calls with the gold labels is scored in `reports/results.csv`.

## Riskiest handoff: s1 (Notify the enrollee and prescriber) to enrollee
Risk score 6: deadline (no later than 72 hours after receipt of the request), leaves the organisation (enrollee), 2 open decision(s) downstream.

Context the packet must carry:

- Instructions (source text): When a party makes a request for a drug benefit, the Part D plan sponsor must notify the enrollee and the prescriber of its determination as expeditiously as the enrollee's health condition requires, but no later than 72 hours after receipt of the request.
- Deadline: no later than 72 hours after receipt of the request
- Completed steps and their outputs: none (first step)
- Open decisions downstream: Which applies: request is expedited?; Which applies: request is not expedited?
- Next steps: s2, s3, s4

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 145.7 |
| Cycle time with agents (agent steps instant plus 2 min review) | 121.8 |
| Cycle time saved | 21.4 |
| Hands-on time saved (agent steps minus 2 min review each) | 21.4 |
