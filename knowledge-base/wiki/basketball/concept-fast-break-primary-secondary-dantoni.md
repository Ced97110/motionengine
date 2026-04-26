---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [offense, transition, fast-break, pick-and-roll, spacing, tempo]
source_count: 1
last_updated: 2026-04-11
---

# Primary and Secondary Break System — D'Antoni

## Summary
Mike D'Antoni's fast-break system (pro team) defines the primary break as the first 2–3 seconds after gaining possession, and the secondary break as the period before the defense fully sets. Together they account for more than half the team's scoring. The system runs every single possession off a defensive rebound, out-of-bounds play, steal, or turnover — no exceptions. [S7, pp.163–175]

## When to Use
- On every possession with transition opportunity (rebound, steal, OOB, turnover)
- 2-on-1: anytime two players get ahead of a single defender
- 3+ players: whenever wings can fill wide lanes ahead of the defense
- Secondary: when primary scoring chances are not available but defense is still disorganized

## Primary Break

### Trigger Situations
- Defensive rebound after missed FG or FT
- Any out-of-bounds (nearest player to ball inbounds immediately after opponent score)
- Steal or offensive turnover [S7, p.166]

### 2-on-1 Primary Break
- Ball handler stops near the corner of the free-throw lane, keeps dribbling
- Second offensive player cuts at 45° angle to the basket, maintaining proper spacing
- **Read**: If defender comes to ball handler → pass to cutter; if defender sags/hedges toward cutter → ball handler shoots or drives [S7, p.167]
- Rule: proper spacing + eagerness to run. Court sense decides the option.

```json name=diagram-positions
{"players":[{"role":"1","x":-10,"y":29},{"role":"2","x":14,"y":22},{"role":"x1","x":0,"y":35}],"actions":[{"from":"1","to":"rim","type":"dribble"},{"from":"2","to":"rim","type":"cut"}],"notes":"Figure 10.1 (p.167) shows a two-on-one fast break. The diagram is a full-court view but the key action occurs in the offensive half-court. Player 1 (ball handler) is positioned near the left corner of the free-throw lane, continuing to dribble. Player 2 is on the right wing area cutting at roughly a 45-degree angle toward the basket. A single defender (x) is positioned between them near the elbow/lane area. The dribble arrow shows 1 moving toward the free-throw lane corner; a cut arrow shows 2 angling toward the rim. The diagram also shows the full-court origin of the break (both players running from the backcourt), but the starting half-court formation captured here reflects their positions as the scoring decision is being made."}
```

### 3-Player Primary Break
- After opponent score: 4 (PF) makes quick inbounds to 1 (PG)
- 2 (SG) and 3 (SF) sprint as wide as possible — "touch the sideline" to occupy precise lanes
- 2 and 3 run to deep corners of the offensive half-court
- 5 (first trailer) options at FT line extended:
  - Receive ball and shoot, or cut at 45° into lane for shot under basket
  - Stay middle to reverse the ball to the other side [S7, p.168]
- 4 (second trailer, made inbounds) sprints offense and spots up for 3-point shot

```json name=diagram-positions
{"players":[{"role":"4","x":0,"y":-2},{"role":"1","x":-8,"y":8},{"role":"2","x":-25,"y":20},{"role":"5","x":6,"y":18},{"role":"3","x":25,"y":20}],"actions":[{"from":"4","to":"1","type":"pass"},{"from":"1","to":"rim","type":"dribble"},{"from":"2","to":"left_corner","type":"cut"},{"from":"3","to":"right_corner","type":"cut"},{"from":"5","to":"rim","type":"cut"}],"notes":"Figure 10.2 starting formation: 4 is the inbounder at the top (just past half-court), passing to 1 (PG) who is handling the ball in the left-center area. 2 (SG) and 3 (SF) sprint wide to their respective deep corners. 5 (first trailer) follows the break down the middle toward the rim. The diagram shows the initial positions and movement arrows for the wide-lane 3-player primary break. Figures 10.3–10.5 show subsequent trailer options; only the Figure 10.2 starting formation is extracted here."}
```

