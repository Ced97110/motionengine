---
type: drill
level: intermediate
positions: [PG, SG, SF, PF, C]
players_needed: 2
duration_minutes: 10-20
tags: [shooting, scoring, footwork, conditioning, game-situations, layup, jump-shot, chair-drills]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
trains_techniques:
  - id: catch-and-shoot-footwork
    emphasis: primary
  - id: square-up-mechanics
    emphasis: primary
  - id: shooting-off-screens
    emphasis: secondary
  - id: low-to-high-shooting
    emphasis: secondary
  - id: two-count-stop
    emphasis: secondary
trains_anatomy:
  - region: hip_flexor_complex
    emphasis: primary
  - region: ankle_complex
    emphasis: secondary
  - region: core_outer
    emphasis: secondary
---

# Chair Drill Series (Kevin Eastman)

## Objective
Develop game-realistic footwork, ball pickup, square-up mechanics, and shot execution using chairs with balls — forcing players to stay low on the approach and rise properly into every shot.

## Setup
- Various configurations on half court (described per drill)
- One ball per chair
- One rebounder in the lane
- Note: Chairs with balls force players to pick up the ball from a low position, reinforcing the "low to high" principle

## Execution

### Intensity Layup
1. Two chairs at the elbows, one ball each. Rebounder under basket.
2. Player starts at mid-lane. Cuts outside the right chair, picks up ball, makes a layup.
3. Cuts out of the lane, around the left chair, picks up ball, makes a layup on the left side.
4. **Goal: 4 layups in 15 seconds.** Rebounder replaces balls on chairs.
<!-- DIAGRAM: Figure 19.9 -- needs visual extraction, p.308 -->

### Elbow Jump Shot
1. Same setup as Intensity Layup.
2. Player fakes going left, then cuts right-side of the chair, picks up ball, squares up, takes a jump shot.
3. Continues to the other chair on the left side. Set number of shots or time.
<!-- DIAGRAM: Figure 19.10 -- needs visual extraction, p.309 -->

### Reverse Elbow Pick-Up
1. Same setup as Elbow Jump Shot.
2. Player cuts to the right side of the chair, goes *past* it, stops, reverse pivots, comes off the other side of the chair, picks up ball, and shoots.
3. Continues on the left side. Set number of shots or time.
<!-- DIAGRAM: Figure 19.11 -- needs visual extraction, p.309 -->

### Four Chairs
1. Two chairs just inside the 3PT arc near the baseline; two more just outside the elbows. One ball per chair, one rebounder in the lane.
2. Player starts at low post. Cuts to Chair 1, picks up ball, squares to basket, shoots.
3. Repeats at Chairs 2, 3, and 4 in sequence.
<!-- DIAGRAM: Figures 19.12a-b -- needs visual extraction, p.309 -->

### Pin-Down, Pull-Up
1. One chair (with ball) on the wing; one chair in the central lane. Rebounder in lane.
2. Player at low post fakes a cut inside, sprints to the wing chair, picks up ball, squares up, shoots.
3. Sprints to midcourt line, touches it with one foot, sprints back to the other chair, picks up ball, squares up, shoots again.
4. Run for set shots or set time.
```json name=diagram-positions
{"players":[{"role":"1","x":-7,"y":40},{"role":"R","x":-3,"y":32},{"role":"C_wing","x":18,"y":22}],"actions":[{"from":"1","to":"C_wing","type":"cut"},{"from":"C_wing","to":"rim","type":"cut"}],"notes":"Figure 19.13 (Pin-Down, Pull-Up drill). The diagram shows a player starting at the left low-post position (left low block area). One chair with ball is on the right wing (~18, 22) and another chair is in the central lane near the free-throw line area (~0, 29). A rebounder (R) is in the lane. The player's path: fakes inside, sprints to the wing chair (right wing), picks up ball, squares up and shoots; then sprints to midcourt and back to the central lane chair. Chair positions are labeled as approximate landmarks. The \"C_wing\" role represents the wing chair position and \"C_lane\" the lane chair — no actual labeled offensive player numbers are used in this individual drill diagram beyond the single player (1) and rebounder (R)."}
```

### Dribble Intos
1. Three chairs form a tight triangle at the free-throw line. One rebounder in lane.
2. Player starts outside the 3PT arc with a ball. Dribbles fast into the chairs, makes a two-count stop under control, pulls up, and shoots a jump shot.
3. Can be run on either side of the half-court.
```json name=diagram-positions
{"players":[{"role":"1","x":-10,"y":18},{"role":"R","x":-3,"y":38},{"role":"C1","x":0,"y":29},{"role":"C2","x":-4,"y":32},{"role":"C3","x":4,"y":32}],"actions":[{"from":"1","to":"right_elbow","type":"dribble"}],"notes":"Figure 19.14: Dribble Intos drill. Three chairs (C1, C2, C3) are arranged in a tight triangle at/around the free-throw line area. The player (1) starts outside the 3PT arc and dribbles into the chair triangle, making a two-count stop and pulling up for a jump shot. The rebounder (R) is in the lane. Chair markers are represented as 'h' symbols in the diagram. Player starts on the left side of the arc in the diagram. The diagram is somewhat small but shows the player with a dribble arrow leading into the cluster of three chairs near the free-throw line, with the rebounder positioned in the lane below the chairs."}
```

