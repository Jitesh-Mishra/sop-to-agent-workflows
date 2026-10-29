# Runbook: Reporting fatalities, hospitalizations, amputations, and losses of an eye to OSHA

Source: 29 CFR 1904.39 (OSHA), https://www.osha.gov/laws-regs/regulations/standardnumber/1904/1904.39

Generated from the `gold` workflow spec. Rounded boxes are agent steps, square boxes are human steps.

```mermaid
flowchart TD
  s1["s1: Determine the reportable event and deadline 8 h fatality, 24"]
  s2(["s2: Report to OSHA by phone, in person or online with the requir"])
  s3(["s3: Record the event on the OSHA injury and illness records"])
  s4["s4: Decide whether to investigate"]
  s1 -->|not a public-road motor vehicle accident outside a work zone| s2
  s1 -->|public-road motor vehicle accident outside a work zone| s3
  s2 --> s3
  s2 --> s4
  classDef agent fill:#e3eefb,stroke:#2a78d6
  classDef human fill:#fde8de,stroke:#eb6834
  class s2,s3 agent
  class s1,s4 human
```

| Step | Action | Owner | Executor | Hands to | Deadline | Source lines |
|---|---|---|---|---|---|---|
| s1 | Determine the reportable event and deadline (8 h fatality, 24 h hospitalization, amputation, eye loss) | employer | human |  | Within eight (8) hours after the death of any employee as a result of a work-related incident; Within twenty-four (24) hours after the in-patient hospitalization of one or more employees or an employee's amputation or an employee's loss of an eye | L1, L2 |
| s2 | Report to OSHA by phone, in person or online with the required details | employer | agent | OSHA |  | L3, L4, L5 |
| s3 | Record the event on the OSHA injury and illness records | employer | agent |  |  | L7 |
| s4 | Decide whether to investigate | OSHA Area Office director | human |  |  | L8 |

## Handoffs

- **s2** employer to **OSHA**: Report to OSHA by phone, in person or online with the required details
