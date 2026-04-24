---
type: play
category: offense
formation: 1-3-1
tags: [zone-offense, 2-3-zone, step-up-screen, baseline-drive, layup, kickout, surprise-play]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: wing-entry-pass
    role: "1"
    criticality: required
  - id: step-up-screen-set
    role: "4"
    criticality: required
  - id: baseline-drive-on-catch
    role: "2"
    criticality: required
  - id: post-dive-to-rim
    role: "5"
    criticality: required
  - id: dump-off-pass
    role: "2"
    criticality: optional
  - id: kickout-pass
    role: "5"
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
  - region: hip_flexor_complex
    criticality: required
    supports_technique: post-dive-to-rim
    for_role: "5"
  - region: ankle_complex
    criticality: optional
    supports_technique: post-dive-to-rim
    for_role: "5"
  - region: core_outer
    criticality: optional
    supports_technique: step-up-screen-set
    for_role: "4"
---

# Step Up

## Overview
A 2-3 zone play designed to catch the defense off-guard. A wing player receives the ball and immediately attacks baseline off a step-up screen, forcing the zone to rotate and opening a diving post player for a layup — or a kick-out to a wing shooter. Best used 1-2 times per game as a surprise element. [S4, pp.47-48]

## Formation
1-3-1 set. Wings (2 and 3) positioned **slightly lower than free-throw line extended** to ensure the low zone defender must play on-ball. 5 at the high post (free-throw line). 4 in the corner. 1 at the top. [S4, p.47]

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":14},{"role":"2","x":18,"y":24},{"role":"3","x":-18,"y":24},{"role":"4","x":18,"y":10},{"role":"5","x":0,"y":29}],"actions":[{"from":"1","to":"2","type":"dribble"},{"from":"1","to":"2","type":"pass"},{"from":"4","to":"2","type":"screen"},{"from":"2","to":"right_corner","type":"cut"}],"notes":"The first (top) diagram on p.47 shows the 1-3-1 starting formation. 1 is at the top near half-court, dribbling toward the right slot. 2 is on the right wing slightly below free-throw line extended. 3 is on the left wing mirroring 2. 5 is at the high post (free-throw line). 4 is in the right corner/slot area. The diagram shows 1 dribbling toward 2, a pass arrow to 2 on the wing, 4 moving up to set a step-up screen on the baseline side of 2, and 2 beginning to attack baseline. The second diagram shows the continuation (Phase 2 onward) and is not the starting formation."}
```

## Phases

### Phase 1: Wing Entry
- 1 dribbles to a slot position and passes to 2 on the wing.
- As the pass is made, the low wing zone defender (X4) is forced to close out to prevent the outside shot.

### Phase 2: Step-Up Screen and Baseline Attack
- 4 **immediately follows X4** and sets a step-up screen on X4 for 2.
- 2 receives the pass and immediately **attacks baseline on the catch**.
- 2 must be positioned low enough to force X4 to play on-ball, but high enough to still have a clear baseline driving lane. [S4, p.48]

### Phase 3: Force Rotation and Finish
- X5 is forced to rotate to stop 2's baseline drive.
- 5 **dives from the free-throw line to the rim**, receiving the pass from 2 for the open layup. [S4, p.47]
- **Secondary option:** If X3 rotates correctly and quickly enough to stop 5's catch, 5 kicks out to 3 on the weak-side wing who is alone for an open three-point shot. [S4, p.47]

## Key Coaching Points
- 2 must be positioned at the right height: "low enough that it forces the low defender to play on-ball defense on them while high enough to attack the baseline." [S4, p.48]
- This play **only works 1-2 times per game** — save it for crucial moments. [S4, p.48]
- The play works best with a 5 (center) who has "soft hands and is able to pass" — they may need to kick out rather than finish. [S4, p.48]
- The step-up screen element is the key surprise — the defense expects X4 to close out freely.

## Counters
- If X5 doesn't rotate, 2 can finish at the basket directly.
- If 3's wing shot is contested, 3 can pump-fake and drive or reset to 1.

## Related Plays
- [[play-low-split]] — another 1-3-1 zone play targeting the interior with post flashes
- [[play-pick-overload]] — zone play from 1-3-1 using on-ball screen and drive
- [[play-black]] — man-to-man play with similar baseline-drive-then-kick structure

## Sources
- [S4, pp.47-48] — full play description with diagrams
