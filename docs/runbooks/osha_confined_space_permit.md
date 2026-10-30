# Runbook: Permit-required confined spaces: permit system

Source: 29 CFR 1910.146(e) (OSHA), https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.146

Generated from the `LLM-compiled` workflow spec. Rounded boxes are agent steps, square boxes are human steps.

```mermaid
flowchart TD
  s1(["s1: Document completion of pre-entry measures"])
  s2["s2: Authorize entry"]
  s3(["s3: Make permit available"])
  s4(["s4: Limit permit duration"])
  s5(["s5: Cancel entry and permit"])
  s6["s6: Retain canceled permits"]
  s1 --> s2
  s2 --> s3
  s3 --> s4
  s4 --> s5
  s5 --> s6
  classDef agent fill:#e3eefb,stroke:#2a78d6
  classDef human fill:#fde8de,stroke:#eb6834
  class s1,s3,s4,s5 agent
  class s2,s6 human
```

| Step | Action | Owner | Executor | Hands to | Deadline | Source lines |
|---|---|---|---|---|---|---|
| s1 | Document completion of pre-entry measures | employer | agent |  |  | L1 |
| s2 | Authorize entry | entry supervisor | human |  |  | L2 |
| s3 | Make permit available | employer | agent | authorized entrants |  | L3 |
| s4 | Limit permit duration | employer | agent |  |  | L4 |
| s5 | Cancel entry and permit | entry supervisor | agent |  |  | L5 |
| s6 | Retain canceled permits | employer | human |  |  | L6 |

## Handoffs

- **s3** employer to **authorized entrants**: Make permit available
