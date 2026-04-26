---
type: play
sport: football
category: offense
formation: shotgun
tags: [pass, screen, bubble-screen, run-blocking, shotgun, quick-game, man-to-man, cover-1, cover-3]
source_count: 0
last_updated: 2026-04-26
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
    for_role: RB
  - region: glute_max
    criticality: required
    for_role: RB
  - region: ankle_complex
    criticality: required
    for_role: RB
  - region: shoulder_girdle
    criticality: required
    for_role: QB
  - region: hip_flexor_complex
    criticality: optional
    for_role: WR1
counters:
  - text: "When the defense pattern-reads the screen and the linebacker stays home in the flat, the quarterback resets and throws the slant to the boundary receiver who is one-on-one with no help."
    extraction: llm-inferred
  - text: "When the edge rusher chases the screen release and opens the edge, the quarterback keeps the ball on a designed scramble outside the screen side."
    extraction: llm-inferred
---

# Screen Pass

## Overview
A slow-developing pass concept that turns defensive aggression into a liability. The offensive line initially pass-sets before releasing to the second level, creating a wall of blockers for the running back, who leaks into the flat after a brief delay. The quarterback sells the pocket and delivers the ball just before the delayed pass rush arrives, putting the ball in space with blockers already in position.

The screen pass tags are `pass`, `screen`, and `run-blocking`. The `screen` tag is football-specific and sport-scoped: it refers to a screen route, not a ball-screen in the basketball sense. The compiler treats tags as sport-scoped, so `screen` in football wiki pages does not intersect with basketball's `screen` tag when building the cross-ref sidecars.

## Formation
Shotgun. QB five yards behind center. RB to QB's right. WR1 split wide right (occupied cornerback). WR2 split wide left. WR3 in the left slot. OL aligned in standard spacing.

```json name=diagram-positions
{
  "sport": "football",
  "schema_version": "2",
  "field_position": "midfield",
  "los_x": 60,
  "phases": [
    {
      "label": "Screen Pass — OL release and RB receiving in the flat",
      "players": [
        {"role": "QB",  "x": 55, "y": 26.65, "jersey": "QB", "side": "offense", "label": "hold pocket, sell dropback"},
        {"role": "C",   "x": 60, "y": 26.65, "jersey": "C",  "side": "offense", "label": "pass-set then release right"},
        {"role": "RG",  "x": 60, "y": 31,    "jersey": "RG", "side": "offense", "label": "pass-set then pull right"},
        {"role": "RT",  "x": 60, "y": 35,    "jersey": "RT", "side": "offense", "label": "pass-set then lead right"},
        {"role": "LG",  "x": 60, "y": 22,    "jersey": "LG", "side": "offense", "label": "pass-set and hold backside"},
        {"role": "LT",  "x": 60, "y": 18,    "jersey": "LT", "side": "offense", "label": "pass-set and hold backside"},
        {"role": "RB",  "x": 56, "y": 30,    "jersey": "RB", "side": "offense", "label": "delay then leak into flat"},
        {"role": "WR1", "x": 60, "y": 48,    "jersey": "X",  "side": "offense", "label": "stalk-block corner"},
        {"role": "WR2", "x": 60, "y": 5,     "jersey": "Z",  "side": "offense", "label": "crack or stalk"},
        {"role": "WR3", "x": 60, "y": 17,    "jersey": "H",  "side": "offense", "label": "backside clear"}
      ],
      "actions": [
        {"from": "RB",  "to": "RB_flat",  "type": "route",  "d": "M 56 30 C 57 30 59 35 63 38",     "style": "solid"},
        {"from": "RG",  "to": "RG_pull",  "type": "block",  "d": "M 60 31 C 62 33 63 35 65 37",     "style": "dashed"},
        {"from": "RT",  "to": "RT_lead",  "type": "block",  "d": "M 60 35 C 62 36 63 37 66 38",     "style": "dashed"},
        {"from": "C",   "to": "C_release","type": "block",  "d": "M 60 26.65 C 62 30 63 33 65 36",  "style": "dashed"},
        {"from": "WR1", "to": "WR1_stalk","type": "block",  "d": "M 60 48 L 63 48",                 "style": "solid"},
        {"from": "QB",  "to": "RB",       "type": "pass",   "d": "M 55 26.65 L 62 38",              "style": "dashed"}
      ],
      "ball": {"x": 55, "y": 26.65, "possessed_by": "QB"},
      "notes": "RB delays two counts to let the OL sell the pass rush, then leaks into the flat behind the releasing linemen. QB holds the pocket for the same two counts, then delivers a short throw to RB just as the defensive linemen turn their backs chasing upfield. C, RG, RT release to the second level after a brief two-count pass-set."
    }
  ]
}
```

## Phases

### Phase 1: Snap and Pass-Rush Invitation
- At the snap, every offensive lineman executes a legitimate pass set: flat back, arms extended, inviting the pass rush upfield.
- QB takes a five-step drop, eyes downfield, holding the ball as long as possible to draw the pass rush past the ball carrier.
- RB counts two beats before moving.

### Phase 2: RB's Delay and Release
- After two counts, RB slips into the flat on the right side, staying behind the line of scrimmage.
- The delay is the mechanism: the linemen who were engaged in their pass rush are now chasing upfield, past the point where the ball will be thrown.

### Phase 3: OL Releases to the Second Level
- C, RG, and RT disengage from their blocks and release into the flat as pullers, leading RB upfield.
- WR1 engages the cornerback in a stalk block — this is a blocking assignment, not a route. WR1 must seal the cornerback away from the RB's running lane.
- The OL blockers arrive at the second level simultaneously with RB receiving the ball; they do not lead RB by more than one yard or the timing collapses.

### Phase 4: Throw and Execution
- QB delivers a short, catchable throw to RB in the flat.
- The throw is behind the line of scrimmage — this is a legal forward pass at the time of release.
- RB catches the ball, sets his feet, and reads the first blocker. Follow the OL's lead block, cutting behind the guard's seal.

## Key Coaching Points
- The OL pass-set must be convincing. Linemen who immediately turn and release tip the screen and allow defenders to pattern-read it.
- WR1's stalk block is the most important block on the play. The cornerback in open space is the only defender who can stop a gain of ten or more yards.
- QB's eyes must stay downfield for the full two-count delay. A quarterback who looks immediately to the flat signals the screen before the OL can release.
- The screen pass is an answer to a defense that is rushing aggressively. It should not be called against a defense sitting in coverage — the defenders in the flat will be in position to defeat the blocks.

## Counters
- When the defense pattern-reads the screen and holds the flat, the quarterback resets to the boundary slant against single coverage.
- When the edge rusher chases the flat on screen recognition, the QB keeps the ball and runs outside the screen side.

## Related Plays
- [[play-counter-trey]] — the heavy-run complement; when defenders over-pursue the counter trey, the screen attacks the same over-pursuit
- [[play-quick-out]] — same-side quick game that forces corners to stay home rather than crashing on screens
- [[play-rpo-slant]] — the RPO forces linebackers inside; the screen punishes the same linebackers when they over-aggressively fill on the run

## Related Concepts
- [[defending-cover-2]] — Cover-2 flat defenders are the primary screen stoppers; stalk-blocking the flat defender is the key assignment
- [[defending-cover-3]] — the hook-curl zone dropper must carry his defender and cannot drive on the flat; screen is effective against passive Cover-3 hooks