### No-Solution Primary → PnR
- If primary break yields no quick scoring: **4 sets screen on 1 immediately**
- Quick pick-and-roll creates:
  - Pass to 2 or 3 in deep corners for 3-point shot
  - Pass to 5 cutting into the 3-second lane
  - 1 makes layup
  - 4 rolls to basket after screening [S7, p.169]

```json name=diagram-positions
{"players":[{"role":"1","x":-10,"y":22},{"role":"2","x":-22,"y":42},{"role":"3","x":22,"y":42},{"role":"4","x":4,"y":10},{"role":"5","x":8,"y":26}],"actions":[{"from":"4","to":"1","type":"screen"},{"from":"1","to":"rim","type":"dribble"},{"from":"1","to":"2","type":"pass"},{"from":"1","to":"3","type":"pass"},{"from":"1","to":"5","type":"pass"},{"from":"4","to":"rim","type":"cut"}],"notes":"Figure 10.6: No-solution primary break pick-and-roll. 1 has the ball near the top of the key/left of center. 4 sets a screen on 1 for a quick PnR. 5 is positioned at the right elbow area. 2 and 3 are stationed in the deep left and right corners respectively. Action arrows show: 4 screening 1, 1 dribbling off the screen (toward the lane/rim), with pass options depicted to 2 (left corner), 3 (right corner), and 5 (cutting into the lane); 4 rolls to the basket after the screen. Starting positions are approximate from the diagram on p.169."}
```

## Secondary Break

D'Antoni's secondary break philosophy: **always keep 3–4 players on the perimeter, reverse ball quickly, and give all perimeter players green-light shooting.** Big men post briefly, then face up or drift outside. Middle of court stays open. [S7, p.169]

### Roll 4 Pop
- 4 is first trailer, cuts into lane and posts up; 5 is second trailer, stops outside 3-point line
- 1 passes to 5; 1 moves opposite direction; 5 reverses to 3 coming high
- Simultaneously with 5→3 pass: 2 cuts baseline off 4's screen, replaces 3 in opposite corner
- If 3 can't pass to 2: 1 screens down for 4, 4 receives stagger screen from 5 (who sets up in short corner after screening)
- 4 catches at middle of court from 3; 4 drives to basket or kicks to 5 (popped to corner), 1, 3, or 2 on perimeter [S7, pp.169–170]

```json name=diagram-positions
{"players":[{"role":"1","x":-10,"y":2},{"role":"2","x":-22,"y":32},{"role":"3","x":22,"y":32},{"role":"4","x":-7,"y":36},{"role":"5","x":18,"y":14}],"actions":[{"from":"1","to":"5","type":"pass"},{"from":"5","to":"3","type":"pass"},{"from":"2","to":"right_corner","type":"cut"},{"from":"4","to":"left_low_block","type":"screen"}],"notes":"This is Figure 10.7 (Roll 4 Pop starting formation), extracted from p.169. 1 is near the top of the key/left of center coming down from transition; 4 is the first trailer who has cut into the lane and posted up left low block area; 5 is the second trailer stopped outside the three-point line on the right wing; 2 is in the left corner; 3 is in the right corner. The diagram shows: 1 passes to 5, 5 reverses to 3 (coming high), and 2 cuts baseline off 4's screen to replace 3 in the opposite corner. The diagram is a half-court view oriented with the basket at the bottom of the diagram (y ≈ 43 in our coordinate system)."}
```

### Roll 1 Pop
- Same start as Roll 4 Pop but designed for 1
- 1 passes to 5; 5 to 3 coming high; 2 cuts baseline off 4's screen to opposite corner
- 1 receives screen from 5, goes to middle of court, receives ball from 3
- After screen, 5 rolls to basket and moves to short corner; 4 goes to free-throw angle
- 1 passes to 4, cuts around for potential hand-off, then goes to corner; 3 cuts to short corner opposite side
- 4 drives toward 2 for hand-off if can't shoot/drive; 2 can penetrate or pass to 4/5/3/1 [S7, p.170]

