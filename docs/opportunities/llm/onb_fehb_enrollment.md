# Automation opportunity: New employee health benefits enrollment (FEHB)

Process family: **onboarding** (mapped to Oracle Fusion Cloud HCM (Onboarding, Benefits)). Spec source: `llm (specs)`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Elect to enroll or not | employee | **agent** | Classifying or routing based on eligibility criteria. |  |
| s2 | Enrollment takes effect | employee | **agent** | Routine record keeping. |  |
| s3 | Enroll within 60 days | employee | **agent** | Routine record keeping and notification. |  |

- Agent steps: **3 of 3**; handoffs: **0**.
- Agent flags that the (draft) gold labels confirm: **1 of 3**. Unconfirmed flags are where the model over-automates; treat them as candidates for review, not decisions.
- Agreement of these executor calls with the gold labels is scored in `reports/results.csv`.

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 49.4 |
| Cycle time with agents (agent steps instant plus 2 min review) | 6.0 |
| Cycle time saved | 43.4 |
| Hands-on time saved (agent steps minus 2 min review each) | 43.4 |
