---
type: drill
level: intermediate
positions: [PG, SG, SF]
players_needed: 2
duration_minutes: 5-10
tags: [shooting, footwork, reaction, pivoting, catch-and-shoot, jump-shot]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
trains_techniques:
  - id: pivot-footwork
    emphasis: primary
  - id: catch-and-shoot
    emphasis: primary
  - id: shot-fake
    emphasis: secondary
  - id: crossover-dribble
    emphasis: secondary
trains_anatomy:
  - region: hip_flexor_complex
    emphasis: primary
  - region: ankle_complex
    emphasis: secondary
  - region: core_outer
    emphasis: secondary
---

# Quick Square-Ups Drill

## Objective
Build reactive pivot and square-up footwork by forcing players to process a directional command during the flight of the pass.

## Setup
- Half court, inside the 3PT arc
- Coach with ball at the half-court line, outside the 3PT arc
- Player facing the coach inside the arc

```json name=diagram-positions
{"players":[{"role":"C","x":0,"y":47},{"role":"1","x":0,"y":22}],"actions":[{"from":"C","to":"1","type":"pass"}],"notes":"Figure 19.7 shows two participants: the Coach (C) positioned at the baseline/under the basket area (acting as the passer from outside the 3PT arc near half-court per prose, but the diagram places C at the bottom near the baseline/free-throw area), and a Player (1) inside the arc near the top of the key. The diagram shows a pass from C upward to the player, with arrows radiating outward from the player indicating pivot/square-up directions (right and left). The coach in the diagram appears to be placed roughly at the free-throw line area or just below, not literally at half-court — the coordinate is approximated from the diagram's visual placement. Action arrows from the player show the pivot square-up motion but no additional pass or cut targets beyond the catch-and-shoot action."}
```

## Execution
1. Coach passes the ball to the player.
2. While the ball is in the air, the coach yells **"Right!"** or **"Left!"**
3. If "Right!" — player pivots on the right foot, squares up, and shoots.
4. If "Left!" — player pivots on the left foot, squares up, and shoots.
5. Run for a set number of shots or a set time.

**While pivoting and squaring up:**
- Stay low; then rise from the legs into the shot
- Bring the ball up on the side between the shoulder and chin (right side for right-handers)
- Wrists of the shooting hand are bent back before the shot

### Quick Square-Ups and Crossovers (Variation)
- Same setup, but after squaring up, the player **fakes a shot**, makes a crossover dribble, and pulls up for a jump shot.
- During the crossover: sweep the ball quickly *below the knees*, make a lateral "pound" dribble so the ball returns quickly to the hands.
- Watch for players who don't commit to a true shot fake — demand a convincing fake. [S7, p.308]

## Coaching Points
- The command must come *while the ball is in the air* — no time to think, only react
- "Stay low, square up, then rise into the shot" — not the other way around
- Ball side matches shooting hand: right shoulder-chin for righties, left for lefties
- Crossover version: the shot fake must be convincing, not a head-bob
- Sweep the crossover dribble below the knees for ball security [S7, p.308]

## Progressions
1. **Beginner:** Coach calls direction *before* passing so player can prepare
2. **Intermediate:** Call during flight (standard version)
3. **Advanced:** Quick Square-Ups and Crossovers — add a live passive defender on the crossover

## Concepts Taught
- [[concept-pivot-footwork]] — reactive pivot mechanics on catch
- [[concept-player-development-philosophy-eastman]] — low-to-high game-speed shooting
- [[concept-shot-fake-step-fake]] — shot fake in the crossover variation

## Sources
- [S7, p.308] — Kevin Eastman, Chapter 19: Player Development
