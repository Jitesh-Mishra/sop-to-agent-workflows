# Automation opportunity: Federal hiring: tentative offer through entry on duty

Process family: **onboarding** (mapped to Oracle Fusion Cloud HCM (Onboarding, Benefits)). Spec source: `gold`. Public template mapped to an Oracle product area, not an Oracle internal SOP.

| Step | Action | Role | Executor | Why | Handoff to |
|---|---|---|---|---|---|
| s1 | Audit the certificate for legal compliance | Human Resources Office | **human** |  |  |
| s2 | Extend a tentative job offer | Human Resources Office | **agent** |  | selectee |
| s3 | Collect and verify selectee documents (DD-214, transcripts, OF-306) | Human Resources Office | **agent** |  | selectee |
| s4 | Notify remaining eligibles of the selection | Human Resources Office | **agent** |  | remaining eligibles |
| s5 | Initiate the background investigation | Security Office | **agent** |  |  |
| s6 | Accept or decline the official offer | selectee | **human** |  |  |
| s7 | Return entry-on-duty forms | selectee | **human** |  | Human Resources Office |
| s8 | Start orientation | Human Resources Office | **human** |  |  |

- Agent steps: **4 of 8**; handoffs: **4**.

## Riskiest handoff: s6 (Accept or decline the official offer) to selectee
Risk score 4: leaves the organisation (selectee), 1 open decision(s) downstream, a person must act.

Context the packet must carry:

- Instructions (source text): Official offer and acceptance: allow selectee to accept or decline job offer and make necessary arrangements with current employer.
- Deadline: none stated
- Completed steps and their outputs: s1, s2, s3, s4, s5
- Open decisions downstream: Which applies: selectee accepts?
- Next steps: s7

## Estimated time (SIMULATED)
200 runs through the LangGraph runtime with random branch choices and the assumed time model in `sopflow/eval/opportunity.py` (not measured data).

| | Median minutes per run |
|---|---:|
| Cycle time today (every step by a person, queue wait at each change of hands) | 872.4 |
| Cycle time with agents (agent steps instant plus 2 min review) | 578.1 |
| Cycle time saved | 223.7 |
| Hands-on time saved (agent steps minus 2 min review each) | 58.2 |
