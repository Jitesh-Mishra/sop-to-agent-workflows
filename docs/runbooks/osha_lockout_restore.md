# Runbook: Typical minimal lockout procedure: restoring equipment to service

Source: 29 CFR 1910.147 Appendix A (OSHA), https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.147AppA

Generated from the `gold` workflow spec. Rounded boxes are agent steps, square boxes are human steps.

```mermaid
flowchart TD
  s1["s1: Check the machine and area for nonessential items"]
  s2["s2: Check all employees are safely positioned or removed"]
  s3["s3: Verify controls are in neutral"]
  s4["s4: Remove lockout devices and reenergize"]
  s5(["s5: Notify affected employees the machine is ready"])
  s1 --> s2
  s2 --> s3
  s3 --> s4
  s4 --> s5
  classDef agent fill:#e3eefb,stroke:#2a78d6
  classDef human fill:#fde8de,stroke:#eb6834
  class s5 agent
  class s1,s2,s3,s4 human
```

| Step | Action | Owner | Executor | Hands to | Deadline | Source lines |
|---|---|---|---|---|---|---|
| s1 | Check the machine and area for nonessential items | authorized employee | human |  |  | L2 |
| s2 | Check all employees are safely positioned or removed | authorized employee | human |  |  | L3 |
| s3 | Verify controls are in neutral | authorized employee | human |  |  | L4 |
| s4 | Remove lockout devices and reenergize | authorized employee | human |  |  | L5 |
| s5 | Notify affected employees the machine is ready | authorized employee | agent | affected employees |  | L7 |

## Handoffs

- **s5** authorized employee to **affected employees**: Notify affected employees the machine is ready
