---
type: play
sport: football
category: offense
formation: shotgun
tags: [pass, dropback, cover-2, post, seam-route, shotgun, play-action, intermediate]
source_count: 0
last_updated: 2026-04-26
demands_anatomy:
  - region: shoulder_girdle
    criticality: required
    for_role: QB
  - region: hip_flexor_complex
    criticality: required
    for_role: WR1
  - region: glute_max
    criticality: required
    for_role: WR1
  - region: ankle_complex
    criticality: optional
    for_role: WR2
defends_against:
  - slug: defending-cover-2
    shared_tags: [cover-2, post]
counters:
  - text: "When the free safety rotates to the post side before the snap, redirect WR1 to a corner route outside the safety's leverage and deliver the ball to the vacated seam."
    extraction: llm-inferred
  - text: "When both safeties stay deep and the corner walls at twelve yards, check down to the running back on a wheel route into the flat where no defender is aligned."
    extraction: llm-inferred
---

# Cover-2 Beater — Skinny Post

## Overview
An intermediate dropback concept designed to attack Cover-2 between the deep halves. The primary receiver runs a skinny post — an inside-breaking route at a shallow angle — into the vacancy between the two deep safeties at twelve to fifteen yards depth. The quarterback targets the inside hip of the free safety: the ball is delivered before the safety can rotate inside to cut it off. This concept is a direct answer to any Cover-2 or Tampa-2 shell where the safeties split the field into equal halves.

## Formation
Shotgun. QB five yards behind center. WR1 split wide right (the primary post runner). WR2 split wide left (occupy the backside safety). TE aligned right on the line. RB to the left of QB. WR3 in the left slot as the check-down and flat distributor.

```json name=diagram-positions
{
  "sport": "football",
  "schema_version": "2",
  "field_position": "midfield",
  "los_x": 60,
  "phases": [
    {
      "label": "Cover-2 Beater — skinny post route and coverage stress",
      "players": [
        {"role": "QB",  "x": 55, "y": 26.65, "jersey": "QB", "side": "offense", "label": "shotgun 5yd deep"},
        {"role": "C",   "x": 60, "y": 26.65, "jersey": "C",  "side": "offense", "label": "center"},
        {"role": "WR1", "x": 60, "y": 48,    "jersey": "X",  "side": "offense", "label": "primary — skinny post"},
        {"role": "WR2", "x": 60, "y": 5,     "jersey": "Z",  "side": "offense", "label": "backside — occupy safety"},
        {"role": "WR3", "x": 60, "y": 17,    "jersey": "H",  "side": "offense", "label": "left slot — flat check-down"},
        {"role": "TE",  "x": 60, "y": 31,    "jersey": "Y",  "side": "offense", "label": "seam right — stress middle"},
        {"role": "RB",  "x": 56, "y": 23,    "jersey": "RB", "side": "offense", "label": "protection / check-down"}
      ],
      "actions": [
        {"from": "WR1", "to": "WR1_post", "type": "route", "d": "M 60 48 L 67 48 C 71 46 73 38 74 33", "style": "solid"},
        {"from": "TE",  "to": "TE_seam",  "type": "route", "d": "M 60 31 L 66 30 L 72 29",             "style": "solid"},
        {"from": "WR2", "to": "WR2_go",   "type": "route", "d": "M 60 5 L 72 5",                       "style": "dashed"},
        {"from": "WR3", "to": "WR3_flat", "type": "route", "d": "M 60 17 C 64 15 67 12 69 10",         "style": "dashed"},
        {"from": "QB",  "to": "WR1",      "type": "pass",  "d": "M 55 26.65 C 62 30 68 33 74 33",      "style": "dashed"}
      ],
      "ball": {"x": 55, "y": 26.65, "possessed_by": "QB"},
      "notes": "WR1 releases inside the corner at the top of a seven-step stem, then breaks on a shallow angle between the right half-safety (who must honor WR2's vertical) and the free safety (who cannot rotate inside in time). The TE seam stresses the strong safety to hold his hash responsibility. Ball delivered to WR1's inside hip before the free safety arrives."
    }
  ]
}
```

## Phases

### Phase 1: Seven-Step Drop and Initial Stem
- QB takes a five-step or seven-step drop depending on the protection call.
- WR1 releases vertically, selling a go route for the first six steps. The corner's depth and leverage are set in this window.

### Phase 2: The Post Break
- At six to seven steps, WR1 plants the outside foot and breaks inside at a forty-five-degree angle, aimed at the seam between the hash mark and the far hash.
- The break angle is intentionally shallow — not a true deep post to the goalpost. The objective is to cross the free safety's face at twelve yards, not run behind both safeties at twenty-five yards.

### Phase 3: The Throw Window
- The throw window is narrow: the ball must leave the quarterback's hand before the free safety reads the break and drives inside.
- Target the inside hip of WR1 so the receiver can box out the safety on the catch.
- If the window is closed, the TE running the seam on the right hash is the secondary read. He should be one-on-one with the strong safety who is held wide by WR1's vertical stem.

### Phase 4: After the Catch
- WR1 secures the catch at twelve to fifteen yards and turns upfield between the two safeties.
- The TE's seam route clears the underneath zone, allowing the check-down to WR3 in the flat if the throw goes to the TE rather than WR1.

## Key Coaching Points
- The skinny post is a timing route. The ball is thrown before the safety rotates — the quarterback cannot wait for the receiver to be open.
- WR1's stem must convince the corner that a go route is coming. Any early break tip sends the corner inside and closes the throwing lane.
- The TE's seam is not a decoy. It is a live second read that occupies the strong safety and widens the window for the post.
- Against Tampa-2, the middle linebacker drops into the deep middle seam. The TE seam becomes available earlier as the linebacker opens his hips and sinks; the quarterback shortcuts to the TE.

## Counters
- If the free safety rotates to the post side pre-snap, convert WR1 to a corner route; the ball goes over the corner's outside shoulder.
- Against two-high press, the corner cannot release WR1 inside — the underneath zone opens for the TE and RB immediately.

## Related Plays
- [[play-quick-out]] — short-game complement; run this concept when Cover-2 corners are driving hard on the out route
- [[play-rpo-slant]] — backside slant attacks the same inside zone the skinny post vacates
- [[play-screen-pass]] — slow-developing answer to aggressive two-deep shell corners who fly up on every quick game rep

## Related Concepts
- [[defending-cover-2]] — the specific coverage this play is designed to exploit
- [[defending-cover-3]] — different safety rotation; this post concept is less effective against single-high because the free safety is already centered
