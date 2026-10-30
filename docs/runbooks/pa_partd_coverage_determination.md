# Runbook: Medicare Part D coverage determination

Source: 42 CFR 423.568, 423.570 and 423.572 (CMS), https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-B/part-423/subpart-M

Generated from the `LLM-compiled` workflow spec. Rounded boxes are agent steps, square boxes are human steps.

```mermaid
flowchart TD
  s1(["s1: Notify the enrollee and prescriber"])
  s2["s2: Provide an expedited determination"]
  s3["s3: Make a completely favorable decision"]
  s4["s4: Give written notice"]
  s5["s5: Inform of right to redetermination"]
  s6(["s6: Forward the request to IRE"])
  s1 --> s2
  s1 -->|request is expedited| s3
  s1 -->|request is not expedited| s4
  s2 --> s5
  s3 --> s4
  s3 --> s5
  s3 --> s6
  classDef agent fill:#e3eefb,stroke:#2a78d6
  classDef human fill:#fde8de,stroke:#eb6834
  class s1,s6 agent
  class s2,s3,s4,s5 human
```

| Step | Action | Owner | Executor | Hands to | Deadline | Source lines |
|---|---|---|---|---|---|---|
| s1 | Notify the enrollee and prescriber | Part D plan sponsor | agent | enrollee | no later than 72 hours after receipt of the request | L1 |
| s2 | Provide an expedited determination | Part D plan sponsor | human | enrollee |  | L2 |
| s3 | Make a completely favorable decision | Part D plan sponsor | human | enrollee | no later than 24 hours after receiving the request | L3 |
| s4 | Give written notice | Part D plan sponsor | human | enrollee |  | L4 |
| s5 | Inform of right to redetermination | Part D plan sponsor | human | enrollee |  | L5 |
| s6 | Forward the request to IRE | Part D plan sponsor | agent | IRE | within 24 hours of the expiration of the adjudication timeframe | L6 |

## Handoffs

- **s1** Part D plan sponsor to **enrollee**: Notify the enrollee and prescriber
- **s2** Part D plan sponsor to **enrollee**: Provide an expedited determination
- **s3** Part D plan sponsor to **enrollee**: Make a completely favorable decision
- **s4** Part D plan sponsor to **enrollee**: Give written notice
- **s5** Part D plan sponsor to **enrollee**: Inform of right to redetermination
- **s6** Part D plan sponsor to **IRE**: Forward the request to IRE
