# Runbook: Employment eligibility verification (Form I-9)

Source: 8 CFR 274a.2(b) (DHS/USCIS), https://www.ecfr.gov/current/title-8/chapter-I/subchapter-B/part-274a/subpart-A/section-274a.2

Generated from the `gold` workflow spec. Rounded boxes are agent steps, square boxes are human steps.

```mermaid
flowchart TD
  s1["s1: Complete and sign Form I-9 section 1 at hire"]
  s2["s2: Physically examine identity and work authorization documents"]
  s3["s3: Complete and sign Form I-9 section 2 within 3 business days"]
  s4(["s4: Retain the Form I-9 for the required period"])
  s5["s5: Reverify work authorization before it expires"]
  s1 --> s2
  s2 --> s3
  s3 --> s4
  s4 -->|work authorization expires| s5
  classDef agent fill:#e3eefb,stroke:#2a78d6
  classDef human fill:#fde8de,stroke:#eb6834
  class s4 agent
  class s1,s2,s3,s5 human
```

| Step | Action | Owner | Executor | Hands to | Deadline | Source lines |
|---|---|---|---|---|---|---|
| s1 | Complete and sign Form I-9 section 1 at hire | employee | human |  |  | L1 |
| s2 | Physically examine identity and work authorization documents within 3 business days | employer | human |  | Within three business days of the hire | L3 |
| s3 | Complete and sign Form I-9 section 2 within 3 business days | employer | human |  | Within three business days of the hire | L4 |
| s4 | Retain the Form I-9 for the required period | employer | agent |  |  | L5 |
| s5 | Reverify work authorization before it expires | employer | human |  | not later than the date work authorization expires | L6 |

## Handoffs

- none
