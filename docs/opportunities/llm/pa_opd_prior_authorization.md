# Automation opportunity: Prior authorization for hospital outpatient department services

Process family: **prior_authorization** (mapped to Oracle Health (payer and provider prior authorization)). Spec source: `llm (specs)`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Submit a prior authorization request | provider | **agent** | Submitting a request is information work an AI agent can do with system access. | CMS or its contractor |
| s2 | Include all necessary documentation | provider | **agent** | Compiling and checking documents. |  |
| s3 | Submit before service and claim | provider | **agent** | Submitting a claim based on known facts. |  |
| s4 | Review by CMS or contractor | CMS or contractor | **agent** | Searching and correlating information to determine compliance with rules. |  |
| s5 | Affirmation or non-affirmation | CMS or contractor | **agent** | Checking and issuing a provisional affirmation or non-affirmation based on known rules and facts. | provider |
| s6 | Expedited review | CMS or contractor | **agent** | Routine information work such as completing an expedited review. |  |
| s7 | Resubmit upon non-affirmation | provider | **agent** | Resubmitting a request is an information work that an AI agent can automate. |  |

- Agent steps: **7 of 7**; handoffs: **2**.
- Agent flags that the (draft) gold labels confirm: **2 of 7**. Unconfirmed flags are where the model over-automates; treat them as candidates for review, not decisions.
- Agreement of these executor calls with the gold labels is scored in `reports/results.csv`.

## Riskiest handoff: s5 (Affirmation or non-affirmation) to provider
Risk score 6: deadline (within 7 calendar days of receipt of the request), leaves the organisation (provider), 2 open decision(s) downstream.

Context the packet must carry:

- Instructions (source text): CMS or its contractor will issue a provisional affirmation to the provider if the rules are met, or a non-affirmation if they are not met, within 7 calendar days of receipt of the request.
- Deadline: within 7 calendar days of receipt of the request
- Completed steps and their outputs: s1, s2, s3, s4
- Open decisions downstream: Which applies: non-affirmation?; Which applies: affirmation?
- Next steps: s6, s7

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 484.3 |
| Cycle time with agents (agent steps instant plus 2 min review) | 14.0 |
| Cycle time saved | 471.3 |
| Hands-on time saved (agent steps minus 2 min review each) | 95.4 |
