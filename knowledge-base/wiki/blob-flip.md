---
type: play
category: out-of-bounds
formation: box
tags: [BLOB, man-to-man, cross-screen, seal, post, layup, rim-attack, youth]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: inbound-pass-read
    role: "1"
    criticality: required
  - id: cross-screen-set
    role: "5"
    criticality: required
  - id: flash-cut-to-rim
    role: "4"
    criticality: required
  - id: post-seal-and-pivot
    role: "5"
    criticality: required
  - id: corner-flash-decoy
    role: "2"
    criticality: optional
  - id: lob-pass-delivery
    role: "1"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: flash-cut-to-rim
    for_role: "4"
  - region: glute_max
    criticality: required
    supports_technique: flash-cut-to-rim
    for_role: "4"
  - region: core_outer
    criticality: required
    supports_technique: post-seal-and-pivot
    for_role: "5"
  - region: ankle_complex
    criticality: optional
    supports_technique: cross-screen-set
    for_role: "5"
# Cross-ref edge #8 — analytic signature. See backend/spec/crossref-anatomy-chain.md §M4 signature expansion
produces_signature:
  - factor: efg-pct
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: high
    rationale: "Both post players are routed to the rim via cross-screen and seal mechanics, generating layup attempts rather than mid-range or perimeter shots by design."
  - factor: ftr
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "Role 5's post seal pins the defender, and role 4's flash cut to the rim invites body contact on the receive or finish, increasing the likelihood of foul calls."
  - factor: tov-pct
    direction: protects
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "The play is a single-read, one-pass BLOB set where role 1 delivers directly to the open post; the scripted action limits dribble-handoff and skip-pass exposure that inflate turnover risk."
---

# Flip (BLOB vs Man-to-Man)

## Overview
An incredibly simple BLOB play from a box formation. A cross screen by the ball-side post frees the opposite post to cut to the rim, and then the screener seals and flashes to the other side. Both post players attack the rim simultaneously, forcing the passer (1) to read and deliver to the open layup. [S4, pp.23-24]

## Formation
- **1** (best passer): inbounder at the baseline
- **2**: weak-side low block
- **3**: ball-side low block
- **4**: weak-side elbow (big)
- **5**: ball-side elbow (big)

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":47},{"role":"3","x":-7,"y":40},{"role":"2","x":7,"y":40},{"role":"5","x":-8,"y":29},{"role":"4","x":8,"y":29}],"actions":[{"from":"3","to":"left_corner","type":"cut"},{"from":"2","to":"right_corner","type":"cut"}],"notes":"The first (top) diagram on p.23 shows the setup/Phase 1: box formation with 1 as OB inbounder at baseline center, 3 at ball-side (left) low block, 2 at weak-side (right) low block, 5 at ball-side (left) elbow, 4 at weak-side (right) elbow. Arrows show 2 flashing right to the corner and 3 flashing left to the corner. The second diagram shows Phase 2–3 (cross screen and cuts), which is not extracted here per instructions to emit only the starting/initial formation."}
```

## Phases

### Phase 1: Guards Flash to Corners
- **1 slaps the basketball** to start the play.
- **2 and 3** immediately flash hard to the corners, calling for the ball to drag their defenders away from the paint.

### Phase 2: Cross Screen
- **5** (ball-side post, elbow) sets a **cross screen on 4's defender**.
- **4** immediately flashes toward the **ball-side low block**, calling for the basketball.
- The screen must be set at the correct angle — **on the back hip** of the defender — so the defender cannot slip under and beat 4 to the rim. [S4, p.24]

### Phase 3: Screener Seals and Flashes
- After setting the screen, **5 seals 4's defender** and pivots, then **flashes to the opposite side of the rim** calling for the basketball.
- Both 4 and 5 now threaten the basket from opposite sides.
- **Post players must show target hands** to indicate where they want the pass as they flash to the rim. [S4, p.24]

### Phase 4: Passer Reads and Delivers
- **1 reads the defense** and passes to whichever post player is open for the layup.
- **Safety valve**: if neither 4 nor 5 is available, **3 can cut to the top of the key** to receive a lob pass over the top. [S4, p.24]

## Key Coaching Points
- **1 must be the best passer** — this play demands a quick, accurate read and delivery.
- **4 and 5 must stay to their own sides** when cutting to the rim; if they converge, one defender can deflect passes to both players. [S4, p.24]
- **Screen angle is critical** — set on the back hip so the defender cannot slip underneath. [S4, p.24]

## Counters
- If both post options are denied → 3 cuts to the top of the key as a lob-pass safety.

## Related Plays
- [[blob-box-gate]] — box formation BLOB with gate screen for wing shooter
- [[blob-yo-yo]] — box formation BLOB with dual up-screens for post finishers
- [[blob-two-inside]] — screen-the-screener BLOB to get ball inside to post

## Sources
- [S4, pp.23-24] — full play description and coaching points
