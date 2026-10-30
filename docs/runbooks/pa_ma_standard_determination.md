# Runbook: Medicare Advantage standard organization determination (prior authorization)

Source: 42 CFR 422.566(d) and 422.568, https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-B/part-422/subpart-M

Generated from the `LLM-compiled` workflow spec. Rounded boxes are agent steps, square boxes are human steps.

```mermaid
flowchart TD
  s1(["s1: Notify the enrollee"])
  s2(["s2: Extend the timeframe"])
  s3["s3: Review by a physician"]
  s4["s4: Deny a service or item"]
  s5(["s5: Provide notice language"])
  s6["s6: Appeal the failure"]
  s1 --> s2
  s2 -->|enrollee requests the extension or the extension is justifie| s3
  s3 --> s4
  s4 --> s5
  s4 -->|MA organization fails to provide timely notice of an organiz| s6
  classDef agent fill:#e3eefb,stroke:#2a78d6
  classDef human fill:#fde8de,stroke:#eb6834
  class s1,s2,s5 agent
  class s3,s4,s6 human
```

| Step | Action | Owner | Executor | Hands to | Deadline | Source lines |
|---|---|---|---|---|---|---|
| s1 | Notify the enrollee | MA organization | agent | enrollee | no later than 7 calendar days after receiving the request for the standard organization determination | L1 |
| s2 | Extend the timeframe | MA organization | agent |  |  | L2 |
| s3 | Review by a physician | MA organization | human |  |  | L3 |
| s4 | Deny a service or item | MA organization | human | enrollee and physician |  | L4 |
| s5 | Provide notice language | MA organization | agent | enrollee |  | L5 |
| s6 | Appeal the failure | MA organization | human |  |  | L6 |

## Handoffs

- **s1** MA organization to **enrollee**: Notify the enrollee
- **s4** MA organization to **enrollee and physician**: Deny a service or item
- **s5** MA organization to **enrollee**: Provide notice language
