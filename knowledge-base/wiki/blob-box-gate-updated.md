---
type: play
category: out-of-bounds
formation: box
tags: [BLOB, man-to-man, back-screen, gate-screen, cross-screen, post-up, catch-and-shoot, layup]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: back-screen-set
    role: "2"
    criticality: required
  - id: hard-cut-to-rim
    role: "5"
    criticality: required
  - id: gate-screen-set
    role: "3"
    criticality: required
  - id: gate-screen-set
    role: "4"
    criticality: required
  - id: catch-and-shoot-off-screen
    role: "2"
    criticality: required
  - id: cross-screen-set
    role: "1"
    criticality: optional
  - id: post-up-duck-in
    role: "5"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: hard-cut-to-rim
    for_role: "5"
  - region: glute_max
    criticality: required
    supports_technique: hard-cut-to-rim
    for_role: "5"
  - region: ankle_complex
    criticality: required
    supports_technique: catch-and-shoot-off-screen
    for_role: "2"
  - region: core_outer
    criticality: optional
    supports_technique: back-screen-set
    for_role: "2"
---

# BLOB Box Gate

## Overview
From a box formation, the best shooter (2) sets a back screen for the center (5), freeing 5 for a layup. 2 then immediately sprints off a gate screen set by 3 and 4 for a wing catch-and-shoot. As a tertiary action, the inbounder (1) sets a cross screen for 5 to duck in or post up. [S4, pp.21-22]

## Formation
Box formation. 2 (best shooter) starts on the weak-side low block. 5 (best post-up player) starts on the weak-side elbow. 3 and 4 on ball-side elbow and low block respectively. 1 (PG) inbounds. [S4, p.21]

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":-1},{"role":"2","x":-7,"y":40},{"role":"3","x":7,"y":40},{"role":"4","x":8,"y":29},{"role":"5","x":-8,"y":29}],"actions":[{"from":"1","to":"5","type":"pass"},{"from":"2","to":"rim","type":"cut"},{"from":"2","to":"5","type":"screen"}],"notes":"1 inbounds from the top/sideline area (shown at top of diagram, near half-court side). Box formation: 2 on weak-side (left) low block, 5 on weak-side (left) elbow, 3 on ball-side (right) low block, 4 on ball-side (right) elbow. The first diagram shows Phase 1: 1 passes toward 5, and 2 sets a back screen for 5 who cuts to the rim. The diagram is small but the box formation and initial actions are legible."}
```

## Phases

### Phase 1: Back Screen for Center Layup
- 2 sets a back screen for 5.
- 5 cuts hard to the rim looking for the inbound pass and layup.
- Simultaneously, 3 begins moving up the side of the key — **3 cannot move too early or the defense reads the play**.

### Phase 2: Gate Screen for Shooter
- Immediately after setting the back screen for 5, 2 sprints off a gate screen set by 3 and 4.
- 2 catches the ball on the wing for a catch-and-shoot opportunity.
- 3 and 4 clear out to the top of the key after setting the gate screen.
- 1 must pass to 2's **inside shoulder** — a pass to the outside shoulder makes it difficult to catch and shoot. [S4, p.22]

### Phase 3: Cross Screen for Post (Tertiary)
- 1 steps inside the court and sets a cross screen for 5.
- 5 looks to duck in for the pass or post up on the ball-side low block.
- This keeps a strong finisher involved as a third option.

## Key Coaching Points
- PG inbounds so the helper on the cross screen is a **smaller defender** — putting the opponent's point guard on the cross screen help is a size mismatch advantage. [S4, p.22]
- 3 must **wait until 2 is ready to sprint** before initiating the gate — both screeners should arrive simultaneously. [S4, p.22]
- Pass to 2's inside shoulder, not outside body. [S4, p.22]
- 3 cannot tip off the gate by moving too early — wait for 2 to set the back screen first. [S4, p.21]

## Counters
- If the pass to 5 on the layup cut is open, take it immediately before the gate screen develops.
- If 2 is denied off the gate, 5 is available in the post on the cross screen.

## Related Plays
- [[blob-box-gate]] — existing page (update/merge)
- [[blob-4-low-flex]] — another BLOB man play using screen-the-screener
- [[blob-flip]] — BLOB man box play with cross-screen for dual rim attack
- [[blob-yo-yo]] — simple box BLOB using up-screens for post layups

## Sources
- [S4, pp.21-22]
