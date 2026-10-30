# Runbook: Sequence for putting on personal protective equipment (PPE)

Source: CDC, Sequence for Putting On PPE (CS250672-E), https://www.cdc.gov/hai/pdfs/ppe/ppe-sequence.pdf

Generated from the `LLM-compiled` workflow spec. Rounded boxes are agent steps, square boxes are human steps.

```mermaid
flowchart TD
  s1(["s1: Choose appropriate PPE based on precautions"])
  s2["s2: Put on gown"]
  s3["s3: Fasten gown in back"]
  s4["s4: Secure mask or respirator"]
  s5["s5: Fit respirator"]
  s6["s6: Fit-check respirator"]
  s7["s7: Put on goggles or face shield"]
  s8["s8: Extend gloves to wrist"]
  s1 --> s2
  s2 --> s3
  s3 --> s4
  s4 --> s5
  s5 --> s6
  s6 --> s7
  s7 --> s8
  classDef agent fill:#e3eefb,stroke:#2a78d6
  classDef human fill:#fde8de,stroke:#eb6834
  class s1 agent
  class s2,s3,s4,s5,s6,s7,s8 human
```

| Step | Action | Owner | Executor | Hands to | Deadline | Source lines |
|---|---|---|---|---|---|---|
| s1 | Choose appropriate PPE based on precautions | user | agent |  |  | L1 |
| s2 | Put on gown | user | human |  |  | L2 |
| s3 | Fasten gown in back | user | human |  |  | L3 |
| s4 | Secure mask or respirator | user | human |  |  | L4 |
| s5 | Fit respirator | user | human |  |  | L5 |
| s6 | Fit-check respirator | user | human |  |  | L6 |
| s7 | Put on goggles or face shield | user | human |  |  | L7 |
| s8 | Extend gloves to wrist | user | human |  |  | L8 |

## Handoffs

- none
