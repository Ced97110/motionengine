---
type: drill
level: intermediate
positions: [PF, C]
players_needed: 4-8
duration_minutes: 10-12
tags: [transition, fast-break, screening, pick-and-roll, big-men, post]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
trains_techniques:
  - id: stagger-screen
    emphasis: primary
  - id: pick-and-roll
    emphasis: primary
  - id: secondary-break
    emphasis: secondary
  - id: pop-action
    emphasis: secondary
trains_anatomy:
  - region: hip_flexor_complex
    emphasis: primary
  - region: glute_max
    emphasis: secondary
  - region: core_outer
    emphasis: secondary
---

# Double Drag Drill (D'Antoni Secondary Break)

## Objective
Train big men to set a stagger screen ("double drag") for the ball handler on the secondary break, with one player rolling to the basket for a layup/dunk and the other popping outside for a jump shot.

## Setup
- Half court
- One coach positioned on the perimeter (wing area)
- One coach at the free-throw line
- Line of big men (PF/C) at the middle of the half-court, each with a ball

## Execution
1. First player in line passes the ball to the coach on the perimeter
2. Second player in line passes the ball to the coach at the free-throw line
3. The two big men then **set a stagger screen** ("double drag") for the coach on the perimeter
4. **First player** (first screener): picks and rolls to the basket → receives a pass from the coach at the free-throw line → shoots a layup or dunk
5. **Second player** (second screener): after setting the second screen for the coach outside the three-second lane, pops out → receives the ball from the coach on the perimeter → shoots from outside [S7, p.172]
6. Rotate players; run continuously

```json name=diagram-positions
{"players":[{"role":"C1","x":-14,"y":22},{"role":"C2","x":0,"y":29},{"role":"P1","x":-7,"y":37},{"role":"P2","x":-3,"y":40},{"role":"P3","x":0,"y":43},{"role":"P4","x":3,"y":46}],"actions":[{"from":"P1","to":"C1","type":"pass"},{"from":"P2","to":"C2","type":"pass"},{"from":"P1","to":"C1","type":"screen"},{"from":"P2","to":"C1","type":"screen"},{"from":"P1","to":"rim","type":"cut"},{"from":"P2","to":"left_wing","type":"cut"}],"notes":"Figure 10.16 shows the Double Drag Drill. Two coaches are present: C1 on the left perimeter/wing (~left wing area) and C2 at the free-throw line. A line of big men (P1, P2, and additional players waiting) is positioned at/below the half-court line in the middle. P1 (first player) passes to C1 on the perimeter, P2 (second player) passes to C2 at the free-throw line. The two bigs then set a stagger screen for C1: P1 screens first then rolls to the basket (shown with arrow toward the rim), P2 sets the second screen then pops out to receive from C1. The waiting line players (P3, P4) are stacked behind in the middle. Role labels are adapted as coach/player since the drill uses \"C\" for coach and numbered players for big men — numeric roles used here for structural clarity."}
```

## Coaching Points
- The stagger (double drag) is the standard pro team secondary break action when two trailers arrive simultaneously
- First screener must sprint the roll immediately after contact — don't admire the screen
- Second screener must pop to an open shooting position — not drift to a covered spot
- Both players must arrive and set screens in proper sequence without getting in each other's way
- The coaches simulate the ball handler being shadowed to the sideline — the double drag gets them free

## Progressions
1. **Beginner**: Walk through positions and roll/pop angles without live passes
2. **Intermediate**: Live execution with passes as described; both big men score at their assigned spot
3. **Advanced**: Add a third player as a live dribbling ball handler; first and second trailer set stagger for them in real transition tempo

## Concepts Taught
- [[concept-fast-break-primary-secondary-dantoni]] — secondary break trailer options and stagger screen action
- [[defending-staggered-screens]] — how opponents defend this action

## Sources
- [S7, p.172] — D'Antoni, Gentry, Iavaroni: Double Drag Drill
