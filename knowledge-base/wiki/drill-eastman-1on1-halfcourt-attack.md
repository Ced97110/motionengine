---
type: drill
level: advanced
positions: [PG, SG, SF, PF, C]
players_needed: 3
duration_minutes: 10-15
tags: [1on1, attacking-the-rim, dribble-penetration, defensive-recovery, conditioning, competition]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
trains_techniques:
  - id: dribble-penetration
    emphasis: primary
  - id: attacking-the-rim
    emphasis: primary
  - id: defensive-recovery
    emphasis: secondary
  - id: explosive-first-step
    emphasis: secondary
trains_anatomy:
  - region: hip_flexor_complex
    emphasis: primary
  - region: glute_max
    emphasis: secondary
  - region: ankle_complex
    emphasis: secondary
---

# One-on-One Half-Court Attack Drill

## Objective
Develop full-court dribble-attack skills under pressure by having the offense curl around a chair toward the rim while the defense races a parallel path to beat them to the inside spot.

## Setup
- Full half-court to mid-court area
- Two chairs set a few feet from the mid-court line (one on each side of the lane)
- Offensive player with ball: starts in the corner near the baseline and sideline
- Defender: starts near the lane on the opposite side

```json name=diagram-positions
{"players":[{"role":"O","x":22,"y":42},{"role":"X","x":5,"y":8},{"role":"h","x":8,"y":2},{"role":"h2","x":-4,"y":2}],"actions":[{"from":"O","to":"rim","type":"dribble"}],"notes":"Figure 19.20 shows a half-court diagram oriented from mid-court down to the baseline. The offensive player (O, with ball) starts in the right corner near the baseline/sideline (~right corner). The defender (X) starts near the top of the key/lane area closer to mid-court. Two chairs (marked 'h') are positioned a few feet from the mid-court line — one slightly right of center, one left of center. The dribble arrow shows the offense curling from the corner around the near chair toward the rim. The diagram is partially cut off on the right side but the key elements are visible. Role labels 'h2' used for the second chair for disambiguation."}
```

## Execution
1. Coach yells "Go!"
2. Offensive player dribbles hard, curls around the chair in front of them, and attacks the rim
3. Defender simultaneously runs around the other chair and tries to beat the offensive player to the inside spot
4. Players compete 1-on-1 until the offensive player scores or the defender gets the ball

## Coaching Points
- Offensive player must attack with maximum intent — no passive dribbling
- "Curl tight around the chair — don't drift wide or you lose the angle"
- Defender must run hard — the goal is to take away the inside, not just react
- Offense reads the defender's position on the curl and decides to attack inside or pull up
- This drill simulates a defender recovering on a fast break or after a beat — attack the advantage while you have it

## Progressions
1. **Beginner**: Both players start at half-court facing each other; offense dribbles toward the basket, defense recovers from mid-court
2. **Intermediate**: Full drill as described — chairs create curved paths
3. **Advanced**: Add a second defender who starts under the basket; offense must read two defenders

## Concepts Taught
- [[concept-player-development-philosophy-s7]] — competitive game-speed 1-on-1 drill
- [[concept-dribbling-driving-techniques]] — attacking the rim off the dribble
- [[concept-first-step-quickness]] — initial acceleration toward the basket

## Sources
- [S7, p.312] — Kevin Eastman, Chapter 19: One-on-One Drills
