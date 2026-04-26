---
type: play
sport: football
category: offense
formation: shotgun
tags: [RPO, pass, slant, zone-run, shotgun, quick-game, man-to-man, cover-1, cover-3]
source_count: 0
last_updated: 2026-04-26
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    for_role: RB
  - region: glute_max
    criticality: required
    for_role: RB
  - region: shoulder_girdle
    criticality: required
    for_role: QB
  - region: hip_flexor_complex
    criticality: required
    for_role: WR1
  - region: ankle_complex
    criticality: required
    for_role: WR1
# produces_signature: DEFERRED
# The basketball Four Factors enum (efg-pct, oreb-pct, tov-pct, ftr, ppp,
# pace, floor-pct) does not map to football. A football-specific factor enum
# (e.g. yards-per-carry, completion-pct, explosive-rate, third-down-conv) is
# deferred to the Step 4 prompt-architecture workstream. This field is
# intentionally omitted here rather than borrowing basketball factor slugs.
# See SCHEMA-football.md § Known gaps.
counters:
  - text: "When the overhang defender squeezes inside on the zone run, the quarterback pulls the ball and delivers the slant to the boundary receiver before the corner can rotate."
    extraction: llm-inferred
  - text: "When the corner plays inside leverage on the slant receiver at the snap, the quarterback hands off on the zone run and the running back attacks the outside edge where the corner vacated."
    extraction: llm-inferred
---

# RPO — Slant

## Overview
A run-pass option (RPO) that pairs a one-back inside zone run with a backside slant route. At the snap, the quarterback reads the alignment of a single overhang defender — a linebacker or safety positioned between the box and the boundary. If the defender fills on the run, the quarterback pulls and throws the slant. If the defender stays wide, the quarterback hands off and the run has a numbers advantage at the point of attack.

The RPO is a pre-snap concept. The quarterback's decision is made from the defender's alignment, not from a post-snap scramble drill.

## Formation
Shotgun. QB five yards behind center. RB to QB's right. WR1 split wide to the right (the slant receiver). WR2 split wide to the left. WR3 in the right slot. OL aligned in a standard shotgun 11-personnel spacing.

```json name=diagram-positions
{
  "sport": "football",
  "schema_version": "2",
  "field_position": "midfield",
  "los_x": 60,
  "phases": [
    {
      "label": "RPO Slant — read key and decision point",
      "players": [
        {"role": "QB",  "x": 55, "y": 26.65, "jersey": "QB", "side": "offense", "label": "shotgun 5yd deep"},
        {"role": "C",   "x": 60, "y": 26.65, "jersey": "C",  "side": "offense", "label": "center"},
        {"role": "RB",  "x": 56, "y": 30,    "jersey": "RB", "side": "offense", "label": "right of QB — zone carrier"},
        {"role": "WR1", "x": 60, "y": 48,    "jersey": "X",  "side": "offense", "label": "split wide right — slant"},
        {"role": "WR2", "x": 60, "y": 5,     "jersey": "Z",  "side": "offense", "label": "split wide left — clear"},
        {"role": "WR3", "x": 60, "y": 37,    "jersey": "H",  "side": "offense", "label": "right slot — block or release"}
      ],
      "actions": [
        {"from": "WR1", "to": "WR1_slant", "type": "route", "d": "M 60 48 L 63 48 C 66 46 68 40 69 36", "style": "solid"},
        {"from": "RB",  "to": "RB_run",    "type": "run",   "d": "M 56 30 L 63 30",                     "style": "wavy"},
        {"from": "QB",  "to": "WR1",       "type": "pass",  "d": "M 55 26.65 L 68 39",                  "style": "dashed"},
        {"from": "QB",  "to": "RB",        "type": "run",   "d": "M 55 26.65 L 56 30",                  "style": "wavy"}
      ],
      "ball": {"x": 55, "y": 26.65, "possessed_by": "QB"},
      "notes": "The overhang defender (linebacker or safety aligned outside the box on the right) is the read key. Arrow to WR1 (dashed) represents the throw if the overhang collapses; arrow to RB (wavy) represents the handoff if the overhang holds. QB's footwork stays identical regardless of the decision — there is no tell."
    }
  ]
}
```

## Phases

### Phase 1: Pre-Snap Read
- Before the snap, the quarterback identifies the read key: the defender aligned between the box and the boundary, typically the overhang linebacker or a rotated safety.
- If the defender is inside the box (run responsible), the slant side is one-on-one with the corner — the throw will be available.
- If the defender is outside the box (pass responsible), the run has a numerical advantage inside.

### Phase 2: Snap and Mesh Point
- The center snaps the ball. The offensive line fires off the ball on a zone-run scheme — double teams at the point of attack, backside cutback lane opened by the left guard and tackle.
- The quarterback brings the ball to the mesh point with the RB's belly. The hand-off fake or actual hand-off occurs here.

### Phase 3: Decision
- **Hand off**: if the overhang defender held outside, the ball goes to the RB. The RB reads the first down lineman and presses the zone, cutting backside on the cutback lane or pressing the B gap.
- **Pull and throw**: if the overhang vacated to the run, the QB pulls the ball from the mesh, resets feet, and delivers the slant on a one-step hitch.

### Phase 4: The Slant Throw
- WR1 releases inside on the slant at a forty-five-degree angle after two upfield steps.
- The throw targets the inside shoulder at chest height. The ball is delivered on WR1's second step inside — not after the break is complete.
- WR1 secures the catch, turns upfield, and works the corridor between the emptied linebacker zone and the safety.

## Key Coaching Points
- The quarterback's body language at the mesh point must be identical on give and pull. Any lean or early pull tip telegraphs the decision to the read key.
- WR1's release must be outside-in — a vertical release before the break prevents the corner from undercutting the slant.
- The zone run and the slant route are both live plays. The line blocks the zone run on every snap; the RPO does not create a run/pass conflict for the linemen.
- Against press coverage on WR1, the slant is suppressed because the corner can reroute the release. Use the hand-off and attack the B gap where the overhang over-rotated.

## Counters
- When the overhang fills inside on the zone, the pull-and-throw to the slant exploits the vacated outside zone.
- When the corner takes away the slant with inside leverage, hand off and allow the RB to attack the exposed edge.

## Related Plays
- [[play-quick-out]] — same quick-game timing window; pair with the slant to create a two-way go on man coverage
- [[play-counter-trey]] — heavy run concept that complements the zone-run threat in this RPO
- [[play-cover-2-beater-skinny-post]] — intermediate route that attacks the same inside zone the slant opens when the overhang vacates

## Related Concepts
- [[defending-cover-3]] — the corner-flat structure of Cover-3 often holds the overhang in the curl zone, triggering the hand-off read
- [[defending-cover-2]] — Cover-2's flat-defender responsibility can conflict with the overhang's run key, creating the give window
