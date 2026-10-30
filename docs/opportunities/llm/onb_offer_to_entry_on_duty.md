# Automation opportunity: Federal hiring: tentative offer through entry on duty

Process family: **onboarding** (mapped to Oracle Fusion Cloud HCM (Onboarding, Benefits)). Spec source: `llm (specs)`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Audit certificate for compliance | Human Resources Office and Security Office | **human** | Requires hands-on review and attestation by multiple parties. |  |
| s2 | Extend a tentative job offer | Human Resources Office | **human** | Needs hands-on communication and decision-making. | selectee |
| s3 | Solicit and verify information | Human Resources Office | **agent** | Soliciting and verifying information is an information work that an AI agent can do with system access. | selectee |
| s4 | Notify remaining eligibles | Human Resources Office | **agent** | Compiling and sending a notice from known facts. | remaining eligibles |
| s5 | Initiate investigation | Agency | **agent** | Searching and correlating information to initiate the investigation. |  |
| s6 | Allow selectee to accept or decline | Human Resources Office | **human** | A professional judgment and decision (approve, deny, determine, accept, adjudicate) is needed. | selectee |
| s7 | Enter on duty | Human Resources Office | **human** | Needs physical presence and hands-on action to enter on duty. | selectee |
| s8 | Orientation Roadmap begins | Human Resources Office | **agent** | Creating and sending a roadmap from known facts. |  |

- Agent steps: **4 of 8**; handoffs: **5**.
- Agent flags that the (draft) gold labels confirm: **3 of 4**. Unconfirmed flags are where the model over-automates; treat them as candidates for review, not decisions.
- Agreement of these executor calls with the gold labels is scored in `reports/results.csv`.

## Riskiest handoff: s3 (Solicit and verify information) to selectee
Risk score 2: leaves the organisation (selectee).

Context the packet must carry:

- Instructions (source text): Solicit, review and verify information from selectee such as DD-214, college transcripts, OF-306, Declaration for Federal Employment, etc. if not already provided with the initial application.
- Deadline: none stated
- Completed steps and their outputs: s1, s2
- Open decisions downstream: none
- Next steps: s4

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 831.4 |
| Cycle time with agents (agent steps instant plus 2 min review) | 320.9 |
| Cycle time saved | 470.0 |
| Hands-on time saved (agent steps minus 2 min review each) | 58.7 |
