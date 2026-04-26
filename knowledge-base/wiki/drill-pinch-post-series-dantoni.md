---
type: drill
level: intermediate
positions: [PF, C]
players_needed: 4-8
duration_minutes: 12-15
tags: [transition, fast-break, post, elbow, dribble-handoff, pick-and-roll, big-men, face-up]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
trains_techniques:
  - id: pinch-post-catch-and-read
    emphasis: primary
  - id: dribble-handoff
    emphasis: primary
  - id: face-up-jump-shot
    emphasis: secondary
  - id: pick-and-roll
    emphasis: secondary
  - id: elbow-drive-to-basket
    emphasis: secondary
trains_anatomy:
  - region: hip_flexor_complex
    emphasis: primary
  - region: glute_max
    emphasis: secondary
  - region: core_outer
    emphasis: secondary
---

# Pinch Post Series (D'Antoni Secondary Break)

## Objective
Train big men to catch at the pinch post (corner of the free-throw area/elbow), read a cutting defender, and choose between three secondary break finishes: drive-to-basket, face-up jump shot, or hand-off screen-and-roll.

## Setup
- Half court (run simultaneously on both halves)
- Two lines of players at the baseline facing midcourt — one line on each side; each player has a ball
- Two coaches positioned at the head of each line

## Execution

### Base Setup
1. First player of each line passes to the coach at the head of the line
2. Player posts up at the **corner of the free-throw area (elbow)** and receives the ball back
3. After the pass, the coach cuts around the player — acting as a defender and **trying to tip the ball**, creating a game situation
4. Player protects the ball, watches over their shoulder to locate the "defender," and reads the three finish options:

### Finish 1: Drive to Basket
- Player drives directly to the basket for a layup or dunk after faking a hand-off pass
- Protect the ball, watch over shoulder, then drive
- Both players (left and right lines) drive simultaneously — they must coordinate their paths to the basket [S7, p.173]

### Finish 2: Face-Up Jump Shot
- Player turns to face the basket from the elbow and takes a jump shot [S7, p.174]

### Finish 3: Hand-Off → Screen → Roll
- Player dribbles outside the lane toward the coach who has cut to the corner
- Player makes a hand-off pass to the coach
- Coach dribbles toward midcourt and passes back
- Player has rolled to the basket for a layup or dunk, or to the short corner for a jump shot [S7, pp.173–174]

### Finish 4: Hand-Off → Screen → Roll (Coach-Initiated)
- Player receives ball, makes hand-off pass to coach who dribbles toward the baseline
- Player **screens for the coach**, who dribbles toward midcourt and passes back to player
- Player rolls to basket for layup/dunk OR to short corner for jump shot [S7, p.174]

```json name=diagram-positions
{"players":[{"role":"C_left","x":-10,"y":29},{"role":"C_right","x":10,"y":29},{"role":"P1_left","x":-10,"y":44},{"role":"P2_left","x":-10,"y":46},{"role":"P1_right","x":10,"y":44},{"role":"P2_right","x":10,"y":46}],"actions":[{"from":"P1_left","to":"C_left","type":"pass"},{"from":"P1_right","to":"C_right","type":"pass"},{"from":"C_left","to":"rim","type":"dribble"},{"from":"C_right","to":"rim","type":"dribble"}],"notes":"Figure 10.21 (the first of the Pinch Post Series diagrams, pp.173–174) shows the starting formation for the Pinch Post Series drill. Two coaches (C) are positioned at the elbows/corners of the free-throw area (left and right), and two lines of players stand at the baseline behind each coach. The diagram depicts Finish 1 (drive to basket) and Finish 2 (face-up jump shot) simultaneously on both sides. The coaches at the elbows receive passes from the first player in each line, and then drive or shoot. Role labels follow the drill structure rather than numbered offensive roles, since this is a drill with coaches and player lines rather than a named-play formation. The C_left and C_right represent the coaches at the pinch-post elbows; the stacked player icons at the baseline represent the lines. Actions shown are the baseline players passing to coaches and the coaches driving to the rim."}
```

## Coaching Points
- The pinch post is a critical secondary break decision point — big men must read immediately after catching
- "As soon as the player receives the ball, he protects it, watching over his shoulder to get used to locating the defender" [S7, p.173]
- Running both lines simultaneously creates coordination pressure — players must see each other when driving simultaneously
- The hand-off action is a key pro team secondary break weapon — creates dribble penetration from the elbow that the defense is not set for
- Emphasis: big men here are NOT traditional post players. They face the basket, drive, and shoot from the outside. [S7, p.171]

## Progressions
1. **Beginner**: One finish per session — don't mix until each is mastered individually
2. **Intermediate**: Coach calls which finish at the moment of the catch; player must react
3. **Advanced**: Live coach-as-defender actually challenges the catch and the chosen finish — player must read and execute against real defensive pressure

## Concepts Taught
- [[concept-fast-break-primary-secondary-dantoni]] — elbow/pinch-post secondary break reads
- [[defending-dribble-handoff]] — defense against the hand-off action from the elbow
- [[concept-post-front-outside-pivot]] — face-up fundamentals off the elbow catch

## Sources
- [S7, pp.173–174] — D'Antoni, Gentry, Iavaroni: Pinch Post Series Drill
