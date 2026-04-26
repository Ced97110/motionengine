---
type: play
category: offense
formation: 2-3 high-post
tags: [continuity, back-screen, chin, flare, down-screen, motion, half-court]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: back-screen-set
    role: "5"
    criticality: required
  - id: rub-cut-off-screen
    role: "2"
    criticality: required
  - id: post-pop-after-screen
    role: "5"
    criticality: required
  - id: down-screen-set
    role: "3"
    criticality: required
  - id: flare-screen-set
    role: "1"
    criticality: required
  - id: multi-option-post-read
    role: "5"
    criticality: required
  - id: backdoor-cut
    role: "4"
    criticality: optional
  - id: dribble-handoff-screen-on-ball
    role: "1"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: rub-cut-off-screen
    for_role: "2"
  - region: ankle_complex
    criticality: required
    supports_technique: rub-cut-off-screen
    for_role: "2"
  - region: core_outer
    criticality: required
    supports_technique: back-screen-set
    for_role: "5"
  - region: glute_max
    criticality: required
    supports_technique: back-screen-set
    for_role: "5"
  - region: hip_flexor_complex
    criticality: optional
    supports_technique: backdoor-cut
    for_role: "4"
  - region: ankle_complex
    criticality: optional
    supports_technique: flare-screen-set
    for_role: "1"
# Cross-ref edge #8 — analytic signature. See backend/spec/crossref-anatomy-chain.md §M4 signature expansion
produces_signature:
  - factor: efg-pct
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: high
    rationale: "The play cascades back screens, down screens, and flare screens simultaneously, generating layup attempts at the rim (roll cuts) and open catch-and-shoot looks on the perimeter — eliminating contested mid-range attempts by design."
  - factor: ftr
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "Rub cuts off back screens and post rollers attacking the paint force defenders into body contact, inviting foul calls on closeout and pursuit situations."
  - factor: tov-pct
    direction: protects
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "The structured multi-option read hierarchy gives the passer (role 5 or role 3) a sequenced decision tree rather than ad-hoc improvisation, reducing unforced turnovers relative to open motion offense."
  - factor: pace
    direction: lowers
    concept_slug: concept-four-factors
    magnitude: low
    rationale: "The continuity system cycles through multiple screen layers and secondary options before a shot is taken, consuming half-court possession time and depressing overall pace."
# Cross-ref edge — counters provenance (M4 part 3). extraction labels gate which bullets are surface-safe.
counters:
  - text: "When the defense switches on 5's back screen, 5 immediately rolls hard to the basket, exploiting the size mismatch against the smaller defender who switched onto him."
    extraction: llm-inferred
  - text: "When the defense collapses to stop 4 coming off the flare screen, 1 abandons the fade and rolls directly to the basket to receive a pass for a layup."
    extraction: llm-inferred
  - text: "When 2 cannot receive the pass off the back screen, 5 shifts to the opposite elbow and reads the available secondary screening options to restart the action."
    extraction: llm-inferred
---

# Continuity — Chin Action

## Overview
The "Chin" action is a specialized Continuity set that begins with a **back pick by the high post (5) on the weak side of the half-court**. It creates multiple simultaneous screening threats — a guard rubbing off a back screen, a post rolling to the basket, and down-screen / flare-screen combinations — that are very difficult for a man-to-man defense to cover without switching. The Chin Pass to Strong Side variant adds a flare-screen wrinkle that simultaneously frees two perimeter players and two rollers. [S7, pp.128-130]

## Formation
1 and 2 at guard positions; 3 at weak-side wing; 4 at ball-side wing; 5 flashing to high-post elbow on the weak side.

## Phases

