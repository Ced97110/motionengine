---
type: drill
level: advanced
positions: [PG, SG, SF, PF, C]
players_needed: 2
duration_minutes: 10-20
tags: [conditioning, transition, offense, defense, shooting, lane-slides, help-defense, skills-conditioning]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
trains_techniques:
  - id: transition-sprint
    emphasis: primary
  - id: skills-conditioning
    emphasis: primary
  - id: lane-slides
    emphasis: secondary
  - id: help-and-recover
    emphasis: secondary
  - id: catch-and-shoot
    emphasis: secondary
trains_anatomy:
  - region: hip_flexor_complex
    emphasis: primary
  - region: glute_max
    emphasis: secondary
  - region: ankle_complex
    emphasis: secondary
  - region: core_outer
    emphasis: secondary
---

# Offense-Transition-Defense Sequence

## Objective
Simulate the full game conditioning cycle — offense → sprint in transition → defensive movement → sprint back → offense — in a single continuous drill that builds sport-specific aerobic and anaerobic conditioning.

## Setup
- 1 player, 1 passer/rebounder (or coach)
- Full court
- Basketball

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":47}],"actions":[{"from":"1","to":"right_wing","type":"cut"},{"from":"right_wing","to":"rim","type":"cut"},{"from":"rim","to":"left_elbow","type":"cut"},{"from":"left_elbow","to":"rim","type":"cut"}],"notes":"Figure 21.6 is a full-court drill diagram showing a single player's movement pattern across both ends of the court. Only a half-court coordinate system is available, so the starting position is mapped to the baseline (y≈47). The diagram shows the player beginning at the near baseline, sprinting to the far end to receive a pass and shoot (inside 3PT line), then sprinting back in transition to the near paint for defensive movement, then sprinting again to the far end to shoot again. The arrows depict: (1) a sprint up the right wing toward the far basket/shooting spot, (2) movement through the far paint (defensive area), (3) sprint back down toward the near paint, and (4) sprint back up for the final shot. Because this is a full-court drill compressed into a half-court viewBox, the depicted arrows represent the player's continuous sprint-and-shoot sequence rather than discrete offensive set pieces. No additional offensive players are present; only one player (plus an off-screen passer) is used."}
```

## Execution
1. Player **starts at the baseline** and **sprints downcourt** to receive a pass.
2. **Shoots from a random spot inside the three-point line** (with or without a dribble).
3. Immediately after the shot, **sprints in transition** to the opposite paint area.
4. In the paint, performs a **defensive movement for 4-10 seconds** (lane slides, help-and-recover, or any assigned defensive pattern).
5. After the defensive work, **sprints in transition** back to the original end.
6. **Receives a pass** and takes a shot (with or without a dribble).
7. Continue the sequence for the **prescribed number of reps (4-6)**. [S7, p.328]

## Coaching Points
- Offensive movements can be predetermined (to replicate your specific offense) or random jump shots.
- Defensive movement must be **game-quality** — not jogging in place. "If you're doing lane slides, do them like you're guarding someone."
- The key is intensity at every phase — sprint transitions, not jog transitions.
- Mental toughness is developed when the player has to make a shooting decision while physically exhausted.
- Track makes-to-attempts to show progress.

## Progressions
1. **Beginner**: Reduce the defensive work to 4 seconds of simple lane slides; allow 1-dribble max on offense.
2. **Intermediate**: Full sequence as described; mix offensive movements (catch-and-shoot, pull-up, drive-to-layup).
3. **Advanced**: Increase to 8-10 reps; defensive movement becomes full help-and-recover pattern; add a specific offensive play action (High-Post cut, pin-screen curl, etc.) for the scoring possessions.

## Concepts Taught
- [[concept-modern-conditioning-basketball]] — full conditioning program philosophy
- [[concept-skills-conditioning]] — skill execution under fatigue
- [[transition-defense-principles]] — transition defensive mindset
- [[weak-side-help-defense]] — help-and-recover defense trained in paint segment

## Sources
- [S7, p.328] — Rich Dalatri, "Modern Conditioning Methods"
