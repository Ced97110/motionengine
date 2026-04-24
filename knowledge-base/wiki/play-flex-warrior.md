---
type: play
category: offense
formation: horns
tags: [flex-screen, screen-the-screener, down-screen, post-up, catch-and-shoot, half-court]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: flex-screen-set
    role: "1"
    criticality: required
  - id: flex-cut-to-rim
    role: "2"
    criticality: required
  - id: down-screen-set
    role: "5"
    criticality: required
  - id: catch-and-shoot-off-screen
    role: "1"
    criticality: required
  - id: second-screen-set
    role: "5"
    criticality: optional
  - id: post-seal-deep
    role: "5"
    criticality: optional
  - id: wing-catch-and-shoot
    role: "2"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: flex-cut-to-rim
    for_role: "2"
  - region: glute_max
    criticality: required
    supports_technique: flex-cut-to-rim
    for_role: "2"
  - region: ankle_complex
    criticality: required
    supports_technique: catch-and-shoot-off-screen
    for_role: "1"
  - region: core_outer
    criticality: optional
    supports_technique: post-seal-deep
    for_role: "5"
  - region: hip_flexor_complex
    criticality: optional
    supports_technique: down-screen-set
    for_role: "5"
  - region: glute_max
    criticality: optional
    supports_technique: post-seal-deep
    for_role: "5"
---

# Flex Warrior

## Overview
A multi-action half-court play from a horns set involving a flex screen, a screen-the-screener action, and a post seal. It creates numerous open shot opportunities for guards and also a deep post-up option. Recommended for high school teams and older due to the timing, screening angles, and shot-making required. [S4, pp.60-61]

## Formation
Horns set: 4 and 5 on the elbows (high post), 2 and 3 on the wings at the level of the lower blocks, 1 at the top of the key with the ball. [S4, p.60]

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":33},{"role":"2","x":22,"y":40},{"role":"3","x":-22,"y":22},{"role":"4","x":-8,"y":29},{"role":"5","x":8,"y":29}],"actions":[{"from":"1","to":"4","type":"pass"},{"from":"1","to":"left_low_block","type":"cut"},{"from":"2","to":"rim","type":"cut"}],"notes":"The first (top) diagram on page 1 is used as the starting formation. This is a horns set: 4 and 5 are on the elbows, 2 is on the right wing at block level, 3 is on the left wing, and 1 starts near the top of the key/free-throw area with the ball. The diagram shows the Phase 1 action: 1 passing to 4 (left elbow), 1 cutting down the lane toward the left low block to set the flex screen for 2, and 2 cutting toward the rim off the flex screen. The diagram appears mirrored relative to prose (pass goes to 4 on the left elbow, 2 starts right wing), which matches the first diagram's depiction."}
```

## Phases

### Phase 1: Flex Screen Action
- 1 passes to 4 on the elbow (preferably on the side of the team's best scorer on the wing).
- 1 then cuts down the center of the lane and sets a flex screen for 2.
- 2 can cut either high or low off the flex screen and looks for the pass from 4 for an easy layup. [S4, p.60]

### Phase 2: Screen-the-Screener (STS)
- As 2 uses the flex screen, 5 sets a down screen for 1 — a classic screen-the-screener action.
- 1 uses the down screen and cuts to the top of the elbow or slot, looking for the catch-and-shoot. [S4, p.60]

### Phase 3: Second Screen for 2 & Post Seal
- After screening for 1, 5 immediately sets another screen for 2, who cuts out to the wing.
- If 1 was not open for the shot, 1 swings the basketball to 2, who should be open on the wing. [S4, p.61]
- After screening 2's player, 5 attempts to get a deep seal in the paint. If 2 is not open, 2 can pass in to 5 for the score. [S4, p.61]

## Key Coaching Points
- 1 should pass to the elbow on the side of the team's best scorer to favor that side. [S4, p.61]
- All screens must be set with correct timing and angles — a poorly timed flex screen or down screen collapses the whole action. [S4, p.61]
- Shot selection is crucial: players must be willing to pass up an acceptable shot for an excellent one. [S4, p.61]
- This play is **not recommended for youth teams** due to its complexity in timing and spacing.

## Key Personnel
- **1 (PG)**: Passer, flex screener, then shooter off the down screen. Must be able to consistently hit the open catch-and-shoot.
- **2 (SG)**: Primary off-ball cutter; cuts off flex screen to the rim, then off a second screen to the wing for a shot.
- **3 (SF)**: Weakside spacing; stays wide to occupy their defender.
- **4 (PF)**: Elbow receiver; looks to feed 2 on the flex cut, then 1 off the STS action.
- **5 (C)**: Key screener throughout — sets the STS down screen for 1, then another screen for 2, then seals deep in the paint.

## Counters
- If x2 goes over the flex screen, 2 can pop to the corner instead.
- If the defense cheats on the STS, 1 can cut backdoor instead of popping to the slot.
- 5's post seal after screening is a built-in counter when perimeter options are contested.

## Related Plays
- [[play-drive-hammer]] — another box/horns play with screen-the-screener concepts
- [[concept-setting-screens]] — angle and timing principles for all screens in this play
- [[concept-reading-screens-off-ball]] — how 2 and 1 read their defenders off the flex and down screens

## Sources
- [S4, pp.60-61]
