---
type: drill
level: beginner
positions: [PG, SG, SF]
players_needed: 3
duration_minutes: 5-10
tags: [passing, cutting, driving, finishing, warm-up]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
trains_techniques:
  - id: pass-and-follow
    emphasis: primary
  - id: player-replacement-movement
    emphasis: primary
  - id: drive-and-finish
    emphasis: secondary
  - id: pivot-footwork
    emphasis: secondary
trains_anatomy:
  - region: hip_flexor_complex
    emphasis: primary
  - region: ankle_complex
    emphasis: secondary
  - region: core_outer
    emphasis: secondary
---

# Reverse, Replace, and Drive (Shoot) Drill

## Objective
Develop pass-and-follow movement, player replacement principles, and finishing at the rim in a continuous flowing sequence.

## Setup
- Half court, left wing
- Line of players on left wing, each with a ball
- One player positioned at the middle of the half-court (top of key area)
- One player stationed at the wing

```json name=diagram-positions
{"players":[{"role":"1","x":-22,"y":22},{"role":"2","x":-18,"y":35},{"role":"3","x":0,"y":10}],"actions":[{"from":"1","to":"3","type":"pass"},{"from":"1","to":"3","type":"cut"},{"from":"3","to":"2","type":"pass"},{"from":"3","to":"2","type":"cut"},{"from":"2","to":"rim","type":"dribble"}],"notes":"Figure 19.3 shows three players: a line on the left wing (Player 1 / first in line, approximated at left wing area), a player at top of key / middle of half-court (Player 3), and a player at the left wing spot (Player 2). Arrows show: line player passes to middle, follows pass (cut) to replace middle; middle player passes to wing, cuts to replace wing; wing player drives (dribble) to the basket. The diagram is a small half-court schematic with wavy dribble arrows toward the rim and straight pass arrows. Player positions are approximated from the prose and diagram scan."}
```

## Execution
1. First player in line passes the ball to the player at the middle of the court.
2. The passer follows the pass and replaces the middle player.
3. The middle player immediately passes the ball to the wing player and replaces the wing.
4. The wing player **drives to the basket** and finishes a layup (Drive version) or receives the pass and shoots a jump shot (Shoot version).
5. The drill runs for a set number of shots or a set time, then repeats on the right side.

**Shoot variation:** The wing player catches the pass and takes a jump shot instead of driving.

## Coaching Points
- "Reverse, replace" — every passer must immediately move to fill the spot they just passed to
- Drive version: attack the rim with purpose, finish through contact
- Shoot version: use proper one-two step footwork, freeze the follow-through
- Coach corrects *every* mistake during warm-up versions — precision matters from the first rep
- Attend to every small detail: footwork on the drive, body position on the catch [S7, p.307]

## Progressions
1. **Beginner:** Walk through the pass-replace sequence before adding the drive/shot
2. **Intermediate:** Add a defensive token (passive) on the wing to simulate a contested finish
3. **Advanced:** Live 1-on-1 after the wing catches — the middle-player-turned-wing now defends

## Concepts Taught
- [[concept-player-development-philosophy-eastman]] — game-speed, precise movement in every rep
- [[concept-pivot-footwork]] — footwork on wing catch and drive

## Sources
- [S7, pp.306-307] — Kevin Eastman, Chapter 19: Player Development