### Cut Intos
1. Three chairs just outside the left elbow. Coach outside 3PT arc with ball. Rebounder in lane.
2. Player fakes a cut to the basket, then cuts into the chairs. Coach delivers pass. Player makes a two-count stop and takes a jump shot.
3. Make 5 shots, then repeat on the other side.
```json name=diagram-positions
{"players":[{"role":"C","x":-20,"y":29},{"role":"R","x":2,"y":37},{"role":"1","x":-5,"y":32}],"actions":[{"from":"C","to":"1","type":"pass"},{"from":"1","to":"left_elbow","type":"cut"}],"notes":"Figure 19.15 — Cut Intos drill. The diagram shows a coach (C) outside the 3PT arc on the left side, a rebounder (R) in the lane near the basket, and a player (1) cutting from the right lane area into the chairs set just outside the left elbow. Three chairs form a cluster just outside the left elbow (~-8, 29). The coach passes to the player who cuts into the chairs, makes a two-count stop, and shoots. The player's starting position appears to be opposite (right side of lane), and the cut goes left toward the elbow chair cluster. Actions show the coach's pass and the player's cut direction."}
```

### Figure-8 Shooting
1. One chair outside the right elbow, one near the baseline inside the 3PT arc. One ball each, rebounder in lane.
2. Player starts outside the 3PT arc between the two chairs. Cuts around the baseline chair, picks up ball, squares up, shoots.
3. Loops over that chair, sprints to the elbow chair, picks up ball, squares up, shoots.
4. Continues figure-8 for set shots or time, then repeats on the other side.
```json name=diagram-positions
{"players":[{"role":"1","x":-2,"y":14},{"role":"R","x":-5,"y":35},{"role":"chair_baseline","x":5,"y":41},{"role":"chair_elbow","x":8,"y":29}],"actions":[{"from":"1","to":"chair_baseline","type":"cut"},{"from":"chair_baseline","to":"chair_elbow","type":"cut"}],"notes":"Figure 19.16: Figure-8 Shooting drill. The player (labeled as starting position between the two chairs outside the 3PT arc) is shown on the right side of the court. One chair is outside the right elbow (~right elbow area) and one near the baseline inside the 3PT arc (right baseline area). The rebounder (R) is in the lane. The figure-8 movement arrows show the player cutting around the baseline chair first, then looping up to the elbow chair. Chair positions are approximated from the diagram; they are not labeled as numbered players but as drill props. Player start position is approximated near the top of the key / right side outside the arc."}
```

### Flare Screen Shooting
1. Two chairs on the right side near the 3PT arc. One ball each, rebounder in lane.
2. Player starts from the central lane, cuts off an imaginary flare screen, picks up ball at first chair, squares up, shoots.
3. Sprints to the second chair, shoots again. Repeats for set shots or time, then on the other side.
```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":8},{"role":"R","x":-3,"y":30},{"role":"C1","x":10,"y":22},{"role":"C2","x":10,"y":14}],"actions":[{"from":"1","to":"C1","type":"cut"},{"from":"C1","to":"C2","type":"cut"}],"notes":"Figure 19.17 Flare Screen Shooting drill. The diagram shows a player (1) starting near the central lane of the half-court (top of key area), cutting rightward off an imaginary flare screen toward two chairs positioned on the right side near the 3PT arc — one roughly at the right wing (~right elbow extended toward arc) and one further out/back. The rebounder (R) is in the lane near the left elbow area. No ball-handler/coach is explicitly shown as a separate role; the balls are on the chairs. The player's cut path goes from the central lane to chair 1 (right wing near arc), then to chair 2 (further right/back near arc). Exact chair positions approximated from the diagram: chair 1 near right wing arc (~10, 22), chair 2 further right and slightly higher (~10, 14)."}
```

## Coaching Points
- The purpose of chairs with balls: **forces players to stay low as they approach** and pick up the ball before rising into the shot — "play low to high"
- Require a true square-up on every shot — no rushed releases
- On Intensity Layup: emphasize aggressive cuts, soft finishes
- On Dribble Intos: the two-count stop must be under control — no drift, no lean
- On Cut Intos: the fake must look like a real cut to the basket before redirecting
- On Flare Screen Shooting: simulate a real flare — shoulder-to-shoulder off the screen, come out balanced
- Chart makes and misses on all chair drills [S7, pp.308-311]

## Progressions
1. **Beginner:** Walk-through on each drill pattern; use only 1-2 chairs to start
2. **Intermediate:** Game-speed reps; timed goals (e.g., 4 layups in 15 sec)
3. **Advanced:** Add passive defender trailing the cut; coach varies pass timing

## Concepts Taught
- [[concept-player-development-philosophy-eastman]] — game-speed low-to-high mechanics
- [[concept-shooting-off-screens-s3]] — flare screen shooting reads
- [[concept-one-two-step-footwork]] — catch-and-shoot footwork on all chair drills
- [[concept-pivot-footwork]] — square-up pivot on every ball pickup

## Sources
- [S7, pp.308-311] — Kevin Eastman, Chapter 19: Player Development
