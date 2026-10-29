# Runbook: New employee health benefits enrollment (FEHB)

Source: 5 CFR 890.301, https://www.ecfr.gov/current/title-5/chapter-I/subchapter-B/part-890/subpart-C/section-890.301

Generated from the `gold` workflow spec. Rounded boxes are agent steps, square boxes are human steps.

```mermaid
flowchart TD
  s1["s1: Elect to enroll or not within 60 days"]
  s2(["s2: Set the enrollment effective date"])
  s3["s3: Determine belated-enrollment eligibility and advise the empl"]
  s1 -->|employee enrolls| s2
  s3 -->|employee enrolls within 60 days of the determination| s2
  classDef agent fill:#e3eefb,stroke:#2a78d6
  classDef human fill:#fde8de,stroke:#eb6834
  class s2 agent
  class s1,s3 human
```

| Step | Action | Owner | Executor | Hands to | Deadline | Source lines |
|---|---|---|---|---|---|---|
| s1 | Elect to enroll or not within 60 days | employee | human | employing office | within 60 days after becoming eligible | L1 |
| s2 | Set the enrollment effective date | employing office | agent |  |  | L2 |
| s3 | Determine belated-enrollment eligibility and advise the employee | employing office | human | employee | within the time limits; within 60 days after the employing office advises the employee of its determination | L3 |

## Handoffs

- **s1** employee to **employing office**: Elect to enroll or not within 60 days
- **s3** employing office to **employee**: Determine belated-enrollment eligibility and advise the employee
