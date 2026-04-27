---
type: concept
sport: football
category: defense
level: intermediate
tags: [defense, cover-2, zone, two-deep, flat-defender, cornerback, safety, pass-coverage]
source_count: 0
last_updated: 2026-04-26
---

# Cover-2

## Summary
Cover-2 is a two-deep zone coverage that divides the field into five underneath zones and two deep halves. Each safety is responsible for half the field from fifteen yards to the end zone. The two cornerbacks are not deep-half players; they carry the flat zones to approximately eight yards depth before handing routes off vertically to the safeties. Three linebackers or a combination of linebacker and nickel cover the hook-curl and middle zones underneath.

The structure places the entire burden of deep coverage on the two safeties. Its vulnerability is any route concept that splits the seam between the two halves, which is why the skinny post and the seam route are the primary offensive answers.

## Zone Responsibilities

| Position | Zone | Depth |
|----------|------|-------|
| Left corner (CB) | Left flat | 0–8 yards |
| Right corner (CB) | Right flat | 0–8 yards |
| Left safety (SS/FS) | Deep left half | 15+ yards |
| Right safety (SS/FS) | Deep right half | 15+ yards |
| OLB / curl-flat | Left curl zone | 8–15 yards |
| MLB | Middle hook | 0–12 yards |
| OLB / curl-flat | Right curl zone | 8–15 yards |

## Structure and Reads

```json name=diagram-positions
{
  "sport": "football",
  "schema_version": "2",
  "field_position": "midfield",
  "los_x": 60,
  "phases": [
    {
      "label": "Cover-2 — zone responsibilities and alignment",
      "players": [
        {"role": "MLB", "x": 56, "y": 26.65, "jersey": "M", "side": "defense", "label": "middle hook zone"},
        {"role": "OLB1","x": 56, "y": 17,    "jersey": "W", "side": "defense", "label": "left curl-flat zone"},
        {"role": "OLB2","x": 56, "y": 36,    "jersey": "S", "side": "defense", "label": "right curl-flat zone"},
        {"role": "CB1", "x": 61, "y": 6,     "jersey": "C", "side": "defense", "label": "left flat — carry to 8yds"},
        {"role": "CB2", "x": 61, "y": 47,    "jersey": "C", "side": "defense", "label": "right flat — carry to 8yds"},
        {"role": "FS",  "x": 50, "y": 14,    "jersey": "F", "side": "defense", "label": "deep left half"},
        {"role": "SS",  "x": 50, "y": 39,    "jersey": "S", "side": "defense", "label": "deep right half"},
        {"role": "DE1", "x": 62, "y": 20,    "jersey": "E", "side": "defense", "label": "backside DE — contain"},
        {"role": "DT1", "x": 62, "y": 24,    "jersey": "T", "side": "defense", "label": "inside rush"},
        {"role": "DT2", "x": 62, "y": 29,    "jersey": "T", "side": "defense", "label": "inside rush"},
        {"role": "DE2", "x": 62, "y": 33,    "jersey": "E", "side": "defense", "label": "playside DE — contain"}
      ],
      "actions": [],
      "ball": {"x": 60, "y": 26.65, "possessed_by": "offense"},
      "notes": "Zone shading: CBs carry their flat zones until the receiver passes 8 yards, then pass off to the curl-flat linebacker. Safeties read the number-two receiver on their side and rotate to carry any vertical threat above 15 yards. MLB walls the inside breaking routes in the middle hook zone."
    }
  ]
}
```

## Key Principles

1. **The corner carries, then walls.** On a vertical release by the outside receiver, the corner must carry the route to the top of his flat zone (eight yards) before handing off to the curl-flat linebacker. If the corner bails too early, the flat is open underneath. If the corner bails too late, the curl-flat linebacker is isolated deep against a vertical stem.

2. **The safety reads the number-two receiver.** The inside receiver on each side determines the safety's pre-snap alignment and post-snap rotation. If the number-two receiver runs a vertical route (seam, post), the safety must match him deep before rotating to his half responsibility.

3. **Wall the seam.** The most dangerous route against Cover-2 is the seam route by a tight end or slot receiver attacking the gap between the hash and the safety's half. The curl-flat linebacker walls the seam route at the hash until the safety takes it over above fifteen yards.

4. **The hole in Cover-2.** The boundary between the two deep halves, roughly over the middle of the field at fifteen to twenty yards, is the structural vacancy. Routes that split this gap — skinny post, crossing route, deep curl converting to a post — attack the coverage's fundamental weakness. Disguising the split point with the safety's pre-snap depth reduces this exposure.

## Vulnerabilities

- **Skinny post**: an inside-breaking route at a shallow angle splits the two safeties before either can rotate to it. See [[play-cover-2-beater-skinny-post]].
- **Four verticals**: all four receivers running vertical routes force the two safeties to choose which route to carry; one seam will be uncovered.
- **Flat-and-out combination**: the corner's flat responsibility is attacked by a shallow cross that pulls the corner inside while the outside receiver runs an out route behind the vacated zone.
- **Over-loaded flat**: trips formation to one side forces the corner to cover two receivers in the flat zone; one will be free.

## Common Mistakes

1. **Corner releases too early** → the outside receiver runs an eight-yard out behind the corner who has already bailed into a deep third. Correction: the corner must maintain inside leverage and carry the flat zone.
2. **Safety over-rotates** → the safety rotates to the number-two receiver's vertical stem and the backside half is uncovered. Correction: the safety carries his half first; only man-match a number-two receiver when the curl-flat linebacker confirms help.
3. **MLB abandons the middle hook** → the linebacker over-pursues a crossing route and opens the hook zone for a dump-off. Correction: wall the hook zone before rotating to the crossing route.

## Related Concepts
- [[defending-cover-3]] — single-high alternative; the free safety is centered and the corners have deeper responsibilities, eliminating the seam-between-halves gap
- [[play-cover-2-beater-skinny-post]] — the primary offensive answer to this coverage
- [[play-screen-pass]] — the flat-carry responsibility of Cover-2 corners makes them vulnerable to screen-blocking when they widen
