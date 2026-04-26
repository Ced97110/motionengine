---
type: drill
level: beginner
positions: [PG, SG, SF, PF, C]
players_needed: 5
duration_minutes: 5-10
tags: [passing, conditioning, warm-up, spacing, communication]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
trains_techniques:
  - id: passing-timing
    emphasis: primary
  - id: sprint-conditioning
    emphasis: secondary
  - id: communication-on-court
    emphasis: secondary
trains_anatomy:
  - region: hip_flexor_complex
    emphasis: primary
  - region: ankle_complex
    emphasis: secondary
---

# Circle Pass Drill

## Objective
Build passing timing, communication, and sprint conditioning by having two mirrored groups pass simultaneously while sprinting to exchange positions.

## Setup
- 5 players: 4 players positioned at compass points (A at top, B at right wing, C at left wing, D at opposite baseline corner) **outside** the three-point arc, each with a ball
- A 5th corresponding set of 4 players **inside** the three-point arc in the same compass positions
- Player A inside the arc is under the basket; players B and D are at his left and right

```json name=diagram-positions
{"players":[{"role":"A_out","x":0,"y":2},{"role":"B_out","x":-18,"y":22},{"role":"C_out","x":-22,"y":42},{"role":"D_out","x":18,"y":2},{"role":"A_in","x":0,"y":43},{"role":"B_in","x":7,"y":35},{"role":"D_in","x":-7,"y":35}],"actions":[{"from":"A_out","to":"B_out","type":"pass"},{"from":"A_in","to":"B_in","type":"pass"},{"from":"A_out","to":"A_in","type":"cut"},{"from":"A_in","to":"A_out","type":"cut"}],"notes":"Figure 19.1 shows two concentric groups. The outer group (outside 3PT arc) has: A at top center (~half-court), D at upper right, C at left baseline corner. The inner group (inside arc) has: A under the basket, B at A's right side, D at A's left side. The diagram labels are A, B, C, D for both groups; roles are suffixed _out and _in here to distinguish them. The outer C appears at the lower-left corner area. Both A players pass to their respective B players simultaneously (dashed pass arrows), then sprint to exchange positions with each other. Note: the diagram uses a full-court-like view compressed into a half-court page — the outer group's A is near half-court (top), D is upper-right, C is lower-left baseline; the inner group mirrors around the paint. Coordinates are approximated to the half-court viewBox."}
```

## Execution
1. Both A players simultaneously pass to their corresponding B player on the right
2. Both A players immediately sprint to exchange positions with the opposite A player (inner ↔ outer)
3. Play continues: B passes to C, C passes to D, each pair sprinting to exchange after their pass
4. Run for a set number of passes or a set time period
5. The drill can be reversed (passing left) for the return cycle

## Coaching Points
- Both groups must pass at exactly the same time — timing and communication matter
- Sprint immediately after the pass — no standing and watching
- Receiver must be ready on the catch before the passer releases
- Keep movements crisp; this is a warm-up but every detail counts
- "Stay low on the exchange sprint — don't straighten up mid-run"

## Progressions
1. **Beginner**: Walk through the pass sequence, then add the sprint
2. **Intermediate**: Game-speed passes and full-effort sprints
3. **Advanced**: Add a competition component — first group to complete X full rotations without a dropped pass wins

## Concepts Taught
- [[concept-pivot-and-pass-technique]] — catching and immediately transitioning to the next pass
- [[concept-player-development-philosophy-s7]] — high-rep, fast-paced warm-up philosophy

## Sources
- [S7, pp.306] — Kevin Eastman, Chapter 19: Player Development, Warm-Up Drills
