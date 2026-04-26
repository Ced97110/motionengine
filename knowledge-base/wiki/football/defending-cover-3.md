---
type: concept
sport: football
category: defense
level: beginner
tags: [defense, cover-3, zone, single-high, free-safety, cornerback, curl-flat, pass-coverage]
source_count: 0
last_updated: 2026-04-26
---

# Cover-3

## Summary
Cover-3 is a single-high zone coverage that divides the deep field into three equal thirds: a left deep third, a middle deep third, and a right deep third. The free safety covers the middle third from the center of the field. Both cornerbacks drop to cover their respective outside thirds. Three underneath defenders — two hook-curl players and a hook or overhang player — cover the intermediate and shallow zones.

Cover-3 is a base coverage because it is easy to teach, disguises well from a two-high pre-snap look, and provides eight defenders at or near the line of scrimmage before the ball is snapped. That run-force capability makes it an effective answer to RPO-heavy offenses that use the threat of the run to clear out the intermediate zones.

## Zone Responsibilities

| Position | Zone | Depth |
|----------|------|-------|
| Left corner (CB) | Deep left third | 15+ yards |
| Free safety (FS) | Deep middle third | 15+ yards |
| Right corner (CB) | Deep right third | 15+ yards |
| Weak OLB / flat | Left curl-flat | 0–15 yards |
| MLB | Middle hook | 0–12 yards |
| Strong OLB / flat | Right curl-flat | 0–15 yards |
| SS | Robber / overhang | 0–8 yards; rotates to run force |

## Structure and Reads

```json name=diagram-positions
{
  "sport": "football",
  "schema_version": "2",
  "field_position": "midfield",
  "los_x": 60,
  "phases": [
    {
      "label": "Cover-3 — single-high shell and zone thirds",
      "players": [
        {"role": "MLB", "x": 56, "y": 26.65, "jersey": "M", "side": "defense", "label": "middle hook zone"},
        {"role": "OLB1","x": 57, "y": 17,    "jersey": "W", "side": "defense", "label": "left curl-flat"},
        {"role": "OLB2","x": 57, "y": 36,    "jersey": "S", "side": "defense", "label": "right curl-flat"},
        {"role": "SS",  "x": 57, "y": 31,    "jersey": "S", "side": "defense", "label": "robber / overhang — rotates to run"},
        {"role": "CB1", "x": 54, "y": 6,     "jersey": "C", "side": "defense", "label": "deep left third"},
        {"role": "CB2", "x": 54, "y": 47,    "jersey": "C", "side": "defense", "label": "deep right third"},
        {"role": "FS",  "x": 48, "y": 26.65, "jersey": "F", "side": "defense", "label": "deep middle third — single high"},
        {"role": "DE1", "x": 62, "y": 20,    "jersey": "E", "side": "defense", "label": "backside edge"},
        {"role": "DT1", "x": 62, "y": 24,    "jersey": "T", "side": "defense", "label": "shade 3-technique"},
        {"role": "DT2", "x": 62, "y": 29,    "jersey": "T", "side": "defense", "label": "shade 3-technique"},
        {"role": "DE2", "x": 62, "y": 33,    "jersey": "E", "side": "defense", "label": "playside edge"}
      ],
      "actions": [],
      "ball": {"x": 60, "y": 26.65, "possessed_by": "offense"},
      "notes": "FS aligns pre-snap at 10 yards depth over the center (single-high). Corners align at 6–8 yards and bail to the deep third at the snap. SS and linebackers own the underneath zones. The SS can rotate to run force or drop into the curl-flat based on the offensive set."
    }
  ]
}
```

## Key Principles

1. **The corners are deep-third players, not press players.** In Cover-3, corners must get to their deep third by ten yards depth on any vertical release. A corner who gets caught underneath at eight yards on a go route surrenders the deep third entirely. The corner's pre-snap alignment is typically five to seven yards off the line of scrimmage to allow the bail.

2. **The free safety owns the deep middle.** The free safety must be positioned to split the difference between any two vertical routes on either side of the field. Pre-snap alignment at ten to twelve yards of depth allows the FS to break on any ball thrown into the deep middle before the receiver arrives.

3. **Curl-flat defenders carry the number-two receiver.** When the slot receiver or tight end releases vertically, the curl-flat defender must carry the route through the intermediate zone until the corner takes it over at the boundary. A curl-flat defender who abandons his zone for the number-one receiver opens the seam immediately.

4. **Run-force from the SS.** The strong safety aligns close enough to provide a plus-one run-force advantage over the formation's attached blockers. Against an RPO with a quick receiver route, the SS must honor the run threat first.

## Vulnerabilities

- **Four verticals against three deep defenders**: four receivers running vertical routes force the three deep players to choose two; one seam is uncovered. The FS must decide which inside vertical to bracket.
- **Smash concept**: a corner route by a receiver running vertically forces the corner to bail to the deep third while a second receiver runs a flat or hitch underneath in the vacated space.
- **Backside out route**: when the curl-flat linebacker sinks on a vertical stem, the corner vacates the short zone on the backside, and the out route hits behind him.
- **Crossing routes at twelve yards**: a dig or crossing route at twelve to fifteen yards splits the depth between the curl-flat zone (0–15 yards) and the deep third (15+ yards) if the curl-flat linebacker overruns or the corner bails prematurely.

## Common Mistakes

1. **Corner bails before reading run** — the corner drops into the deep third before confirming a pass, and the run attacks the flat. Correction: the corner's first read is run or pass key; bail only after confirming pass.
2. **FS over-rotates to one side** — the FS cheats toward a motion or a pre-snap route stem and the backside deep middle opens. Correction: FS stays center until the route stem confirms vertical direction.
3. **Curl-flat defender widens on a flat route** — the linebacker follows the running back into the flat and vacates the curl zone for a receiver running a curl or comeback. Correction: the flat route belongs to the overhang player, not the inside linebacker.

## Related Concepts
- [[defending-cover-2]] — two-high alternative; eliminates the deep middle hole but exposes the seam between the two safety halves
- [[play-rpo-slant]] — Cover-3's hook-curl structure is vulnerable to the RPO slant when the linebacker's curl responsibility holds him in place
- [[play-quick-out]] — Cover-3 corners are deeper pre-snap than Cover-2 corners; the out route can be available at five yards before the corner arrives
- [[play-cover-2-beater-skinny-post]] — the skinny post concept is less effective against Cover-3 than Cover-2 because the FS is already centered