```json name=diagram-positions
{"players":[{"role":"1","x":-12,"y":22},{"role":"2","x":-22,"y":38},{"role":"3","x":22,"y":38},{"role":"4","x":-7,"y":36},{"role":"5","x":12,"y":22}],"actions":[{"from":"1","to":"5","type":"pass"},{"from":"5","to":"3","type":"pass"},{"from":"2","to":"right_corner","type":"cut"},{"from":"4","to":"2","type":"screen"}],"notes":"Figure 10.10 (Roll 1 Pop starting formation): 1 is on the left perimeter near the wing, 5 is on the right side near FT-line extended, 2 is in the left deep corner, 3 is on the right wing coming high, 4 is near the left low block/elbow area as first trailer who sets a baseline screen for 2. The diagram shows 1 passing to 5, 5 reversing to 3 (coming high), and 2 cutting baseline off 4's screen to replace 3 in the right corner. This is the initial phase of Roll 1 Pop (Figure 10.10)."}
```

### Through Flare 1 Man
- Set: 5 is second trailer, 4 is first trailer on low post, 2 and 3 in deep corners
- 1 passes to 2 coming high (or to 5), then cuts to opposite side low-post area
- 3 screens for 1; 1 comes off screen, receives ball from 5; 3 moves to low-post area
- If 1 isn't free: 1 passes to 3, receives screen from 5, goes to middle of court, receives ball back from 3
- 1 can drive to basket or drive and kick to 2/4/3/5 who rolls after screen [S7, pp.171]

```json name=diagram-positions
{"players":[{"role":"1","x":-10,"y":5},{"role":"2","x":-22,"y":32},{"role":"3","x":22,"y":32},{"role":"4","x":-7,"y":40},{"role":"5","x":0,"y":15}],"actions":[{"from":"1","to":"5","type":"pass"},{"from":"1","to":"left_low_block","type":"cut"}],"notes":"This is Figure 10.13, the starting formation of the \"Through Flare 1 Man\" play. Set: 5 is second trailer near top of key/center, 4 is first trailer on left low post, 2 and 3 are deep in the corners. 1 is at the left wing/perimeter area with the ball. The depicted action shows 1 passing to 5 (the case described in the text) and then 1 cutting to the opposite (right) low-post area. The diagram on page 171 shows 1 on the left perimeter, 5 near the top of the key, 2 in left corner, 3 in right corner, and 4 on the left low block area."}
```

## Key Coaching Points
- "As soon as we gain possession — there's no hesitation. We're sprinting toward our end of the court." [S7, p.166]
- Wings must "touch the sideline" — wide spacing forces defenders to cover maximum court area
- Big men must be able to face the basket, drive, and shoot from outside; keep the middle open [S7, p.171]
- Practice all secondary break options at full speed — players must react to defense automatically [S7, p.171]
- Divide practice: big men work secondary break drills on one end; perimeter players practice secondary break shooting options on the other [S7, p.171]

## Counters
- **Defense sags to deny the 3-point arc**: Drive and kick — multiple perimeter players on the arc guarantee someone is open
- **Defense sprints back to deny primary**: No solution → immediate 4-on-1 PnR or secondary set
- **Defense forces ball handler to sideline**: Step-up screen counter (see ) [S7, p.173]

## Related Concepts
- [[concept-fast-break-elements-dantoni]] — prerequisites for running this system
- [[concept-fast-break-philosophy-karl-moe]] — complementary fast-break philosophy
- [[pick-and-roll-defense]] — how opponents try to stop the no-solution PnR counter
- [[concept-basket-man-ball-man]] — defensive assignments that generate break opportunities

## Sources
- [S7, pp.163–175] — D'Antoni, Gentry, Iavaroni: Primary and Secondary Breaks chapter
