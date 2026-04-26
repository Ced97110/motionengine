---
type: play
sport: football
category: offense
formation: i-formation
tags: [gap-run, counter, power, i-formation, man-to-man, run-blocking, goal-line, red-zone]
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
  - region: core_outer
    criticality: required
    for_role: RB
  - region: glute_max
    criticality: required
    for_role: FB
  - region: hip_flexor_complex
    criticality: optional
    for_role: FB
counters:
  - text: "When the backside linebacker scrapes hard across the line expecting the counter, the fullback kicks out that linebacker instead of the defensive end, and the running back bends the path one gap wider."
    extraction: llm-inferred
  - text: "When both linebackers flow immediately to the back's initial step, reset the series with a true inside zone run; the counter's misdirection value depends on the defense respecting the initial fake."
    extraction: llm-inferred
---

# Counter Trey

## Overview
A gap-running play built on misdirection and double-team blocking. The running back takes a step away from the point of attack on the snap, pulling the linebackers to the backside. Two blockers — a pulling guard and the fullback — then kick out and lead through the playside C gap while the offensive line down-blocks and seals the backside defenders. The result is a numbers advantage at the point of attack created by the combination of misdirection and pulling blockers.

## Formation
I-formation. QB under center. FB directly behind QB at three yards depth. RB four yards behind QB. WR1 split right. WR2 split left. TE aligned right on the line.

```json name=diagram-positions
{
  "sport": "football",
  "schema_version": "2",
  "field_position": "plus-territory",
  "los_x": 72,
  "phases": [
    {
      "label": "Counter Trey — backfield misdirection and pulling blockers",
      "players": [
        {"role": "QB",  "x": 70, "y": 26.65, "jersey": "QB", "side": "offense", "label": "under center"},
        {"role": "C",   "x": 72, "y": 26.65, "jersey": "C",  "side": "offense", "label": "center"},
        {"role": "LT",  "x": 72, "y": 18,    "jersey": "LT", "side": "offense", "label": "down-block backside"},
        {"role": "LG",  "x": 72, "y": 22,    "jersey": "LG", "side": "offense", "label": "pulling to playside"},
        {"role": "RG",  "x": 72, "y": 31,    "jersey": "RG", "side": "offense", "label": "down-block inside"},
        {"role": "RT",  "x": 72, "y": 35,    "jersey": "RT", "side": "offense", "label": "down-block inside"},
        {"role": "TE",  "x": 72, "y": 39,    "jersey": "Y",  "side": "offense", "label": "down-block inside"},
        {"role": "FB",  "x": 67, "y": 26.65, "jersey": "FB", "side": "offense", "label": "lead through — kick out DE"},
        {"role": "RB",  "x": 65, "y": 26.65, "jersey": "RB", "side": "offense", "label": "counter step left, run right"},
        {"role": "WR1", "x": 72, "y": 47,    "jersey": "X",  "side": "offense", "label": "crack or stalk"},
        {"role": "WR2", "x": 72, "y": 6,     "jersey": "Z",  "side": "offense", "label": "backside stalk"}
      ],
      "actions": [
        {"from": "RB",  "to": "RB_step",   "type": "run",   "d": "M 65 26.65 L 63 28 L 70 31", "style": "wavy"},
        {"from": "LG",  "to": "LG_pull",   "type": "run",   "d": "M 72 22 C 73 24 74 27 76 31", "style": "solid"},
        {"from": "FB",  "to": "FB_lead",   "type": "run",   "d": "M 67 26.65 L 72 31",          "style": "solid"},
        {"from": "LT",  "to": "LT_down",   "type": "block", "d": "M 72 18 L 74 21",             "style": "solid"},
        {"from": "RG",  "to": "RG_down",   "type": "block", "d": "M 72 31 L 74 29",             "style": "solid"}
      ],
      "ball": {"x": 70, "y": 26.65, "possessed_by": "QB"},
      "notes": "RB takes one step toward the left B gap to pull the linebackers, then plants the left foot and angles to the right C gap. FB kicks out the playside defensive end (DE). LG pulls along the line of scrimmage and leads through the C gap to block the playside linebacker. LT and the right side down-block to seal the backside defenders."
    }
  ]
}
```

## Phases

### Phase 1: Snap and Misdirection Step
- QB receives the snap under center and opens to the right for the handoff while the backfield movement reads as a left run.
- RB takes one aggressive step to the left — the counter step. This step must sell the initial direction; a weak step does not pull the linebackers.
- FB takes a lead step forward and to the right toward the playside C gap.

### Phase 2: Pulling Blockers Launch
- LG pulls immediately at the snap, running the line of scrimmage to the right. LG's aiming point is the inside hip of the defensive end.
- The backside linemen (LT, C) down-block to seal the backside defenders and prevent pursuit.
- RG and RT double-team the playside defensive tackle, creating a vertical push at the point of attack.

### Phase 3: RB Plants and Attacks the C Gap
- After the counter step, RB plants the left foot and redirects hard to the right, receiving the handoff from QB.
- RB reads the FB's kick-out block: if the DE is sealed inside, press the C gap. If the DE fights outside, bend the path one gap wider around the block.
- The cut is explosive — hip flexors and glutes generate the direction change in a single step. Any rounding of the path gives the linebacker time to close.

### Phase 4: Lead Block and Downhill Run
- FB arrives at the C gap just before RB, delivering the kick-out on the defensive end.
- LG arrives second through the gap and climbs to the second level to block the playside linebacker.
- RB reads LG's block: if LG seals the linebacker inside, press outside. If LG is blocked outside, cut inside the block.

## Key Coaching Points
- The counter step is a one-step fake only. Two steps give the linebackers enough time to redirect and close; one decisive step is all the misdirection needed.
- LG's pull path stays tight to the line of scrimmage. A looping pull exposes the back to the linebacker before the lead block arrives.
- RB's decision point is the kick-out block, not the hole. The hole moves based on the DE's reaction.
- The double-team at the point of attack must generate vertical displacement. A stalemate gives the linebacker a free run to the gap.

## Counters
- If the backside linebacker scrapes hard expecting the counter, the FB adjusts the kick-out to the linebacker and the RB bends outside.
- If both linebackers flow immediately to the misdirection step, the misdirection has failed; install an inside zone to punish their aggression.

## Related Plays
- [[play-rpo-slant]] — the zone-run component of the RPO complements counter trey; zone forces linebackers to honor the backside, widening the counter path
- [[play-screen-pass]] — when the defense over-pursues the counter trey, the screen pass attacks the same over-pursuit in space
- [[play-quick-out]] — quick game that forces cornerbacks to stay on their receivers rather than contributing to run support

## Related Concepts
- [[concept-anatomy-hip-flexor-complex]] — the explosive direction change on the counter step demands full hip-flexor activation
- [[concept-anatomy-glute-max]] — horizontal propulsion through the C gap on the cut requires maximum glute engagement