### Phase 1: Chin Option 1 (Back Screen)
- 2 passes to 1; 2 rubs off the back screen set by 5 and cuts to the opposite side
- 1 passes to 3
- 3 can pass to 2; if 2 can't receive, 5 screens on the other elbow for 1
- 1 receives from 3 for a shot or drive; 5 can roll in the opposite direction and receive from 3
```json name=diagram-positions
{"players":[{"role":"1","x":-4,"y":33},{"role":"2","x":14,"y":33},{"role":"3","x":-22,"y":22},{"role":"4","x":22,"y":22},{"role":"5","x":-6,"y":24}],"actions":[{"from":"2","to":"1","type":"pass"},{"from":"1","to":"3","type":"pass"},{"from":"2","to":"right_wing","type":"cut"},{"from":"5","to":"2","type":"screen"}],"notes":"Figure 7.49 shows the starting formation for Chin Option 1. 1 and 2 are at guard positions near the top of the key (2 slightly right, 1 slightly left). 5 is at the weak-side (left) elbow acting as the back-screener. 3 is at the left wing and 4 at the right wing. The arrows show: 2 passes to 1, 1 passes to 3, 2 rubs off 5's back screen and cuts toward the right side of the court. Figure 7.50 (the continuation) shows 5 stepping to the opposite (right) elbow to screen for 1, but the starting formation requested is from Figure 7.49."}
```

### Phase 1: Chin Option 2 (Continuity)
- 2 passes to 1, rubs off 5's back screen, cuts to opposite side
- 1 passes to 3; 3 dribbles right while 5 screens for 1 (1 cuts opposite, replaces 4; 4 gets to guard position)
- 3 passes to 4; 4 passes to 1; 3 rubs off 5's back screen and goes to ball-side corner
- 1 can pass to 3 in the corner
```json name=diagram-positions
{"players":[{"role":"1","x":-4,"y":33},{"role":"2","x":14,"y":33},{"role":"3","x":-22,"y":22},{"role":"4","x":22,"y":18},{"role":"5","x":-2,"y":24}],"actions":[{"from":"2","to":"1","type":"pass"},{"from":"1","to":"3","type":"pass"},{"from":"2","to":"right_wing","type":"cut"},{"from":"5","to":"2","type":"screen"},{"from":"5","to":"1","type":"screen"}],"notes":"Figure 7.51 (the starting formation for Chin Option 2). 1 and 2 are at guard positions near the top of the key (1 slightly left of center, 2 to the right). 5 is at the weak-side (left) high-post elbow area. 3 is at the left wing, 4 at the right wing slightly deeper. Arrows show: 2 passes to 1; 1 passes to 3; 2 rubs off 5's back screen cutting toward the right side of the court; 5 also screens for 1 on the other side. Figure 7.52 (the continuation) shows the later stage: 3 has dribbled right, 4 has moved to guard position, and 1 has replaced 4 on the right — that is a later phase and not the starting formation."}
```

**If no solution:** 5 flashes to the other elbow and back-screens for 4; 1 passes to 4. If 4 can't receive, he comes back and back-screens for 5; 1 reads: pass to 5 or pass to 4 (who pops out).
```json name=diagram-positions
{"players":[{"role":"1","x":8,"y":29},{"role":"2","x":-18,"y":40},{"role":"3","x":18,"y":22},{"role":"4","x":-5,"y":24},{"role":"5","x":0,"y":29}],"actions":[{"from":"5","to":"4","type":"screen"},{"from":"1","to":"4","type":"pass"}],"notes":"Figure 7.53 shows the continuation of Chin Option 2 after no solution has been found. 5 has flashed to the left elbow and is back-screening for 4 (who was at the top of the key area). 1 is at the right elbow/guard area with the ball. 2 is at the bottom-left (ball-side corner area after earlier cuts). 3 is at the right wing. The back screen by 5 for 4 is the primary depicted action, with 1 holding the ball and reading a pass to 4. Figure 7.54 (the secondary diagram) shows 4 coming back to back-screen for 5 if 4 can't receive — not depicted in Figure 7.53's starting frame."}
```

### Phase 2: Chin Pass to Strong Side — Flare Action (Option 1)
- 2 passes to 3 and receives a back screen from 5 (who has flashed to the strong-side elbow); 2 posts down low on the ball side; 5 pops out after the screen
- 3 passes to 5; 3 screens down for 2; 1 makes a **flare screen** for 4
- 5 reads four options:
  - (a) Pass to 2 coming off 3's down screen
  - (b) Pass to 4 coming off 1's flare screen
  - (c) Pass to 3, who rolls to basket after setting the screen for 2
  - (d) Pass to 1, who rolls to basket after setting the flare screen for 4
