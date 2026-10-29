# Runbook: Commercial driver post-accident alcohol and drug testing

Source: 49 CFR 382.303 (FMCSA), https://www.ecfr.gov/current/title-49/subtitle-B/chapter-III/subchapter-B/part-382/subpart-C/section-382.303

Generated from the `gold` workflow spec. Rounded boxes are agent steps, square boxes are human steps.

```mermaid
flowchart TD
  s1["s1: Test surviving drivers for alcohol and drugs after a fatal a"]
  s2["s2: Alcohol-test a cited driver injury or tow-away accident, cit"]
  s3["s3: Drug-test a cited driver citation within 32 h"]
  s4(["s4: Record why the alcohol test was not done within 2 hours"])
  s5(["s5: Stop alcohol test attempts at 8 hours and record reasons"])
  s6(["s6: Stop drug test attempts at 32 hours and record reasons"])
  s7(["s7: Submit records to FMCSA on request"])
  s1 -->|alcohol test not done within 2 hours| s4
  s2 -->|alcohol test not done within 2 hours| s4
  s4 -->|not done within 8 hours| s5
  s1 -->|drug test not done within 32 hours| s6
  s3 -->|drug test not done within 32 hours| s6
  s4 -->|FMCSA requests| s7
  s5 -->|FMCSA requests| s7
  s6 -->|FMCSA requests| s7
  classDef agent fill:#e3eefb,stroke:#2a78d6
  classDef human fill:#fde8de,stroke:#eb6834
  class s4,s5,s6,s7 agent
  class s1,s2,s3 human
```

| Step | Action | Owner | Executor | Hands to | Deadline | Source lines |
|---|---|---|---|---|---|---|
| s1 | Test surviving drivers for alcohol and drugs after a fatal accident | employer | human |  |  | L1 |
| s2 | Alcohol-test a cited driver (injury or tow-away accident, citation within 8 h) | employer | human |  | within 8 hours of the occurrence for a moving traffic violation arising from the accident | L2 |
| s3 | Drug-test a cited driver (citation within 32 h) | employer | human |  | within thirty-two hours of the occurrence for a moving traffic violation arising from the accident | L3 |
| s4 | Record why the alcohol test was not done within 2 hours | employer | agent |  | within two hours following the accident | L4 |
| s5 | Stop alcohol test attempts at 8 hours and record reasons | employer | agent |  | within eight hours following the accident | L5 |
| s6 | Stop drug test attempts at 32 hours and record reasons | employer | agent |  | within 32 hours following the accident | L6 |
| s7 | Submit records to FMCSA on request | employer | agent | FMCSA |  | L7 |

## Handoffs

- **s7** employer to **FMCSA**: Submit records to FMCSA on request
