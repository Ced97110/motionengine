---
type: drill
level: intermediate
positions: [PG, SG, SF, PF, C]
players_needed: 2
duration_minutes: 15-20
tags: [shooting, footwork, cutting, chair-drills, game-speed, conditioning, layup, jump-shot]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
trains_techniques:
  - id: catch-and-shoot-footwork
    emphasis: primary
  - id: low-to-high-shooting-mechanic
    emphasis: primary
  - id: shot-ready-position
    emphasis: secondary
  - id: reverse-pivot
    emphasis: secondary
  - id: v-cut-footwork
    emphasis: secondary
trains_anatomy:
  - region: hip_flexor_complex
    emphasis: primary
  - region: ankle_complex
    emphasis: secondary
  - region: core_outer
    emphasis: secondary
---

# Eastman Chair Shooting Drill Series

## Objective
Use chairs with basketballs placed on them to force players to lower their center of gravity as they pick up the ball before shooting — simulating the "low-to-high" game mechanic and building catch-and-shoot footwork from varied spots and angles.

## Setup
- Half-court
- Chairs with a ball on each (number varies by drill)
- 1 rebounder in the lane
- 1 player working; a coach or manager as feeder when needed
- **Chair placement rationale**: chairs force players to "focus better and get down low as they come into their shots" [S7, p.305]

---

## Drill 1: Intensity Layup
**Setup**: Two chairs at the elbows, one ball each; rebounder under the basket; player starts in the middle of the floor.

**Execution**:
1. Player cuts outside the right-side chair, picks up the ball, and makes a layup
2. Cuts out of the lane and around the left-side chair, picks up the ball, makes a layup on the left side
3. Goal: 4 layups in 15 seconds
4. Rebounder puts balls back on chairs between reps

```json name=diagram-positions
{"players":[{"role":"h","x":-8,"y":29},{"role":"h","x":8,"y":29},{"role":"R","x":0,"y":41},{"role":"1","x":0,"y":24}],"actions":[{"from":"1","to":"h","type":"cut"},{"from":"1","to":"rim","type":"cut"}],"notes":"The PDF page does not contain a basketball court diagram for Figure 19.9 — it shows only a photo of coaches drilling players and introductory text. Positions and actions have been reconstructed from the verbatim diagram marker and surrounding wiki prose: two chairs (h) at the left and right elbows (~(-8,29) and (8,29)), a rebounder (R) under the basket (~(0,41)), and a player (1) starting in the middle of the floor around the top of the key (~(0,24)). The figure-8 cut pattern is represented by two representative action arrows (cut toward a chair, then cut to the rim). This is a best-effort approximation; no actual court diagram was present on the provided PDF page."}
```

---

## Drill 2: Elbow Jump Shot
**Setup**: Same as Intensity Layup.

**Execution**:
1. Player fakes to go to the left side
2. Cuts to the right side of the chair, picks up the ball, squares up, and takes a jump shot
3. Repeats on the left side
4. Run for a set number of shots or set time

```json name=diagram-positions
{"players":[{"role":"R","x":0,"y":41},{"role":"1","x":6,"y":22}],"actions":[{"from":"1","to":"left_elbow","type":"cut"},{"from":"1","to":"right_elbow","type":"cut"}],"notes":"The PDF page (p.305) contains only a photograph of players practicing and introductory prose — no court diagram for Figure 19.10 is visible on this page. The diagram for Drill 2 (Elbow Jump Shot) is not rendered here. Based on the wiki prose and the described setup (same two-chair layout as Drill 1: chairs at the elbows, rebounder under basket, player on the floor), the starting formation has been approximated accordingly. Chair markers (h) are not player roles but are noted at left elbow (~-8,29) and right elbow (~8,29). The player starts near the top of the key and makes a fake cut to one side before a hard cut to the real side."}
```

---

## Drill 3: Reverse Elbow Pick-Up
**Setup**: Same as Elbow Jump Shot.

