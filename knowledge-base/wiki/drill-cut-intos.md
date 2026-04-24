---
type: drill
level: intermediate
positions: [PG, SG, SF]
players_needed: 3
duration_minutes: 8-12
tags: [shooting, cutting, catch-and-shoot, two-count-stop, elbow, game-speed]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
trains_techniques:
  - id: shooting-off-screens
    emphasis: primary
  - id: catch-and-shoot
    emphasis: primary
  - id: two-count-stop
    emphasis: secondary
  - id: v-cut-footwork
    emphasis: secondary
trains_anatomy:
  - region: ankle_complex
    emphasis: primary
  - region: hip_flexor_complex
    emphasis: secondary
  - region: core_outer
    emphasis: secondary
---

# Cut Intos Drill

## Objective
Train the cut-catch-and-shoot sequence by having the player simulate cutting off a screen into a cluster of chairs at the elbow, receiving a live pass, and shooting a jump shot off a controlled two-count stop.

## Setup
- Half-court
- 3 chairs set just outside the left elbow
- Coach outside the 3PT arc with the ball
- 1 rebounder in the lane
- Player starts on the opposite side of the court from the chairs

```json name=diagram-positions
{"players":[{"role":"3","x":22,"y":22},{"role":"R","x":3,"y":35},{"role":"C","x":-24,"y":29}],"actions":[{"from":"3","to":"left_elbow","type":"cut"},{"from":"C","to":"left_elbow","type":"pass"}],"notes":"Figure 19.15 (Cut Intos drill). Three chairs (h) are clustered just outside the left elbow — represented as the cut destination. The player (3) starts on the right/opposite wing. The rebounder (R) is in the lane slightly above the block. The coach (C) is outside the three-point arc on the left side. The diagram shows the player first faking toward the basket, then cutting hard into the chairs at the left elbow to receive a pass from the coach. The chairs themselves are not players and are omitted from the players array."}
```

## Execution
1. Player fakes a cut to the basket
2. Player cuts hard into the three chairs at the elbow (simulating coming off a screen)
3. Receives the ball from the coach
4. Makes a two-count stop under control
5. Takes a jump shot
6. Make 5 shots, then repeat the routine on the other side of the court

## Coaching Points
- The basket-cut fake must be convincing — sell it with body and eyes, not just a head bob
- Cut hard into the chairs — "come off the screen shoulder to shoulder" (simulate tight screen usage)
- Two-count stop must be controlled and balanced — same as in Dribble Intos
- Hands up and in shooting pocket before the ball arrives
- "Perfect feet" on the stop — same footwork every rep

## Progressions
1. **Beginner**: No chair, just the cut-and-catch from a coach; focus on footwork
2. **Intermediate**: Full drill with chairs as described; make-before-you-move (5 makes)
3. **Advanced**: Coach varies the timing and angle of the pass; add a live closeout from the opposite wing

## Concepts Taught
- [[concept-player-development-philosophy-s7]] — precision detail on every rep
- [[concept-shooting-off-the-move-footwork]] — two-count stride stop mechanics
- [[concept-v-cut-footwork]] — the fake-and-cut action
- [[concept-shooting-off-screens-s3]] — simulates coming off a pin-down screen

## Sources
- [S7, p.310] — Kevin Eastman, Chapter 19: Chair Drills
