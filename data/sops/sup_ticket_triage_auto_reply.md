# Support ticket triage and auto-reply gate (authored)
source: AUTHORED for this project from the gate policy of github.com/Jitesh-Mishra/agent-replay-console (arc/agent.py, gate_decision); not a public or Oracle document
---
When a customer ticket arrives, classify it into one of the support queues and predict its priority.
Retrieve the most similar resolved tickets and knowledge base articles.
Draft a reply grounded in the retrieved answers.
If any validation check fails (tool timeout, unknown queue label, malformed tool output, empty retrieval, or a refusal in the draft), escalate the ticket to a support engineer with the run trace.
If route confidence is below 0.6, the predicted priority is high, or retrieval similarity is below 0.5, send the draft to a support agent for approval.
The support agent approves, edits, or rewrites the draft before it is sent.
If all checks pass, send the reply to the customer automatically.
Record the gate decision and its reasons in the run trace.
