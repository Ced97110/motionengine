---
type: concept
level: intermediate
positions: [PG, SG, SF, PF, C]
tags: [offense, transition, fast-break, flex, lane-filling, Argentina]
source_count: 1
last_updated: 2026-04-11
---

# Flex Offense — Transition Game and Setup

## Summary
the head coach (Argentina national team, a pro team connection through a pro player) teaches that the flex offense must be preceded by aggressive defense and fast transition. The offense begins the moment possession is gained, with players filling specific lanes to create overload fast-break opportunities before settling into the half-court flex formation. The transition ends in a specific setup: 2 and 3 in corners, 4 low post, 5 outside the three-second lane, and 1 with the ball. [S7, pp.135-136]

## When to Use
- Immediately after gaining possession — before the defense can set up
- Primary break: fewer defenders than attackers, overload opportunities available
- Secondary break: defense is getting back but hasn't fully set up; trailer opportunities exist
- As a reset: when the primary break produces nothing, arrive in the flex setup to start the half-court offense

## Key Principles
1. **"Be quick, but don't hurry"** (John Wooden) — effective speed of movement is different from hasty counterproductive activity [S7, p.136]
2. **Offense starts with defense** — aggressive defense creates fast-break opportunities through turnovers and quick rebounds
3. **Fill the proper lanes** — players have specific rules based on their position in the transition
4. **Create overload situations** — the goal of filling lanes is to produce high-percentage shots via numerical advantages
5. **Improvise when easy baskets appear** — structure provides a framework, but don't hamper creativity when an obvious layup opportunity presents itself
6. **Transition ends in a specific formation** — this allows the flex offense to begin immediately without a separate play call

## Lane-Filling Rules

### Situation 1: Two Players on the Wing, Same Lane, Ball Side
- If 2 and 3 run on the same lateral lane with the ball driven behind them on that same lane:
  - **2** (forward player in the lane) continues and cuts **under the basket** to the opposite corner
  - **3** (behind 2) stays in the same lane, goes to the **corner on the same side**
  - **4** (other wing, opposite lane) cuts into the three-second area; if no pass, posts up at the low post (first trailer rule)
  - **5** runs as second trailer, stops outside the three-point line
```json name=diagram-positions
{"players":[{"role":"1","x":8,"y":22},{"role":"2","x":20,"y":14},{"role":"3","x":20,"y":42},{"role":"4","x":-20,"y":42},{"role":"5","x":2,"y":30}],"actions":[{"from":"1","to":"rim","type":"dribble"},{"from":"2","to":"left_corner","type":"cut"},{"from":"3","to":"right_corner","type":"cut"},{"from":"4","to":"rim","type":"cut"},{"from":"5","to":"rim","type":"cut"}],"notes":"Figure 8.1 shows a primary break with the ball driven up the right lane. Player 1 is dribbling up the right side toward the basket. Players 2 and 3 are both on the right lateral lane: 2 (forward) cuts under the basket to the left corner, 3 stays right and settles in the right corner. Player 4 (left wing) cuts into the three-second area toward the rim. Player 5 trails and stops near the high post/outside three-second lane. Starting positions approximate the moment of the break before all cuts are fully completed — the diagram depicts a full-court transition so positions are approximated at the point they enter the half-court view."}
```

### Situation 2: One Player on the Wing, Ball Side
- When 3 (guard or SF) is behind the ball:
  - **3** runs to occupy the other open lateral lane, independent of what first trailer (4) is doing
```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":10},{"role":"3","x":-14,"y":18},{"role":"4","x":14,"y":18},{"role":"5","x":0,"y":28}],"actions":[{"from":"3","to":"left_corner","type":"cut"},{"from":"4","to":"right_corner","type":"cut"}],"notes":"Figure 8.2 is referenced in the wiki but not visually shown on the provided PDF pages (only Figure 8.1 is depicted on p.136). Figure 8.2 describes Situation 2: \"One Player on the Wing, Ball Side\" — 3 is behind the ball and runs to occupy the other open lateral lane. Positions are estimated from the prose description: 1 with the ball pushing up the middle, 3 on one wing behind the ball, 4 on the opposite wing as first trailer, and 5 near the paint as second trailer. The diagram itself is not present in the scan; coordinates are approximated from the textual description only."}
```

### Situation 3: Trailer High Over the Ball on Lateral Lane
- **4** (first trailer) is high over the ball and on a lateral lane:
  - 4 runs to receive the ball and shoot a layup
  - If 4 can't receive and finish inside the lane: 4 posts up on the same side as the ball
  - 2 and 3 continue filling lateral lanes; 5 is the second trailer
```json name=diagram-positions
{"players":[{"role":"1","x":8,"y":22},{"role":"2","x":18,"y":10},{"role":"3","x":22,"y":42},{"role":"4","x":-22,"y":42},{"role":"5","x":0,"y":28}],"actions":[{"from":"4","to":"rim","type":"cut"},{"from":"1","to":"4","type":"pass"},{"from":"2","to":"right_corner","type":"cut"},{"from":"3","to":"right_corner","type":"cut"}],"notes":"Figure 8.3 (referenced but not directly shown on the provided pages — the only diagram visible is Figure 8.1 on page 136). Interpreting Figure 8.3 from the prose: 4 (first trailer) is high over the ball on a lateral lane, driving to receive and shoot a layup; 2 and 3 run the lateral lanes; 5 is the second trailer outside the three-point line. Starting positions approximate: 1 with ball near right wing area, 2 running down the right lane, 3 in the right corner area, 4 high on a lateral lane running toward the rim, 5 near the free-throw line. Positions are approximated from prose since Figure 8.3 itself is not rendered on the provided PDF pages."}
```

## Final Transition Formation (Flex Setup)
Transition ends with:
- **1**: Ball at the top of the key
- **2 and 3**: In the corners, outside the three-point line
- **4**: Low-post position
- **5**: Outside the three-second lane (second trailer position)

From this formation, the **flex offense begins**. [S7, p.136]

## Player Responsibilities
- **PG (1)**: Primary ball-handler; pushes the pace; initiates primary break options; initiates flex from final setup
- **SG (2)**: Fills lateral lane; reads whether to cut under (if forward in same lane) or corner (if behind)
- **SF (3)**: Fills the open lateral lane; reads trailer situation
- **PF (4)**: First trailer — cuts into the paint on receiving runs; posts low if not receiving; aggressive attack mentality
- **C (5)**: Second trailer — stops outside three-point line; provides reset spacing

## Common Mistakes
1. **Running without a destination** → correction: every player has a specific lane assignment; know your rule before the break starts
2. **All five players going to the paint** → correction: only one trailer (4) cuts into the three-second area; 5 stops outside
3. **Hurrying rather than being quick** → correction: controlled aggression — read the defense, don't just sprint and hope
4. **Missing the overload** → correction: if the primary break opportunity exists, take it; don't wait for the flex setup

## Related Concepts
- [[concept-basket-man-ball-man]] — defensive transition principles that enable this fast offense
- [[defensive-transition-principles]] — transition defense that limits opponent fast breaks
- [[transition-defense]] — Herb Brown's transition defense framework for context

## Sources
- [S7, pp.135-136] — the head coach, "Transition Game", Flex Offense chapter, pro Coaches Playbook
