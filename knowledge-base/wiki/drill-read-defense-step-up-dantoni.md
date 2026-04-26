---
type: drill
level: intermediate
positions: [PF, C, PG]
players_needed: 3-8
duration_minutes: 8-10
tags: [transition, fast-break, screening, pick-and-roll, reading-defense, big-men]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
trains_techniques:
  - id: pick-and-roll
    emphasis: primary
  - id: roll-to-basket
    emphasis: primary
  - id: reading-defense
    emphasis: secondary
  - id: screen-setting
    emphasis: secondary
trains_anatomy:
  - region: hip_flexor_complex
    emphasis: primary
  - region: glute_max
    emphasis: secondary
  - region: core_outer
    emphasis: secondary
---

# Read the Defense: Step-Up Drill (D'Antoni Secondary Break)

## Objective
Train the counter action when the defense forces the ball handler to the sideline — the "step-up" screen that frees the screener for a roll to the basket after the ball handler is forced baseline.

## Setup
- Both halves of the half-court (run simultaneously on both sides)
- One coach with the ball on the wing
- Line of players behind the coach

## Execution
1. Coach starts to dribble toward the baseline (simulating being forced sideline by defense)
2. First player in line follows the coach (simulates trailing the ball handler)
3. Player comes back and **sets a screen** for the coach (the "step-up" action)
4. Coach uses the screen to reverse direction or continue
5. After the screen, player **rolls to the basket going inside the lane**
6. Receives a pass from the coach for a layup or dunk [S7, p.173]

```json name=diagram-positions
{"players":[{"role":"C","x":-18,"y":22},{"role":"C2","x":18,"y":22},{"role":"1","x":-7,"y":33},{"role":"2","x":7,"y":33},{"role":"3","x":-7,"y":37},{"role":"4","x":7,"y":37}],"actions":[{"from":"C","to":"left_corner","type":"dribble"},{"from":"1","to":"C","type":"screen"},{"from":"1","to":"rim","type":"cut"},{"from":"C","to":"1","type":"pass"},{"from":"C2","to":"right_corner","type":"dribble"},{"from":"2","to":"C2","type":"screen"},{"from":"2","to":"rim","type":"cut"},{"from":"C2","to":"2","type":"pass"}],"notes":"Figure 10.20 shows the step-up drill run simultaneously on both sides of the half-court. Two coaches (C) are positioned on each wing with lines of players behind them. Each coach dribbles toward the baseline; the first player in line follows, comes back to set a step-up screen, then rolls inside the lane to receive the pass. The diagram is mirrored left/right for both sides. Player lines are stacked near the elbow/lane area. Roles labeled as coaches (C, C2) and first two players in each line (1/2 and 3/4 as queue). The starting formation shows coaches on wings and players queued behind them."}
```

## Coaching Points
- The step-up screen is the answer to defensive sideline-forcing — rather than fighting it, use the forced direction to create a new angle
- The player must read when the coach is being forced sideline and **quickly set the step-up screen** before the coach is cornered
- Roll goes *inside the lane* — the defensive rotation leaves the paint unguarded when sideline pressure is applied
- Run on both halves simultaneously to maximize reps [S7, p.173]
- This is a game-situation read: "If the defense wants to force the ball handler to the sideline, we counter this defensive move with a step-up move." [S7, p.173]

## Progressions
1. **Beginner**: Coach walks the path slowly; player sets stationary screen and holds position
2. **Intermediate**: Full-speed execution as described
3. **Advanced**: Add a live defensive player who actually forces the coach sideline, requiring the player to time the step-up against real defensive pressure

## Concepts Taught
- [[concept-fast-break-primary-secondary-dantoni]] — reading defense on the break and using step-up counters
- [[pick-and-roll-defense]] — how the defense tries to contain the roll

## Sources
- [S7, p.173] — D'Antoni, Gentry, Iavaroni: Read the Defense: Step-Up Drill
