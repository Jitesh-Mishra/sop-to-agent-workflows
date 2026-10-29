# Gold labels: guidelines and who labeled what

## Status
| Set | SOPs | Labeled by | Reviewed by |
|---|---:|---|---|
| Process families (procure-to-pay, onboarding, incident handling, prior authorization, support escalation) | 18 | Claude (draft), 2026-10-29 | **pending: Jitesh** |
| Out-of-domain government SOPs | 20 | Claude (draft), 2026-10-29 | **pending: Jitesh** |

Every gold file carries `labeled_by` and `reviewed_by`. Until review, every reported number is "against draft gold labels".
To review, open `data/gold/<sop_id>.json` next to `python -m sopflow.cli show <sop_id>`. Fix what is wrong, set `reviewed_by`, and commit. Then rerun `python -m sopflow.eval.report`; scoring is offline, so no LLM rerun is needed.

## SOP text
- Excerpts of US federal regulations and guidance (eCFR, FAR, OSHA, CDC, NIST, CISA, OPM, CMS). These are US government works in the public domain. The source URL is in each file header.
- One sentence or list item per line, so a step can cite line numbers.
- Text was **excerpted and lightly condensed**:
  - Enumerated sub-lists were merged into one sentence.
  - Cross-references were removed.
  - A few sentences were reordered (PPE doffing, seal check) or split (seal check).
  - No requirement was added.
- The two `sup_*` SOPs are **authored** for this project from the gate policy in agent-replay-console. They are labeled as authored in their headers and in `data/families.json`.

## What counts as a step
- An action a specific party must carry out: do, decide, check, notify, submit, record.
- **Not steps:**
  - purpose and scope statements, definitions, notes and cautions
  - prohibitions ("shall not")
  - stand-alone time limits
  - exemptions (these become edge conditions)
  - lists describing what a notice must contain (their line numbers are added to the notification step)
- A step lists every line that states it. Most steps cite one line.

## Edges
- Execution order or dependency as stated or clearly implied.
- Branches ("if", "when", "unless") get one edge per branch, with the condition text.
- Optional pre-steps (a law-enforcement delay, a timeframe extension) point into the step they delay.
- Loops in the source (NIST 800-61 "repeat detection for new hosts") are labeled as a single "repeat for new hosts" step, because the workflow must be a DAG.

## Handoffs
A step is a handoff when its main effect is passing information, a decision, a document or responsibility to a **different** party: notify, report, submit, forward, refer, inform, furnish, or appeal to. `handoff_to` names the recipient.

## Executor (agent vs human)
This policy is also given, word for word, to the LLM in prompt v2.
- **human**:
  - physical action or presence
  - a signature, attestation or certification
  - a professional, clinical, legal or accountable judgment or decision (approve, deny, determine, accept, adjudicate)
  - a conversation (interview, counseling)
  - any step done by an outside party (customer, enrollee, contractor, applicant, regulator)
- **agent**: information work an AI agent with system access could do:
  - drafting and sending a notice from known facts
  - compiling, checking or forwarding documents
  - recording, logging or tracking
  - searching and correlating information
  - classifying or routing

Hard cases, decided as follows:
- A step that both decides and notifies ("make the determination and notify within 72 hours") is **human**.
- A step that only issues or sends an already-made decision is **agent**.
- Oral notifications by phone (EPCRA, NRC) are **human**.
- Patching production systems is **human**: a change with accountability, even when tools deploy it.