- Note: 4 can also cut backdoor if his defender slides over 1's flare screen
```json name=diagram-positions
{"players":[{"role":"2","x":-10,"y":28},{"role":"3","x":-18,"y":22},{"role":"4","x":22,"y":22},{"role":"1","x":18,"y":32},{"role":"5","x":8,"y":29}],"actions":[{"from":"2","to":"3","type":"pass"},{"from":"5","to":"2","type":"screen"},{"from":"2","to":"left_low_block","type":"cut"}],"notes":"Figure 7.55 (the first of the two requested diagrams) shows the starting formation for Chin Pass to Strong Side, Option 1. 2 is at the left guard/wing area, 3 is at the left wing, 4 is at the right wing, 1 is at the right guard position, and 5 has flashed to the strong-side (right) elbow area. The diagram shows 2 passing to 3, 5 back-screening for 2, and 2 cutting down to post on the ball side (left low block area). Figure 7.56 (the continuation) shows the subsequent 3-passes-to-5 action and the simultaneous down screen / flare screen, but the starting formation is drawn from Figure 7.55."}
```

### Phase 2: Chin Pass to Strong Side — Option 2
- 1 passes to 2, screens on the ball, and pops out to replace 2; 2 dribbles to other side
- 1 posts down low on weak side; 5 gets to the other elbow
- 2 passes to 4; 2 rubs off 5's back screen and goes to ball side; 5 pops out
- 5 receives from 4; 1 screens for 3 who pops out and receives from 5
```json name=diagram-positions
{"players":[{"role":"1","x":-4,"y":33},{"role":"2","x":4,"y":36},{"role":"3","x":-22,"y":22},{"role":"4","x":22,"y":22},{"role":"5","x":5,"y":24}],"actions":[{"from":"1","to":"2","type":"pass"},{"from":"1","to":"right_corner","type":"screen"},{"from":"1","to":"left_low_block","type":"cut"}],"notes":"Figure 7.57 is the starting diagram for this marker (Figures 7.57–7.59). It shows the beginning of Chin Pass to Strong Side, Option 2. 1 and 2 are at guard positions near the top of the key (1 slightly left-center, 2 slightly right-center). 5 is at the right (strong-side) elbow area. 3 is at the left wing. 4 is at the right wing. The depicted action in Fig 7.57 shows 1 passing to 2, then screening on the ball and popping out to replace 2, while 1 will post down low on the weak side. The pass arrow goes from 1 to 2, and 1 has a cut arrow heading down toward the weak-side low block area. 5 is beginning to move toward the other elbow."}
```

## Key Coaching Points
- The back screen timing is critical: 5 must be set at the elbow before 2 (the cutter) initiates the rub
- The cutter must sell going the other way before rubbing off the screen
- In the Flare Action, 1's flare screen and 3's down screen happen simultaneously — the defense must choose which threat to cover
- The four-option read for 5 in the Flare Action is the most complex decision in the Continuity system — post must see all reads before the catch
- "4 can also make a backdoor cut if his defender slides over the screen" — always have the backdoor available when defenders overreact to screens

## Counters
- If defense switches on the back screen: 5 rolls to the basket immediately — it's a small-on-big mismatch
- If defense helps on the flare screen: 1 rolls to the basket instead of fading — pass hits the rolling 1 for a layup
- If 2 can't receive the ball off the back screen: 5 reads the secondary screen options on the other elbow

## Related Plays
- [[play-pass-and-screen-away]] — main "basic" set that uses similar screen-and-roll reads
- [[play-high-split-action]] — follow-the-ball option from same formation
- [[play-reverse-dribble-options]] — when the entry is denied entirely
- [[concept-continuity-offense-overview]] — full system overview
- [[concept-backdoor-cut]] — backdoor technique used throughout
- [[concept-flex-back-screen-footwork]] — back-screen footwork mechanics relevant to the Chin screen

## Sources
- [S7, pp.128-130] — Eddie the iconic scorer and Pete Carril, "Chin" and "Chin Pass to Strong Side", Continuity Offense chapter, pro Coaches Playbook
