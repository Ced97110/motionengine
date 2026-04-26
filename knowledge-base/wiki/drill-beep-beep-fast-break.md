---
type: drill
level: advanced
positions: [PG, SG, SF, PF, C]
players_needed: 10
duration_minutes: 15-20
tags: [transition, fast-break, conditioning, decision-making, shooting]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
trains_techniques:
  - id: transition-fast-break
    emphasis: primary
  - id: decision-making-under-pressure
    emphasis: primary
  - id: catch-and-shoot
    emphasis: secondary
  - id: push-dribble-attack
    emphasis: secondary
trains_anatomy:
  - region: hip_flexor_complex
    emphasis: primary
  - region: glute_max
    emphasis: secondary
  - region: ankle_complex
    emphasis: secondary
---

# Beep-Beep Fast Break Drill

## Objective
Simultaneously train fast-break pace and physical conditioning by forcing the point guard to either shoot immediately or make one pass for an instant shot — named after the Roadrunner cartoon character for its speed requirement.

## Setup
- Full court
- Two teams of 5 players each
- Standard game setup at one end
- Ball in play

## Execution
1. Offense runs a possession with the following constraint: **the PG must push the ball down as fast as possible and either shoot as quickly as he can OR make one pass — the receiver must shoot immediately** [S7, p.160]
2. No second passes are permitted by design; the first receiver shoots
3. Defense rebounds (or takes the ball after a make) and immediately transitions to offense running the same break at the opposite end
4. Play continues full-court, end-to-end, without stoppages
5. Coaches correct wrong decisions but let the game flow

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":2},{"role":"2","x":-24,"y":2},{"role":"3","x":-12,"y":2},{"role":"4","x":12,"y":2},{"role":"5","x":24,"y":2},{"role":"x1","x":-24,"y":5},{"role":"x2","x":-8,"y":5},{"role":"x3","x":4,"y":5},{"role":"x4","x":16,"y":5},{"role":"x5","x":24,"y":5}],"actions":[{"from":"1","to":"rim","type":"dribble"},{"from":"2","to":"left_corner","type":"cut"},{"from":"5","to":"right_corner","type":"cut"},{"from":"1","to":"3","type":"pass"},{"from":"3","to":"rim","type":"cut"}],"notes":"Figure 9.14 (p.160) shows the Beep-Beep drill as a 5-on-5 full-court setup. The diagram depicts the starting positions at roughly the half-court line: offensive players (labeled with circles) spread across the top, with defenders (labeled \"x\") just inside. The point guard (1) is at center with ball, two offensive wings spread wide on each side, and two defenders also spread. Action arrows show: the PG dribbling hard toward the rim, wings sprinting to corners/wings, and a pass option to a wing who cuts to the basket. The diagram uses the notation \"9\" repeated for all player labels (likely a printing artifact), so roles are inferred from position and the prose description. This is the initial formation only; the drill continues end-to-end."}
```

## Coaching Points
- PG must commit to EITHER shoot immediately OR make one decisive pass — no dribbling to survey the floor [S7, p.160]
- The receiver of the one pass must be ready to catch and shoot immediately — no pump fakes, no extra dribbles
- Running at top speed serves a dual purpose: develops the sprinting-the-court habit AND raises practice competition level [S7, p.160]
- The pace creates the same pressure players feel in late-game transition situations
- "The pace raises the level of competition during practice, which challenges players to step up their performance each time on the court, not just in games." [S7, p.160]

## Progressions
1. **Beginner**: PG must only push — no shooting decision required; any open layup or pass for layup
2. **Intermediate**: Standard Beep-Beep (1 pass max, immediate shot)
3. **Advanced**: Add a designated shot clock rule (must shoot within 4 seconds of half-court or possession ends)

## Concepts Taught
- [[concept-fast-break-philosophy-karl-moe]] — player-decision ownership and sprinting culture
- [[concept-fast-break-primary-secondary-dantoni]] — primary break mindset and timing

## Sources
- [S7, pp.159–160] — Karl & Moe, Beep-Beep Drill description
