# Runbook: High-priority ticket escalation (authored)

Source: AUTHORED for this project as a companion to sup_ticket_triage_auto_reply; queue and priority mix from the 16,335-ticket dataset used in agent-replay-console; not a public or Oracle document

Generated from the `LLM-compiled` workflow spec. Rounded boxes are agent steps, square boxes are human steps.

```mermaid
flowchart TD
  s1(["s1: Confirm priority and queue"])
  s2(["s2: Notify on-call engineer"])
  s3(["s3: Open incident"])
  s4(["s4: Post status update"])
  s5(["s5: Forward ticket to billing team"])
  s6(["s6: Send acknowledgement"])
  s7(["s7: Document fix in knowledge base"])
  s8(["s8: Close ticket"])
  s1 --> s2
  s2 -->|ticket reports a service outage| s3
  s2 -->|ticket reports a service outage| s6
  s3 --> s4
  s5 -->|ticket reports a billing or payment error| s6
  s5 -->|ticket reports a billing or payment error| s8
  s6 --> s8
  s7 --> s8
  classDef agent fill:#e3eefb,stroke:#2a78d6
  classDef human fill:#fde8de,stroke:#eb6834
  class s1,s2,s3,s4,s5,s6,s7,s8 agent
```

| Step | Action | Owner | Executor | Hands to | Deadline | Source lines |
|---|---|---|---|---|---|---|
| s1 | Confirm priority and queue | support agent | agent |  |  | L1 |
| s2 | Notify on-call engineer | support agent | agent | on-call engineer | within 1 hour of arrival | L2 |
| s3 | Open incident | on-call engineer | agent |  |  | L3 |
| s4 | Post status update | on-call engineer | agent |  |  | L4 |
| s5 | Forward ticket to billing team | support agent | agent | billing team |  | L5 |
| s6 | Send acknowledgement | support agent | agent | customer |  | L6 |
| s7 | Document fix in knowledge base | owning team | agent |  |  | L7 |
| s8 | Close ticket | owning team | agent |  |  | L7 |

## Handoffs

- **s2** support agent to **on-call engineer**: Notify on-call engineer
- **s5** support agent to **billing team**: Forward ticket to billing team
- **s6** support agent to **customer**: Send acknowledgement
