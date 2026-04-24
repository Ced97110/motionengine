---
type: play
category: offense
formation: 2-3 high-post
tags: [continuity, cut-away, backdoor, down-screen, motion, half-court]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: high-post-entry-pass
    role: "1"
    criticality: required
  - id: cut-away-to-opposite-side
    role: "1"
    criticality: required
  - id: cut-away-to-opposite-side
    role: "2"
    criticality: required
  - id: down-screen-set
    role: "4"
    criticality: required
  - id: backdoor-cut
    role: "3"
    criticality: optional
  - id: dribble-toward-wing
    role: "5"
    criticality: optional
  - id: high-post-read-and-distribute
    role: "5"
    criticality: required
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: cut-away-to-opposite-side
    for_role: "1"
  - region: hip_flexor_complex
    criticality: required
    supports_technique: cut-away-to-opposite-side
    for_role: "2"
  - region: ankle_complex
    criticality: required
    supports_technique: backdoor-cut
    for_role: "3"
  - region: core_outer
    criticality: optional
    supports_technique: down-screen-set
    for_role: "4"
  - region: glute_max
    criticality: optional
    supports_technique: high-post-read-and-distribute
    for_role: "5"
---

# Continuity — Pass and Cut Away Set

## Overview
The "Pass and Cut Away" set keeps all four perimeter spots occupied at all times and eliminates the strong side / weak side distinction. After the high-post entry, both guards cut away from the ball in timed sequence, and the post reads the cuts. This constant perimeter movement forces all five defenders to track assignments simultaneously. [S7, pp.122-123]

## Formation
1 and 2 at guard positions; 3 and 4 at wings; 5 flashing to high-post elbow opposite the ball.

## Phases

### Phase 1: Entry and Both Guards Cut Away
- 2 passes to 1; 5 flashes to high-post elbow opposite the ball
- 1 passes to 5; 2 immediately cuts to the opposite side of the floor
- 1 also cuts away to the opposite side, timing his cut after 2's cut
- 5 can pass to 2 or to 1 on the cut
```json name=diagram-positions
{"players":[{"role":"1","x":-8,"y":35},{"role":"2","x":8,"y":35},{"role":"3","x":-22,"y":22},{"role":"4","x":22,"y":22},{"role":"5","x":8,"y":29}],"actions":[{"from":"2","to":"1","type":"pass"},{"from":"1","to":"5","type":"pass"},{"from":"2","to":"left_corner","type":"cut"},{"from":"1","to":"left_corner","type":"cut"},{"from":"5","to":"2","type":"pass"},{"from":"5","to":"1","type":"pass"}],"notes":"Figure 7.29 starting formation: 1 and 2 at guard positions (roughly top of key / elbow-extended area), 3 and 4 at wings, 5 flashing to the right elbow (high-post). The dashed arrow shows 2 passing to 1, then 1 passing to 5. Both 2 and 1 cut away (leftward) in sequence. 5 has pass options to 2 and 1 during their cuts. Player positions approximate from diagram scan."}
```

### Phase 2: Down Screen and Dribble-Toward Option
- As 1 comes out of the lane, 4 sets a down screen for 1 (or 1 replaces 2's spot)
- 5 can pass to 1 off 4's down screen, or to 4 who rolls to basket after the screen
- If 5 can't reach 1 or 4, 5 dribbles toward 3
- If 3 is overplayed, 3 goes backdoor and can receive from 5
- 3 can also screen down for 2; 5 passes to 2; if 2 can't shoot, passes to 3 who has posted down low
```json name=diagram-positions
{"players":[{"role":"1","x":2,"y":35},{"role":"2","x":8,"y":42},{"role":"3","x":-20,"y":22},{"role":"4","x":20,"y":28},{"role":"5","x":4,"y":33}],"actions":[{"from":"5","to":"3","type":"dribble"},{"from":"4","to":"1","type":"screen"},{"from":"1","to":"right_wing","type":"cut"},{"from":"3","to":"rim","type":"cut"}],"notes":"Figure 7.30 shows the Phase 2 state: 5 is near the high-post/elbow area dribbling toward the left (3's) side. 4 has set or is setting a down screen for 1 near the right elbow/lane area. 3 is on the left wing with a backdoor cut arrow toward the basket (overplayed situation). 2 is near the right corner/baseline area. 1 is coming off 4's down screen toward the right wing. The 'x' marker visible in the diagram near the lane likely denotes the screen location by 4. Coordinates approximated from the diagram layout."}
```

## Key Coaching Points
- The two cuts must be timed sequentially — not simultaneously — so 5 can make a clear read
- "We always want to have the four perimeter spots occupied" and "constantly move the defense so we don't have a weak and strong side" [S7, p.122]
- 5 must read: cut pass (2 or 1), down-screen receiver (1 off 4), roller (4), or dribble-toward backdoor (3)
- If 3 is playing straight up (not overplayed), 3 receives the dribble-toward pass and can initiate from the wing

## Counters
- If defense sags: 5 looks for cut passes immediately when cutters reach the lane area
- If defense chases cutters and denies them: backdoor off 3's wing is available as 5 dribbles toward it
- If 4's down screen is hedged: 4 rolls to basket — deliver to the roll

## Related Plays
- [[play-pass-and-screen-away]] — the screen-away variant from the same basic formation
- [[play-high-split-action]] — follow-the-ball high-split option
- [[concept-continuity-offense-overview]] — full system overview
- [[concept-backdoor-cut]] — backdoor technique used in the dribble-toward counter

## Sources
- [S7, pp.122-123] — Eddie the iconic scorer and Pete Carril, "Pass and Cut Away Set", Continuity Offense chapter, pro Coaches Playbook
