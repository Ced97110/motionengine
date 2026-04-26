---
type: play
category: offense
formation: 4-out 1-in
tags: [post-isolation, mismatch, low-post, foul-trouble, spacing, perimeter-screens]
source_count: 1
last_updated: 2026-04-11
# Cross-ref edge #1 — anatomy chain. See backend/spec/crossref-anatomy-chain.md §4.1
demands_techniques:
  - id: low-post-flash-on-entry
    role: "5"
    criticality: required
  - id: post-entry-pass-from-wing
    role: "3"
    criticality: required
  - id: low-post-isolation-move
    role: "5"
    criticality: required
  - id: wing-to-slot-screen-exchange
    role: "2"
    criticality: required
  - id: post-kickout-pass
    role: "5"
    criticality: optional
  - id: catch-and-shoot-perimeter
    role: "1"
    criticality: optional
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    supports_technique: low-post-flash-on-entry
    for_role: "5"
  - region: glute_max
    criticality: required
    supports_technique: low-post-isolation-move
    for_role: "5"
  - region: core_outer
    criticality: required
    supports_technique: low-post-isolation-move
    for_role: "5"
  - region: ankle_complex
    criticality: optional
    supports_technique: wing-to-slot-screen-exchange
    for_role: "2"
---

# Inside Isolate

## Overview
A half-court set play that isolates the team's best mismatch on the low post while keeping four perimeter players active above the free-throw line. The perimeter action (wing-to-slot screen exchanges) occupies defenders and prevents help defense from collapsing. Especially effective against youth teams where help defense is not well-understood, or against a defender in foul trouble. [S4, pp.64-65]

## Formation
4-out 1-in: 5 at the high post (near the foul line), 1 at the top, 2 and 3 in the slots, 4 and the other wing above the free-throw line. 5 is the post isolation target. [S4, p.64]

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":30},{"role":"2","x":-8,"y":22},{"role":"3","x":18,"y":22},{"role":"4","x":-18,"y":22},{"role":"5","x":0,"y":29}],"actions":[{"from":"1","to":"3","type":"pass"},{"from":"5","to":"right_low_block","type":"cut"}],"notes":"Phase 1 (first/top diagram) is extracted. The setup shows a 4-out 1-in formation: 1 at the top of the key, 2 and 3 in the slots/wings (2 slightly left of center, 3 on the right wing), 4 on the left wing, and 5 near the high post/foul line area. The diagram shows 1 passing to 3 on the ball-side (right) wing, and 5 flashing down toward the low post on the ball side. 5's starting position in the diagram appears near the free-throw line/high post area before the flash."}
```

## Phases

### Phase 1: Wing Entry & Flash
- Play begins with 1 passing to either wing (3 in this example).
- As soon as the pass is made, 5 immediately flashes toward the ball to the low post to take advantage of their mismatch. [S4, p.64]

### Phase 2: Post Feed & Perimeter Distraction
- 3 passes into 5 on the low post.
- Simultaneously, the wing players both screen up for the slot players and they exchange positions (constant movement above the free-throw line). This keeps defenders occupied and prevents them from sagging to help on 5. [S4, p.64]

### Phase 3: Post Isolation
- 5 works 1-on-1 in the low post. Options include:
  - Backing down the defender for a power move
  - Facing up and attacking middle
  - Facing up and attacking baseline [S4, p.64]

## Key Coaching Points
- This play can exploit **any** mismatch in the post — it is not limited to the center or power forward. Even a point guard with a favorable mismatch can be isolated inside. [S4, p.65]
- Excellent against a defender **in foul trouble**: post them up and have the offensive player attack off the dribble; they will likely foul again. [S4, p.65]
- Players should **avoid passing into the post from the slot position** unless it is completely open, as slot-to-post passes are easier for the defense to deflect or steal. Entry passes should come from the wing. [S4, p.65]
- Perimeter player movement must be active and purposeful — lazy movement allows defenders to sag and double-team.

## Key Personnel
- **5 (C / Best Post Mismatch)**: The isolation target; must read the defense and execute low-post moves decisively.
- **3 (Wing)**: Entry passer; must deliver a good post entry pass from the wing, not the slot.
- **1, 2, 4**: Perimeter players; must execute active screen exchanges to occupy defenders above the free-throw line.

## Counters
- If the defense double-teams 5, 5 kicks out to the open perimeter player for a catch-and-shoot.
- If the defense denies the post entry pass, 5 can step out to the high post or 3 can dribble closer to improve the passing angle.

## Related Plays
- [[play-flex-warrior]] — another play using active perimeter movement to free post scoring
- [[play-iverson-ram]] — half-court play focused on a different mismatch (guard PnR)
- [[play-high-post-double-screen]] — uses perimeter spacing to create a PnR opportunity for a wing player

## Sources
- [S4, pp.64-65]
