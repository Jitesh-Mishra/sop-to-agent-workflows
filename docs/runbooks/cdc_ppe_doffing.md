# Runbook: How to safely remove personal protective equipment (PPE), example 1

Source: CDC, How to Safely Remove PPE (CS250672-E), https://www.cdc.gov/hai/pdfs/ppe/ppe-sequence.pdf

Generated from the `LLM-compiled` workflow spec. Rounded boxes are agent steps, square boxes are human steps.

```mermaid
flowchart TD
  s1["s1: Remove all PPE except a respirator"]
  s2["s2: Peel off first glove"]
  s3["s3: Peel off second glove"]
  s4["s4: Remove goggles or face shield"]
  s5["s5: Discard goggles or face shield"]
  s6["s6: Unfasten gown ties"]
  s7["s7: Pull gown away from neck and shoulders"]
  s8["s8: Discard gown"]
  s9["s9: Remove mask or respirator"]
  s10["s10: Discard mask or respirator"]
  s11["s11: Wash hands or use sanitizer"]
  s1 --> s2
  s2 --> s3
  s3 --> s4
  s4 --> s5
  s5 --> s6
  s6 --> s7
  s7 --> s8
  s8 --> s9
  s9 --> s10
  s10 --> s11
  classDef agent fill:#e3eefb,stroke:#2a78d6
  classDef human fill:#fde8de,stroke:#eb6834
  class s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11 human
```

| Step | Action | Owner | Executor | Hands to | Deadline | Source lines |
|---|---|---|---|---|---|---|
| s1 | Remove all PPE except a respirator | healthcare worker | human |  |  | L1 |
| s2 | Peel off first glove | healthcare worker | human |  |  | L2 |
| s3 | Peel off second glove | healthcare worker | human |  |  | L3 |
| s4 | Remove goggles or face shield | healthcare worker | human |  |  | L4 |
| s5 | Discard goggles or face shield | healthcare worker | human |  |  | L5 |
| s6 | Unfasten gown ties | healthcare worker | human |  |  | L6 |
| s7 | Pull gown away from neck and shoulders | healthcare worker | human |  |  | L7 |
| s8 | Discard gown | healthcare worker | human |  |  | L8 |
| s9 | Remove mask or respirator | healthcare worker | human |  |  | L9 |
| s10 | Discard mask or respirator | healthcare worker | human |  |  | L10 |
| s11 | Wash hands or use sanitizer | healthcare worker | human |  |  | L11 |

## Handoffs

- none