**Execution**:
1. Player cuts to the right side of the chair, going past it
2. Player **stops**, executes a **reverse pivot**, comes off the other side of the chair
3. Picks up the ball, squares up, and shoots
4. Repeats on the left side

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":20},{"role":"R","x":0,"y":41}],"actions":[{"from":"1","to":"right_elbow","type":"cut"},{"from":"1","to":"left_elbow","type":"cut"}],"notes":"Page 305 contains only a photograph of players at practice and prose text — no court diagram is visible. The wiki marker references Figure 19.9 (Intensity Layup / two-chair setup). Based on the drill description, the starting formation shows: player (1) in the middle of the floor near the top of the key, rebounder (R) under the basket, and two chairs (not represented as players) at the left and right elbows. The figure-8 cutting pattern goes right elbow first, then left elbow. No actual diagram scan was provided; coordinates are inferred from prose description only."}
```

---

## Drill 4: Four Chairs
**Setup**: 4 chairs — 2 just inside the 3PT arc near the baseline, 2 just outside the two elbows; 1 ball per chair; 1 rebounder in lane; player starts at the low post.

**Execution**:
1. Player cuts to Chair 1 (baseline area), picks up the ball, squares to basket, shoots
2. Immediately cuts to Chair 2, then Chair 3, then Chair 4
3. Cover all 4 spots in sequence

<!-- DIAGRAM: Figures 19.12a and 19.12b show 4 chairs in a perimeter arc (1 = left baseline, 2 = right baseline, 3 = left elbow-area, 4 = right elbow-area), with rebounder in the middle and player cycling through in order. -->

---

## Drill 5: Figure-8 Shooting
**Setup**: 1 chair outside the right elbow, 1 chair near the baseline inside the 3PT arc; 1 ball each; 1 rebounder.

**Execution**:
1. Player starts between the two chairs outside the arc
2. Cuts around the baseline chair, picks up ball, squares up, jump shot
3. Loops over that chair, sprints to the elbow chair, picks up ball, squares up, jump shot
4. Continues in a figure-8 pattern for set reps or time
5. Repeat on the other side of the floor

```json name=diagram-positions
{"players":[{"role":"R","x":-3,"y":30},{"role":"P","x":3,"y":37},{"role":"chair1","x":8,"y":29},{"role":"chair2","x":3,"y":40}],"actions":[{"from":"P","to":"chair2","type":"cut"},{"from":"chair2","to":"chair1","type":"cut"}],"notes":"Figure 19.16 shows the Figure-8 Shooting drill. The rebounder (R) is positioned near the top of the key/lane area (~-3, 30). One chair is just outside the right elbow (~8, 29) and another near the right baseline inside the 3PT arc (~3, 40). The player starts between the two chairs outside the arc. The figure-8 cutting pattern loops around the baseline chair first, then up to the elbow chair. Chairs are represented as positions rather than players; the player's starting position is approximated between the two chairs. The diagram is on the right side of the court as described."}
```

---

## Drill 6: Flare Screen Shooting
**Setup**: 2 chairs on the right side near the 3PT arc, 1 ball each; 1 rebounder.

**Execution**:
1. Player starts from the central lane at half-court
2. Cuts off an **imaginary flare screen**, picks up ball from Chair 1, squares up, jump shot
3. Sprints to Chair 2, picks up ball, shoots
4. Continues for set reps or time
5. Repeat on the left side of the floor

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":5},{"role":"R","x":-3,"y":37},{"role":"C1","x":14,"y":22},{"role":"C2","x":14,"y":36}],"actions":[{"from":"1","to":"C1","type":"cut"},{"from":"C1","to":"C2","type":"cut"}],"notes":"Figure 19.17 — Flare Screen Shooting drill. The player (1) starts at the central lane near half-court and cuts in a flare-screen arc toward two chairs on the right side of the court near the 3PT arc. Chair 1 (C1) is roughly at the right wing (~14, 22) and Chair 2 (C2) is further right and closer to baseline (~14, 36). The rebounder (R) is in the lane just left of the rim. The cutting path curves outward (flare arc) from the lane toward the right arc chairs. No coach/passer is depicted in figure 19.17 itself — the player picks up the ball from the chairs directly."}
```

---

## Coaching Points (All Drills)
- Chairs build the habit of getting low before picking up the ball — do not reach down lazily
- "Perfect feet" on every shot — same mechanics regardless of approach angle
- Stay low through the cut, rise naturally into the shot
- Square up to the basket fully before shooting — not partial squares
- Rebounder must be active — put balls back on chairs immediately
- Coach corrects foot position, follow-through, and pivot on every rep

## Progressions
1. **Beginner**: Slow approach to each chair, emphasis on footwork and square-up
2. **Intermediate**: Game-speed approaches with precise shooting mechanics
3. **Advanced**: Add a time goal (e.g., 4 layups in 15 sec, as in Intensity Layup) or a makes-before-moving threshold

## Concepts Taught
- [[concept-player-development-philosophy-s7]] — low-to-high play, feet first philosophy
- [[concept-shooting-off-the-move-footwork]] — inside-heel pivot and square-up mechanics
- [[concept-v-cut-footwork]] — deception before the cut to the chair
- [[shot-ready-position]] — being in shooting position before the catch/pick-up

## Sources
- [S7, pp.308-311] — Kevin Eastman, Chapter 19: Chair Drills
