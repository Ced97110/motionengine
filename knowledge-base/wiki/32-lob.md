---
type: play
category: offense
formation: 3-out-2-in
tags: [zone-offense, 2-3-zone, lob, backdoor, weak-side, alley-oop, quick-hitter]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: ball-entry-dribble-corner
    role: "2"
    criticality: required
  - id: weak-side-corner-slide
    role: "3"
    criticality: required
  - id: ball-reversal-pass
    role: "2"
    criticality: required
  - id: zone-screen-low-defender
    role: "5"
    criticality: required
  - id: backdoor-hard-cut
    role: "3"
    criticality: required
  - id: lob-pass-delivery
    role: "1"
    criticality: required
  - id: above-rim-finish
    role: "3"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: backdoor-hard-cut
    for_role: "3"
  - region: glute_max
    criticality: required
    supports_technique: backdoor-hard-cut
    for_role: "3"
  - region: ankle_complex
    criticality: required
    supports_technique: backdoor-hard-cut
    for_role: "3"
  - region: core_outer
    criticality: optional
    supports_technique: lob-pass-delivery
    for_role: "1"
  - region: core_outer
    criticality: optional
    supports_technique: zone-screen-low-defender
    for_role: "5"
# Cross-ref edge #8 — analytic signature. See backend/spec/crossref-anatomy-chain.md §M4 signature expansion
produces_signature:
  - factor: efg-pct
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: high
    rationale: "The play's terminal action is a lob to an uncontested cutter at the rim, generating a layup or dunk — the highest-efficiency shot in basketball."
  - factor: tov-pct
    direction: protects
    concept_slug: concept-four-factors
    magnitude: medium
    rationale: "The scripted 3-pass sequence (entry to 2 → reversal to 1 → lob to 3) limits improvised decision-making and reduces live-ball turnover exposure compared to motion offense."
  - factor: ppp
    direction: lifts
    concept_slug: concept-four-factors
    magnitude: high
    rationale: "A designed lob to an open cutter behind a zone screen consistently produces a high-probability two-point finish, inflating points-per-possession when the play succeeds."
  - factor: pace
    direction: lowers
    concept_slug: concept-four-factors
    magnitude: low
    rationale: "The multi-phase zone manipulation (corner dribble, weak-side slide, reversal) consumes deliberate clock before the scoring action, slightly reducing overall pace."
# Cross-ref edge — counters provenance (M4 part 3). extraction labels gate which bullets are surface-safe.
counters:
  - text: "When 3's backdoor cut is sealed off by the defense, 1 pivots the read to 4 sealing in the paint for a post touch, or the offense resets to its half-court alignment."
    extraction: llm-inferred
---

# 32 Lob (Set Play vs 2-3 Zone)

## Overview
Designed to score a backdoor lob for an athletic perimeter player against a 2-3 zone. The play overloads the zone to one side, then uses a weak-side screen to open a clear lane for the lob pass and finish (dunk or layup). Like all surprise plays, it works best 1–2 times per game. [S4, pp.35-36]

## Formation
- Starts in a **3-out, 2-in formation**
- **1** at the top/wing, **2** at ball-side wing, **3** at weak-side wing
- **4** and **5** at the high post / inside

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":33},{"role":"2","x":-18,"y":22},{"role":"3","x":18,"y":22},{"role":"4","x":-5,"y":36},{"role":"5","x":5,"y":36}],"actions":[{"from":"1","to":"2","type":"pass"}],"notes":"Extracting the first (topmost) diagram on p.35, which shows the initial 3-out 2-in setup. 1 is at the top of the key area (slightly below the free-throw line extended), 2 at the left wing, 3 at the right wing, and 4 & 5 are inside the paint near the high-post/elbow area. The only action arrow clearly shown in the first diagram is 1 passing to 2. The diagram labels show a circle around player 1 at the top indicating the starting ball handler, with a dashed pass arrow going toward 2 on the left wing."}
```

## Phases

### Phase 1: Ball Entry — Force Zone to Shift
- **1** passes to **2** (the perimeter player who will NOT receive the lob).
- **2 dribbles toward the corner**, forcing **x4** (the zone's low defender on that side) to track the ball. This means **x5 will take responsibility for 4** in the paint. [S4, p.35]

### Phase 2: Weak-Side Slide
- As **2 dribbles to the corner**, **3 slides down to the weak-side corner** — moving behind the sight lines of the defense so the action is not telegraphed. [S4, p.35]

### Phase 3: Ball Reversal — Zone Committed
- **2 passes back to 1** on the wing (or top).
- The zone defense is now committed to the strong side.

### Phase 4: Screen on Weak-Side Low Defender
- **5 establishes position behind x4** (the low zone defender on the strong side who has tracked the ball) and **nudges them up the lane**, creating space on the baseline. [S4, p.35]

### Phase 5: Backdoor Lob
- **3 cuts hard to the rim** behind 5's screen on the baseline.
- **1 delivers a lob pass** to 3 for the **easy finish at the rim**. [S4, p.35]

## Key Coaching Points
- **Use this play sparingly** — it is a surprise play and will not work if overused. [S4, p.36]
- **3 must slide to the weak-side corner undetected** — moving too early or too obviously tips off the defense.
- **1 must be able to throw an accurate lob** — timing and placement are critical for 3 to finish in traffic.
- **Crowd engagement**: lob plays are excellent for morale and energy — use them with athletic players who can dunk or finish above the rim. [S4, p.36]

## Counters
- If 3 is cut off on the backdoor → 1 can look for 4 sealing in the paint or reset to the half-court set.

## Related Plays
- [[23-flare]] — another quick-hitter set play vs 2-3 zone
- [[blob-stack-zone]] — BLOB zone play also targeting gaps in the 2-3 zone
- [[blob-flip]] — also uses a lob pass as a safety valve option

## Sources
- [S4, pp.35-36] — full play description and coaching points
