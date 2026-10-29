# Runbook: Typical minimal lockout procedure: sequence of lockout

Source: 29 CFR 1910.147 Appendix A (OSHA), https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.147AppA

Generated from the `gold` workflow spec. Rounded boxes are agent steps, square boxes are human steps.

```mermaid
flowchart TD
  s1(["s1: Notify affected employees of the shutdown and lockout"])
  s2["s2: Identify energy type, magnitude, hazards and controls"]
  s3["s3: Shut the machine down by the normal stopping procedure"]
  s4["s4: De-activate the energy isolating devices"]
  s5["s5: Lock out the isolating devices with assigned locks"]
  s6["s6: Dissipate or restrain stored energy"]
  s7["s7: Verify isolation after checking no personnel are exposed"]
  s8["s8: Return operating controls to neutral or off"]
  s1 --> s2
  s2 -->|machine is operating| s3
  s2 -->|machine not operating| s4
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
| s1 | Notify affected employees of the shutdown and lockout | authorized employee | agent | affected employees |  | L3 |
| s2 | Identify energy type, magnitude, hazards and controls | authorized employee | human |  |  | L4 |
| s3 | Shut the machine down by the normal stopping procedure | authorized employee | human |  |  | L5 |
| s4 | De-activate the energy isolating devices | authorized employee | human |  |  | L6 |
| s5 | Lock out the isolating devices with assigned locks | authorized employee | human |  |  | L7 |
| s6 | Dissipate or restrain stored energy | authorized employee | human |  |  | L8 |
| s7 | Verify isolation after checking no personnel are exposed | authorized employee | human |  |  | L9 |
| s8 | Return operating controls to neutral or off | authorized employee | human |  |  | L10 |

## Handoffs

- **s1** authorized employee to **affected employees**: Notify affected employees of the shutdown and lockout
