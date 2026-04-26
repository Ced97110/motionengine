---
type: drill
level: intermediate
positions: [PF, C, PG]
players_needed: 4-8
duration_minutes: 8-12
tags: [transition, fast-break, dribble-handoff, pick-and-roll, big-men]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
trains_techniques:
  - id: dribble-handoff
    emphasis: primary
  - id: screen-and-roll
    emphasis: primary
  - id: secondary-break
    emphasis: secondary
trains_anatomy:
  - region: hip_flexor_complex
    emphasis: primary
  - region: glute_max
    emphasis: secondary
  - region: ankle_complex
    emphasis: secondary
---

# Dribble Drags Drill (D'Antoni Secondary Break)

## Objective
Train the dribble hand-off and immediate screen-and-roll used by big men in the pro team secondary break — the "dribble drag" action that frees a big man rolling to the basket.

## Setup
- Half court
- One coach in the corner **without the ball**
- One coach **with the ball** on the same side outside the three-point line
- Line of players (primarily big men) ready to enter the action

## Execution
1. Coach with the ball starts to dribble toward the other coach (who comes high to receive a hand-off)
2. Dribbling coach hands off to the cutting coach, who receives while coming high
3. The first player in line makes a **screen for the receiving coach** (second coach, now with ball)
4. After screening, the player **rolls to the basket** → receives a pass from the coach who dribbled around the screen → finishes with layup or dunk [S7, p.172]
5. Rotate players continuously

```json name=diagram-positions
{"players":[{"role":"C1","x":-18,"y":8},{"role":"C2","x":-18,"y":42},{"role":"1","x":0,"y":4},{"role":"2","x":0,"y":10},{"role":"3","x":0,"y":16}],"actions":[{"from":"C1","to":"C2","type":"dribble"},{"from":"C1","to":"C2","type":"handoff"},{"from":"1","to":"C2","type":"screen"},{"from":"1","to":"rim","type":"cut"}],"notes":"Figure 10.17 shows two coaches (C1 with ball on the left wing/perimeter outside the arc, C2 in the left corner without ball) and a line of players stacked near the half-court center. C1 dribbles toward C2, who comes high to receive a handoff. The first player in line screens for C2 (now with ball), then rolls to the basket. Roles labeled as C1/C2 for coaches and 1/2/3 for the player line. The diagram is on the right side of the page and uses the left side of the court. Exact pixel positions are approximated from the scan."}
```

## Coaching Points
- The hand-off is a deceptive action — the cutter comes high at the right moment so the hand-off flows naturally
- The screening player must execute a legal, solid screen before rolling — no early rolling
- Roll is to the **ball-side** basket; player must feel where the ball is coming from and cut to that angle
- Coach acting as ball handler simulates dribbling *around* the screen — player must time the screen so the coach can use it
- This drill trains the same dribble-drag action that secondary break trailers use when the point guard is pressured to the sideline

## Progressions
1. **Beginner**: Walk-through hand-off and roll angles
2. **Intermediate**: Live speed with coaches; player finishes at the rim
3. **Advanced**: Add a live defensive player to contest the roll — player must read whether to roll to basket or slip to short corner

## Concepts Taught
- [[concept-fast-break-primary-secondary-dantoni]] — secondary break dribble drag and trailer screen-roll
- [[defending-dribble-handoff]] — defensive principles against this action

## Sources
- [S7, p.172] — D'Antoni, Gentry, Iavaroni: Dribble Drags Drill
