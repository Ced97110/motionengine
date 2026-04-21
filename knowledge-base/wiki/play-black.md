---
type: play
category: offense
formation: 5-out
tags: [man-to-man, step-up-screen, baseline-drive, post-flash, layup, kickout, quick-hitter]
source_count: 1
last_updated: 2026-04-20
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: baseline-drive-on-catch
    role: "2"
    criticality: required
  - id: step-up-screen-set
    role: "4"
    criticality: required
  - id: hard-cut-to-paint
    role: "5"
    criticality: required
  - id: dump-off-pass
    role: "2"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: baseline-drive-on-catch
    for_role: "2"
  - region: glute_max
    criticality: required
    supports_technique: baseline-drive-on-catch
    for_role: "2"
  - region: ankle_complex
    criticality: optional
    supports_technique: hard-cut-to-paint
    for_role: "5"
  - region: core_outer
    criticality: optional
    supports_technique: step-up-screen-set
    for_role: "4"
# Cross-ref edge #8 — stat-signature. Four-Factor direction this play drives.
# direction: "lifts" (raises our factor) or "protects" (lowers opp factor).
# factor enum: efg-pct | oreb-pct | tov-pct | ftr | ppp | pace | floor-pct
produces_signature:
  - factor: efg-pct
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: high
    rationale: "quick-hitter targets layup or open 3 via step-up screen + baseline drive; no mid-range attempts by design"
  - factor: ftr
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "baseline drive to rim invites body-contact fouls on the closeout"
  - factor: tov-pct
    direction: protects
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "set-play mechanics limit the sequence to ≤2 passes; lower TOV surface than motion offense"
---

# Black

## Overview
A quick man-to-man play from a 5-out formation that catches the defense off-guard by using a step-up screen to free a wing player for an immediate baseline drive. The opposite post flashes into the key to counter the defensive rotation, creating a layup opportunity or a kick-out to a perimeter player. [S4, p.56]

## Formation
5-out. 1 (PG) at the top. 2 on one wing. 3 on the opposite wing. 4 and 5 in the **corners** (post players spread wide in the corners). [S4, p.56]

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":33},{"role":"2","x":-18,"y":28},{"role":"3","x":18,"y":28},{"role":"4","x":-22,"y":42},{"role":"5","x":22,"y":42}],"actions":[{"from":"1","to":"2","type":"pass"},{"from":"4","to":"2","type":"screen"},{"from":"2","to":"rim","type":"dribble"},{"from":"5","to":"left_elbow","type":"cut"}],"notes":"The diagram shows the 5-out starting formation. 1 is at the top of the key, 2 and 3 on the wings, and 4 and 5 in the corners. The initial action shows 1 passing to 2, with 4 stepping up to set a screen on 2's defender, 2 driving the baseline toward the rim, and 5 flashing from the right corner up into the key area (approximately the elbow/mid-lane). The diagram combines Phase 1 and Phase 2 actions in a single image; starting positions are captured as the 5-out setup."}
```

## Phases

### Phase 1: Wing Entry and Step-Up Screen
- 1 passes to one wing — for this example, 2.
- As soon as the pass is made, **4 (in the corner) steps up and sets a strong screen** on 2's defender (D2). [S4, p.56]

### Phase 2: Baseline Drive
- 2 receives the pass and **immediately rips the ball through and attacks baseline** on the catch. [S4, p.56]
- The key is attacking on the catch — before D2 recovers.

### Phase 3: Force Rotation and Finish
- If the defense is set up correctly, **5's defender will be in help position**.
- 5 flashes into the key, finding an open angle to receive the pass. [S4, p.56]
- **Options for 2:**
  - Finish the baseline drive at the basket.
  - Drop pass to 5 for the score inside.
  - If the defense rotates down to stop 5, kick out to **3 on the perimeter** who will be alone for the open shot. [S4, p.56]

## Key Coaching Points
- 2 (the wing attacker) should be "the player you want attacking the rim" — this is a drive-first play. [S4, p.56]
- 4 just needs to be able to set a strong screen — not necessarily a scoring threat. [S4, p.56]
- 2 must **rip through immediately** on the catch — any delay lets D2 recover from the screen.
- 5's flash must create a clear passing lane for 2; timing is critical to exploit the defensive rotation.

## Counters
- If D4 stays at home and doesn't rotate to help on 2's drive, 2 can finish uncontested at the rim.
- If 3's kick-out is denied, reset through 1 at the top.

## Related Plays
- [[play-step-up]] — zone version using same step-up screen and baseline drive concept
- [[play-swinger]] — man-to-man play with similar drive-and-kick structure
- [[play-1-4-quick-floppy]] — another man-to-man quick hitter with multiple scoring reads

## Related Concepts
- [[concept-anatomy-hip-flexor-complex]] — required anatomy for roles 2 and 5 (baseline drive + hard flash cut)
- [[concept-anatomy-glute-max]] — required horizontal-propulsion engine for the baseline drive and post-flash finish
- [[concept-anatomy-ankle-complex]] — optional supporting anatomy for baseline drive and post-flash landing mechanics
- [[concept-anatomy-core-outer]] — optional core-stability anatomy for contact on the post flash and deceleration into the finish

## Sources
- [S4, p.56] — full play description with diagram
