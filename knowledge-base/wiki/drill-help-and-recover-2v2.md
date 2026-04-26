---
type: drill
level: intermediate
positions: [PG, SG, SF, PF, C]
players_needed: 3-4
duration_minutes: 8-12
tags: [defense, help-defense, closeout, on-ball, penetration, 2v2]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
trains_techniques:
  - id: help-and-recover
    emphasis: primary
  - id: closeout
    emphasis: secondary
  - id: weak-side-help-defense
    emphasis: secondary
trains_anatomy:
  - region: hip_flexor_complex
    emphasis: secondary
  - region: glute_max
    emphasis: secondary
---

# Two-on-Two Help-and-Recover (the head coach)

## Objective
Train two defenders to execute the help-and-recover principle — one defender helps on dribble penetration while the other closes out to the open teammate — in both elbow-drive and middle-drive scenarios.

## Setup
- 2 offensive players, 2 defenders, 1 coach on the opposite wing
- Half court
- Two variations: Baseline Drive and Middle Drive

## Execution

### Variation A: Help-and-Recover (Elbow Drive)
1. 1 starts with the ball at the top of the key; 2 is outside the corner of the three-second lane; coach is on the opposite wing.
2. 1 **passes to the coach** and sprints to the **ball-side corner of the free-throw lane**.
3. 2 **moves toward the three-second lane**.
4. Coach passes back to 1:
   - X2 closes out on 1
   - X1 helps the helper (sinks toward the paint)
5. 1 **drives hard to the right elbow**.
6. X2 helps (stops the drive) and recovers back to 2 on 1's pass out to 2.
7. **Play live**.

```json name=diagram-positions
{"players":[{"role":"1","x":-2,"y":39},{"role":"2","x":18,"y":22},{"role":"x1","x":-5,"y":34},{"role":"x2","x":12,"y":22},{"role":"C","x":-22,"y":22}],"actions":[{"from":"C","to":"1","type":"pass"},{"from":"1","to":"right_elbow","type":"dribble"},{"from":"1","to":"2","type":"pass"},{"from":"x2","to":"2","type":"cut"}],"notes":"Figure 17.10 depicts the Two-on-Two Help-and-Recover (Elbow Drive) drill. The coach (C) is on the left wing (opposite wing). Player 1 is near the ball-side corner of the free-throw lane (bottom, slightly left of lane). Player 2 is on the right wing area. X1 is near the elbow/paint helping, X2 is closing out toward 2. Arrows show: coach passes back to 1, 1 drives to the right elbow, then kicks out to 2, with X2 recovering to 2. The starting formation shown is after the coach's pass-back to 1 (the moment 1 receives and is about to drive)."}
```

### Variation B: Help-and-Recover, Middle Drive
1. 1 starts with the ball at the top of the key; 2 is outside the corner of the three-second lane.
2. 1 **passes to the coach** and sprints to the **ball-side corner of the free-throw lane**.
3. 2 **moves toward the three-second lane**.
4. Coach passes back to 1:
   - X1 closes out on 1
   - X2 helps the helper
5. 1 **swings the ball to 2**, who drives hard to the **middle**.
6. X1 helps (on 2's drive) and recovers back to 1 (on the kick-out).
7. **Play live**.

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":38},{"role":"2","x":18,"y":22},{"role":"x1","x":2,"y":33},{"role":"x2","x":14,"y":20},{"role":"OB","x":-18,"y":22}],"actions":[{"from":"1","to":"OB","type":"pass"},{"from":"OB","to":"1","type":"pass"},{"from":"1","to":"2","type":"pass"},{"from":"2","to":"rim","type":"dribble"}],"notes":"Figure 17.11 (Variation B — Middle Drive). 1 is at the bottom of the key area (ball-side corner of free-throw lane after sprinting from top), 2 is on the right wing, coach (OB) is on the left wing. The diagram shows 1 passing to 2, who then drives hard to the middle. X1 is near the lane ready to help; X2 closes out on 2. Arrows depict the coach-to-1 pass back, then 1 swings to 2, and 2 drives middle."}
```

## Coaching Points
- **"Help the helper"** — when the first helper helps, the second defender sinks to support; no one is left stranded.
- **Close out under control** — the close-out on the kick-out pass must be high enough to contest the shot but not so aggressive that the ball handler can re-drive past.
- **Recovery angle** — on the help-and-recover, the recovering defender traces a straight line between the ball and their man, not around the drive.
- The difference between Variation A and B: in A, the ball handler drives AFTER receiving; in B, the ball is swung to a second player who then drives.
- **Play live after the predetermined trigger** — both variations end in live 2v2, so defenders must stay sharp through contact.

## Progressions
1. **Beginner**: Coach keeps the ball after the pass-back; 2-on-1 help-only (no live play).
2. **Intermediate**: Add live play as described.
3. **Advanced**: Add a third offensive player at the top for a 3-on-2 help-recover-rotate sequence.

## Concepts Taught
- [[weak-side-help-defense]] — the fundamental principle being drilled
- [[pick-and-roll-defense]] — help-and-recover is the core skill for navigating PnR ball movement
- [[drill-green-post-defense]] — companion defensive drill in Frank's practice
- [[concept-productive-practice-structure]] — embedded in Frank's daily practice

## Sources
- [S7, p.283] — the head coach, Two-on-Two Help-and-Recover drills (both variations), Figures 17.10-17.11
