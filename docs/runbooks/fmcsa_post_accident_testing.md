# Runbook: Commercial driver post-accident alcohol and drug testing

Source: 49 CFR 382.303 (FMCSA), https://www.ecfr.gov/current/title-49/subtitle-B/chapter-III/subchapter-B/part-382/subpart-C/section-382.303

Generated from the `LLM-compiled` workflow spec. Rounded boxes are agent steps, square boxes are human steps.

```mermaid
flowchart TD
  s1["s1: Test for alcohol"]
  s2["s2: Test for alcohol"]
  s3["s3: Test for controlled substances"]
  s4(["s4: Prepare record"])
  s5(["s5: Prepare record"])
  s6(["s6: Prepare record"])
  s1 --> s2
  s2 --> s3
  s1 -->|accident involves loss of human life| s4
  s2 -->|accident involves bodily injury with immediate medical treat| s4
  s3 -->|accident involves bodily injury with immediate medical treat| s4
  s4 -->|alcohol test not administered within 2 hours| s5
  s4 -->|alcohol test not administered within 8 hours| s6
  s5 --> s6
  classDef agent fill:#e3eefb,stroke:#2a78d6
  classDef human fill:#fde8de,stroke:#eb6834
  class s4,s5,s6 agent
  class s1,s2,s3 human
```

| Step | Action | Owner | Executor | Hands to | Deadline | Source lines |
|---|---|---|---|---|---|---|
| s1 | Test for alcohol | employer | human | driver |  | L1 |
| s2 | Test for alcohol | employer | human | driver | within 8 hours of the occurrence for a moving traffic violation arising from the accident | L2 |
| s3 | Test for controlled substances | employer | human | driver | within thirty-two hours of the occurrence for a moving traffic violation arising from the accident | L3 |
| s4 | Prepare record | employer | agent |  | within two hours following the accident | L4 |
| s5 | Prepare record | employer | agent |  | within eight hours following the accident | L5 |
| s6 | Prepare record | employer | agent |  | within 32 hours following the accident | L6 |

## Handoffs

- **s1** employer to **driver**: Test for alcohol
- **s2** employer to **driver**: Test for alcohol
- **s3** employer to **driver**: Test for controlled substances
