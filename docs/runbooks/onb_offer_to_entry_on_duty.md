# Runbook: Federal hiring: tentative offer through entry on duty

Source: OPM End-to-End Hiring Roadmap (Hiring Elements), https://www.opm.gov/policy-data-oversight/human-capital-management/hiring-reform/hiringelements.pdf ; 5 CFR 731.106, https://www.ecfr.gov/current/title-5/chapter-I/subchapter-B/part-731/subpart-A/section-731.106

Generated from the `LLM-compiled` workflow spec. Rounded boxes are agent steps, square boxes are human steps.

```mermaid
flowchart TD
  s1["s1: Audit certificate for compliance"]
  s2["s2: Extend a tentative job offer"]
  s3(["s3: Solicit and verify information"])
  s4(["s4: Notify remaining eligibles"])
  s5(["s5: Initiate investigation"])
  s6["s6: Allow selectee to accept or decline"]
  s7["s7: Enter on duty"]
  s8(["s8: Orientation Roadmap begins"])
  s1 --> s2
  s2 --> s3
  s3 --> s4
  s4 --> s5
  s5 --> s6
  s6 --> s7
  s7 --> s8
  classDef agent fill:#e3eefb,stroke:#2a78d6
  classDef human fill:#fde8de,stroke:#eb6834
  class s3,s4,s5,s8 agent
  class s1,s2,s6,s7 human
```

| Step | Action | Owner | Executor | Hands to | Deadline | Source lines |
|---|---|---|---|---|---|---|
| s1 | Audit certificate for compliance | Human Resources Office and Security Office | human |  |  | L1 |
| s2 | Extend a tentative job offer | Human Resources Office | human | selectee |  | L3 |
| s3 | Solicit and verify information | Human Resources Office | agent | selectee |  | L4 |
| s4 | Notify remaining eligibles | Human Resources Office | agent | remaining eligibles |  | L5 |
| s5 | Initiate investigation | Agency | agent |  |  | L6 |
| s6 | Allow selectee to accept or decline | Human Resources Office | human | selectee |  | L7 |
| s7 | Enter on duty | Human Resources Office | human | selectee |  | L8 |
| s8 | Orientation Roadmap begins | Human Resources Office | agent |  |  | L9 |

## Handoffs

- **s2** Human Resources Office to **selectee**: Extend a tentative job offer
- **s3** Human Resources Office to **selectee**: Solicit and verify information
- **s4** Human Resources Office to **remaining eligibles**: Notify remaining eligibles
- **s6** Human Resources Office to **selectee**: Allow selectee to accept or decline
- **s7** Human Resources Office to **selectee**: Enter on duty
