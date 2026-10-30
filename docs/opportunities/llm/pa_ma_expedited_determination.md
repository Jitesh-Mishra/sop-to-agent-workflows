# Automation opportunity: Medicare Advantage expedited organization determination

Process family: **prior_authorization** (mapped to Oracle Health (payer and provider prior authorization)). Spec source: `llm (specs)`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Submit a request | enrollee or physician | **agent** | Drafting and sending a request from known facts. |  |
| s2 | Document oral requests | MA organization | **agent** | Recording and maintaining documentation is an information work that an AI agent can do. |  |
| s3 | Promptly decide | MA organization | **agent** | Routine decision making. |  |
| s4 | Provide expedited determination | MA organization | **agent** | Compiling and forwarding a determination based on physician's input. | enrollee |
| s5 | Deny request and transfer | MA organization | **agent** | Automatically transferring a request to a standard organization determination is an information work an AI agent can do. | enrollee |
| s6 | Give oral notice | MA organization | **human** | Needs physical action (oral notice) and subsequent written documentation. | enrollee |
| s7 | Request medical information | MA organization | **agent** | Searching and correlating information. |  |
| s8 | Make expedited determination | MA organization | **agent** | Routine record keeping. | enrollee |
| s9 | Notify of adverse determination | MA organization | **human** | Needs hands-on communication and attestation. | enrollee |

- Agent steps: **7 of 9**; handoffs: **5**.
- Agent flags that the (draft) gold labels confirm: **3 of 7**. Unconfirmed flags are where the model over-automates; treat them as candidates for review, not decisions.
- Agreement of these executor calls with the gold labels is scored in `reports/results.csv`.

## Riskiest handoff: s8 (Make expedited determination) to enrollee
Risk score 4: deadline (no later than 72 hours after receiving the request), leaves the organisation (enrollee).

Context the packet must carry:

- Instructions (source text): An MA organization that approves a request for expedited determination must make its determination and notify the enrollee of its decision no later than 72 hours after receiving the request.
- Deadline: no later than 72 hours after receiving the request
- Completed steps and their outputs: s1, s2, s3, s4, s6, s7
- Open decisions downstream: none
- Next steps: s9

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 290.6 |
| Cycle time with agents (agent steps instant plus 2 min review) | 78.4 |
| Cycle time saved | 213.0 |
| Hands-on time saved (agent steps minus 2 min review each) | 79.6 |
