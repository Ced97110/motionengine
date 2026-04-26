---
type: play
category: offense
formation: 1-3-1
tags: [zone-offense, 2-3-zone, flare-screen, three-point, shooter, quick-hitter]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: dribble-drag-defender
    role: "2"
    criticality: required
  - id: flare-screen-set
    role: "5"
    criticality: required
  - id: flare-screen-use
    role: "2"
    criticality: required
  - id: catch-and-shoot-off-screen
    role: "2"
    criticality: required
  - id: pin-down-screen-set
    role: "4"
    criticality: required
  - id: skip-pass-over-top
    role: "1"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: dribble-drag-defender
    for_role: "2"
  - region: ankle_complex
    criticality: required
    supports_technique: flare-screen-use
    for_role: "2"
  - region: glute_max
    criticality: required
    supports_technique: flare-screen-use
    for_role: "2"
  - region: core_outer
    criticality: optional
    supports_technique: flare-screen-set
    for_role: "5"
# Cross-ref edge #8 — analytic signature. See backend/spec/crossref-anatomy-chain.md §M4 signature expansion
produces_signature:
  - factor: efg-pct
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: high
    rationale: "The entire sequence is engineered to deliver the best shooter an uncontested catch-and-shoot three off the flare screen, eliminating mid-range or low-efficiency looks by design."
  - factor: tov-pct
    direction: protects
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "The scripted ball-movement chain (wing → corner → top) keeps the pass count low and each read pre-determined, reducing live-read turnovers versus open motion against the zone."
  - factor: pace
    direction: lowers
    concept_slug: concept-four-factors
    magnitude: low
    rationale: "The multi-phase drag-and-screen setup requires deliberate dribble-drag and sequential screening actions before the shot is taken, consuming clock relative to a direct attack."
# Cross-ref edge — counters provenance (M4 part 3). extraction labels gate which bullets are surface-safe.
counters:
  - text: "When X2 fails to track 2's dribble drag toward the top of the key, 2 is already open for a catch-and-shoot three before 5 ever sets the flare screen."
    extraction: llm-inferred
  - text: "When 1's skip pass over the top to 2 is cut off by X2, 1 reverses the ball to 3 on the weak-side wing to reset the attack."
    extraction: llm-inferred
---

# 23 Flare (Set Play vs 2-3 Zone)

## Overview
A quick-hitter designed to attack the 2-3 zone by moving the ball and the shooter to fatigue the zone's wing defender, then using a sudden flare screen to free the best shooter for an open three-pointer on the wing. Best used 1–2 times per game for maximum surprise effect. [S4, pp.33-34]

## Formation
- Starts in a **1-3-1 formation**
- A shooting-capable player (4) in the corner on the same side as the best shooter (2)
- **1** at top of key, **2** at wing, **3** at weak-side wing, **5** at strong-side elbow area

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":20},{"role":"2","x":16,"y":22},{"role":"3","x":-16,"y":22},{"role":"5","x":4,"y":27},{"role":"4","x":22,"y":42}],"actions":[{"from":"1","to":"2","type":"pass"},{"from":"2","to":"4","type":"pass"}],"notes":"Extracted from the first (top) diagram on p.33, which shows the initial 1-3-1 setup. 1 is at top of key, 2 on the ball-side (right) wing, 3 on the weak-side (left) wing, 5 near the high post/strong-side elbow area, and 4 in the ball-side corner. The diagram shows the Phase 1 action arrows: 1 passing to 2, and 2 passing to 4 in the corner, consistent with the setup description."}
```

## Phases

### Phase 1: Ball to Wing
- **1** takes a few dribbles and passes to **2** on the wing. **1** stays at the top of the key.
- **5** steps to the strong-side elbow.

### Phase 2: Ball to Corner and Back
- **2** immediately passes to **4** in the corner.
- **4** passes back to **2**, and while doing so begins **walking their defender (x4) toward the rim** — setting up the blocking action for later.

### Phase 3: Drag the Zone Wing Defender
- **2** takes 2–3 dribbles toward the top of the key, forcing **X2** to follow in order to deny the open shot opportunity.

### Phase 4: Ball to Top — Flare Screen Triggered
- **2** passes to **1** at the top of the key.
- **5 immediately sets a flare screen** for **2** — the screen must be **quick to catch X2 off guard**. [S4, p.34]
- Simultaneously, **4** (who has walked x4 toward the rim) sets a screen to prevent x4 from contesting the shot.

### Phase 5: Shooter Uses Flare Screen
- **2** uses the flare screen and relocates to the wing.
- **1 delivers the pass over the top** to **2** for the **open three-point shot**. [S4, p.34]

## Key Coaching Points
- **Flare screen must be sudden and quick** — x2 must be caught completely off guard. [S4, p.34]
- **Use sparingly** — this play will only deceive the defense once or twice per game. Save it for moments when a three-pointer is critical. [S4, p.34]
- **4's role is dual** — both participating in the ball reversal and blocking their defender from contesting the shot.

## Counters
- If x2 does not fully follow 2 on the dribble toward the top → 2 may have an open shot before the flare even occurs.
- If the flare pass is denied → 1 can reverse the ball to 3 on the weak side.

## Related Plays
- [[blob-stack-zone]] — BLOB zone play that also attacks the 2-3 zone
- [[32-lob]] — another set play vs 2-3 zone using a backdoor lob
- [[blob-stack-double]] — similar shooter-liberation concept in a BLOB context

## Sources
- [S4, pp.33-34] — full play description and coaching points
