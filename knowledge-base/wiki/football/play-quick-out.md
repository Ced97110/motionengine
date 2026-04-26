---
type: play
sport: football
category: offense
formation: shotgun
tags: [pass, quick-game, out-route, shotgun, man-to-man, cover-1, three-step]
source_count: 0
last_updated: 2026-04-26
demands_anatomy:
  - region: shoulder_girdle
    criticality: required
    for_role: QB
  - region: hip_flexor_complex
    criticality: required
    for_role: WR1
  - region: ankle_complex
    criticality: required
    for_role: WR1
  - region: hip_flexor_complex
    criticality: optional
    for_role: WR2
counters:
  - text: "When the corner drives hard on the out at the snap, the quarterback hitches up and releases the ball over the top on a fade to the same receiver."
    extraction: llm-inferred
  - text: "When the defense rotates to a two-high look pre-snap, check to the in-breaking route on the opposite side where the overhang linebacker is displaced."
    extraction: llm-inferred
---

# Quick Out

## Overview
A three-step dropback concept from shotgun that targets the outside receiver on a five-yard out route. The quarterback reads the leverage of a single outside defender: if the defender is inside, the throw is available immediately on the third step. The play is a high-percentage answer to man-coverage and single-high shells that rewards quick decision-making and a compact throwing motion.

## Formation
Shotgun. QB aligned five yards behind center. WR1 split wide to the right. WR2 split wide to the left. WR3 in the right slot. WR4 in the left slot. RB aligned to the left of QB.

```json name=diagram-positions
{
  "sport": "football",
  "schema_version": "2",
  "field_position": "midfield",
  "los_x": 60,
  "phases": [
    {
      "label": "Quick Out — pre-snap alignment and route",
      "players": [
        {"role": "QB", "x": 55, "y": 26.65, "jersey": "QB", "side": "offense", "label": "shotgun 5yd deep"},
        {"role": "C",  "x": 60, "y": 26.65, "jersey": "C",  "side": "offense", "label": "center at LOS"},
        {"role": "WR1","x": 60, "y": 47,    "jersey": "X",  "side": "offense", "label": "split wide right"},
        {"role": "WR2","x": 60, "y": 6,     "jersey": "Z",  "side": "offense", "label": "split wide left"},
        {"role": "WR3","x": 60, "y": 37,    "jersey": "H1", "side": "offense", "label": "right slot"},
        {"role": "WR4","x": 60, "y": 16,    "jersey": "H2", "side": "offense", "label": "left slot"},
        {"role": "RB", "x": 56, "y": 23,    "jersey": "RB", "side": "offense", "label": "left of QB, check-release"}
      ],
      "actions": [
        {"from": "WR1", "to": "WR1_out", "type": "route", "d": "M 60 47 L 65 47 L 67 50", "style": "solid"},
        {"from": "WR2", "to": "WR2_out", "type": "route", "d": "M 60 6 L 65 6 L 67 3",   "style": "solid"},
        {"from": "WR3", "to": "WR3_cross", "type": "route", "d": "M 60 37 C 65 37 68 30 70 26", "style": "dashed"},
        {"from": "WR4", "to": "WR4_cross", "type": "route", "d": "M 60 16 C 65 16 68 22 70 26", "style": "dashed"},
        {"from": "QB",  "to": "WR1",       "type": "pass",  "d": "M 55 26.65 L 66 50",    "style": "dashed"}
      ],
      "ball": {"x": 55, "y": 26.65, "possessed_by": "QB"},
      "notes": "Primary throw is to WR1 on the five-yard out (solid line). WR3 and WR4 run shallow crosses as distribution and pick options. WR2 runs a mirrored out to the left. RB checks for any free rusher before releasing into the flat."
    }
  ]
}
```

## Phases

### Phase 1: Snap and Three-Step Drop
- QB takes the snap and executes a three-step drop, planting on the third step at five yards depth.
- The drop is compact — the QB's eyes go immediately to WR1 on the right side.

### Phase 2: Leverage Read
- QB reads the alignment of the cornerback on WR1 before the snap.
- If the corner is inside of WR1's alignment (inside leverage), the out route is open on the break.
- If the corner is outside (outside leverage), WR1's break is into the defender's body — see counters below.

### Phase 3: Throw and Follow-Through
- WR1 runs five steps upfield and breaks sharply to the sideline.
- The throw is delivered on WR1's plant foot. A late throw allows the corner to drive on the ball.
- WR1 catches the ball with body turned toward the sideline and gains what is available before stepping out.

## Key Coaching Points
- The quarterback must pre-snap the read. This is a rhythm throw — the decision is made before the snap, not after.
- WR1's break must be decisive. Any rounded cut gives the defender time to drive.
- The ball arrives at WR1's outside shoulder so the catch protects the receiver and discourages the defender from fishing for the strip.
- The release point is over the near hash to the sideline — not looping across the field.

## Counters
- If the corner drives hard on the out, WR1 converts to a fade on the outside shoulder.
- If the defense presents a two-high look at the snap, the quarterback works the crossing routes from the slots into the vacated intermediate zone.

## Related Plays
- [[play-rpo-slant]] — same shotgun alignment; run-pass option using the backside slant instead of the quick out
- [[play-screen-pass]] — slow-developing complement to the quick out; attacks the same defender who is crashing on quick game
- [[play-cover-2-beater-skinny-post]] — intermediate-breaking routes that stress the coverage when corners are jumping quick game

## Related Concepts
- [[defending-cover-2]] — the out route is limited against Cover-2 because the flat defender widens with the out; see the beater concept
- [[defending-cover-3]] — the out route stresses Cover-3 only when the corner is playing curl-flat responsibility; check the corner's alignment pre-snap
