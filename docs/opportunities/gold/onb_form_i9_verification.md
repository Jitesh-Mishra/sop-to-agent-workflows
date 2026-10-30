# Automation opportunity: Employment eligibility verification (Form I-9)

Process family: **onboarding** (mapped to Oracle Fusion Cloud HCM (Onboarding, Benefits)). Spec source: `gold`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Complete and sign Form I-9 section 1 at hire | employee | **human** |  |  |
| s2 | Physically examine identity and work authorization documents within 3 business days | employer | **human** |  |  |
| s3 | Complete and sign Form I-9 section 2 within 3 business days | employer | **human** |  |  |
| s4 | Retain the Form I-9 for the required period | employer | **agent** |  |  |
| s5 | Reverify work authorization before it expires | employer | **human** |  |  |

- Agent steps: **1 of 5**; handoffs: **0**.

## Riskiest handoff: s2 (Physically examine identity and work authorization documents within 3 business days) to employer
Risk score 3: deadline (Within three business days of the hire), a person must act.

Context the packet must carry:

- Instructions (source text): Within three business days of the hire, the employer must physically examine the documentation presented by the individual establishing identity and employment authorization and ensure that the documents presented appear to be genuine and to relate to the individual.
- Deadline: Within three business days of the hire
- Completed steps and their outputs: s1
- Open decisions downstream: none
- Next steps: s3

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 312.7 |
| Cycle time with agents (agent steps instant plus 2 min review) | 296.1 |
| Cycle time saved | 14.2 |
| Hands-on time saved (agent steps minus 2 min review each) | 14.2 |
