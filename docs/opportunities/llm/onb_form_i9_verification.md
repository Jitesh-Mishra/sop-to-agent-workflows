# Automation opportunity: Employment eligibility verification (Form I-9)

Process family: **onboarding** (mapped to Oracle Fusion Cloud HCM (Onboarding, Benefits)). Spec source: `llm (specs)`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Ensure the individual properly completes section 1 of Form I-9 | employer | **human** | Needs a professional, clinical, legal or accountable judgment or decision (approve, deny, determine, accept, adjudicate). |  |
| s2 | Assist the individual if needed | someone | **human** | Needs physical interaction and understanding of the situation. | employer |
| s3 | Physically examine the documentation | employer | **human** | Needs physical access to the documentation. |  |
| s4 | Complete section 2 of Form I-9 | employer | **human** | Requires a professional judgment and signature. |  |
| s5 | Retain the Form I-9 for three years | employer | **agent** | Routine record keeping and retention. |  |
| s6 | Reverify if employment authorization expires | employer | **agent** | Compiling and checking information to determine if employment authorization has expired and re-verifying accordingly. |  |
| s7 | Provide notice prior to inspection | employer | **agent** | Compiling and sending a notice from known facts. |  |

- Agent steps: **3 of 7**; handoffs: **1**.
- Agent flags that the (draft) gold labels confirm: **1 of 3**. Unconfirmed flags are where the model over-automates; treat them as candidates for review, not decisions.
- Agreement of these executor calls with the gold labels is scored in `reports/results.csv`.

## Riskiest handoff: s3 (Physically examine the documentation) to employer
Risk score 3: deadline (Within three business days of the hire), a person must act.

Context the packet must carry:

- Instructions (source text): Within three business days of the hire, the employer must physically examine the documentation presented by the individual establishing identity and employment authorization and ensure that the documents presented appear to be genuine and to relate to the individual.
- Deadline: Within three business days of the hire
- Completed steps and their outputs: s1, s2
- Open decisions downstream: none
- Next steps: s4

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 578.2 |
| Cycle time with agents (agent steps instant plus 2 min review) | 533.1 |
| Cycle time saved | 45.4 |
| Hands-on time saved (agent steps minus 2 min review each) | 45.4 |
