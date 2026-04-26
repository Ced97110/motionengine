# Football Coaching Wiki — Sport-Specific Schema

> This file is the authoritative front-matter and taxonomy spec for all
> pages under `knowledge-base/wiki/football/`. It is a sport-specific
> addendum that extends the structural conventions established in
> `knowledge-base/wiki/basketball/SCHEMA.md`. Any field or compiler
> behavior not documented here inherits from that file.
>
> **Status**: authoring begins at Step 6 of the sport-portable foundations
> blueprint (2026-04-26). Content is hand-authored; PDF ingestion is a
> separate future workstream.

---

## Position vocabulary

### Offense
| Role ID | Full name | Notes |
|---------|-----------|-------|
| QB | Quarterback | Typically 1 player; referred to by role id in diagram-positions |
| RB | Running back | Includes halfback and fullback alignments |
| FB | Fullback | Heavy-formation variant; modeled as a second RB when relevant |
| WR | Wide receiver | Split end (X), flanker (Z), slot (H); role suffix distinguishes them |
| TE | Tight end | Y receiver; blocks and releases |
| LT | Left tackle | Offensive line; blocks only — no passing or run-carry actions |
| LG | Left guard | |
| C  | Center | Ball-snap action starts the play |
| RG | Right guard | |
| RT | Right tackle | |

### Defense
| Role ID | Full name | Notes |
|---------|-----------|-------|
| DE | Defensive end | Edge rusher in 4-3 / 3-4 |
| DT | Defensive tackle | Interior; NG in 3-4 |
| NT | Nose tackle | 3-4 nose |
| ILB | Inside linebacker | |
| OLB | Outside linebacker | |
| MLB | Middle linebacker | |
| CB | Cornerback | |
| S | Safety (generic) | |
| SS | Strong safety | |
| FS | Free safety | |
| NB | Nickel back | 5th DB in nickel package |
| DB | Dimeback | 6th DB in dime package |

### Special teams
K (kicker), P (punter), LS (long snapper), KR (kick returner), PR (punt returner).

---

## Front-matter spec — `type: play`

```yaml
---
type: play
sport: football          # required for sport-scoped compiler routing
category: offense        # offense | defense | special-teams
formation: shotgun       # see formation vocabulary below
tags: []                 # see tag vocabulary below
source_count: 0          # 0 until PDF ingestion workstream ships
last_updated: YYYY-MM-DD

# Cross-ref edge: anatomy load
demands_anatomy:
  - region: <anatomy-slug>     # reuses basketball anatomy vocabulary
    criticality: required | optional
    supports_technique: <technique-slug>   # omit if no technique page exists yet
    for_role: QB | RB | WR | TE | etc.

# Cross-ref edge: defending (tag intersection)
# Compiler auto-builds play-to-defending.json from shared_tags;
# this block is the explicit-override / extra-context layer.
# Leave omitted if relying solely on compiler tag intersection.
defends_against:
  - slug: defending-<slug>
    shared_tags: []

# Cross-ref edge: stat-signature
# IMPORTANT: basketball uses the Four Factors enum (efg-pct, oreb-pct,
# tov-pct, ftr, ppp, pace, floor-pct). Football does NOT map to these
# factors. A football-specific factor enum is deferred to the Step 4
# prompt-architecture workstream. Until that enum is defined:
#   - Omit produces_signature entirely, OR
#   - Use factor: "yards-per-carry" | "completion-pct" | "explosive-rate"
#     | "third-down-conv" | "red-zone-td-rate" | "to-rate"
#     as provisional slugs (document them here, not invented inline).
# Do NOT borrow basketball factor slugs for football plays.
produces_signature:
  - factor: <football-factor-slug>   # see provisional enum above
    direction: lifts | protects | lowers
    concept_slug: concept-football-factors   # does not yet exist; omit or stub
    magnitude: high | medium | low
    rationale: "<Motion-voice one-liner — no source wording>"

# Cross-ref edge: counters
counters:
  - text: "<declarative Motion-voice sentence>"
    extraction: llm-inferred | human-authored
---
```

---

## Front-matter spec — `type: concept` with defending category

Defending pages use `type: concept` with `category: defense` and tags that
mirror the offensive formation / coverage they describe. The compiler
builds `defending-to-play.json` from shared tag intersection.

```yaml
---
type: concept
sport: football
category: defense
level: beginner | intermediate | advanced
tags: []              # include coverage name as a tag (cover-2, cover-3, etc.)
source_count: 0
last_updated: YYYY-MM-DD
---
```

---

## Tag vocabulary

### Formation tags
```
pro, shotgun, pistol, i-formation, singleback, fullhouse,
5-wide, empty, jumbo, goal-line, heavy, trips, bunch
```

### Concept tags (offensive)
```
RPO, play-action, screen, bubble-screen, tunnel-screen,
zone-run, gap-run, counter, sweep, draw, power,
quick-game, dropback, rollout, sprint-out, waggle,
slant, out-route, post, corner-route, crossing-route,
seam-route, fade, go-route, comeback, curl, dig
```

### Coverage tags (defensive)
```
cover-0, cover-1, cover-2, cover-3, cover-4, cover-6,
cover-2-man, man-free, palms, quarters, tampa-2
```

### Front / pressure tags (defensive)
```
4-3, 3-4, nickel, dime, 46, bear,
blitz, edge-blitz, linebacker-blitz, db-blitz,
twist, stunt, simulated-pressure, zone-blitz
```

### Situation tags
```
red-zone, two-minute, third-down, fourth-down,
goal-line, two-point, backed-up, plus-territory,
opening-drive, comeback, clock-management
```

---

## Diagram-positions schema for football

Football diagram coordinates use the **FootballField** viewBox: `0 0 120 53.3`.
- x-axis: 0 = left goal line, 120 = right goal line (each end zone is 10yd deep)
- y-axis: 0 = bottom sideline, 53.3 = top sideline
- Line of scrimmage (LOS) typically at x = 60 (midfield) unless a specific field
  position is being modeled.

```json
{
  "sport": "football",
  "schema_version": "2",
  "field_position": "midfield",
  "los_x": 60,
  "phases": [
    {
      "label": "<phase description>",
      "players": [
        {
          "role": "QB",
          "x": 55,
          "y": 26.65,
          "jersey": "QB",
          "side": "offense",
          "label": "<optional position note>"
        }
      ],
      "actions": [
        {
          "from": "QB",
          "to": "WR1",
          "type": "pass | run | block | route",
          "d": "M x1 y1 C cx cy x2 y2",
          "style": "solid | dashed | wavy"
        }
      ],
      "ball": {
        "x": 55,
        "y": 26.65,
        "possessed_by": "QB"
      }
    }
  ],
  "notes": "<optional context — no source wording>"
}
```

**Coordinate guide**:
- QB under center (I-formation): `x = los_x - 2, y = midfield_y`
- QB in shotgun (5yd depth): `x = los_x - 5, y = midfield_y`
- WR split wide left: `y` near 5–8 (close to bottom sideline)
- WR split wide right: `y` near 45–48 (close to top sideline)
- Slot WR: `y` at 15–18 (left slot) or 35–38 (right slot)
- TE attached right: `x = los_x, y ≈ 32`
- RB behind QB: `x = los_x - 7, y = midfield_y`
- Hash marks at y ≈ 23.58 (bottom hash) and y ≈ 29.72 (top hash)

---

## File naming convention

Same prefix conventions as basketball:

| Prefix | Page type |
|--------|-----------|
| `play-<slug>.md` | One offensive or defensive play |
| `concept-<slug>.md` | Atomic football concept (e.g. `concept-rpo-mesh-point`) |
| `defending-<slug>.md` | Defensive scheme or coverage answer |
| `drill-<slug>.md` | Practice drill |
| `exercise-<slug>.md` | Strength / conditioning movement |

---

## Anatomy vocabulary

The anatomy slug vocabulary is shared with basketball (`hip_flexor_complex`,
`glute_max`, `ankle_complex`, `core_outer`, etc.). Football positions that
perform different dominant motions map as follows:

| Football motion | Primary anatomy slugs |
|----------------|----------------------|
| QB throw | shoulder_girdle, elbow_complex, core_rotators |
| RB explosive cut | hip_flexor_complex, glute_max, ankle_complex |
| WR route break | hip_flexor_complex, glute_max, ankle_complex |
| OL drive block | glute_max, core_outer, hip_flexor_complex |
| DB backpedal | hip_flexor_complex, ankle_complex |

**Coach voice rule** (per `feedback-coach-voice-not-clinical.md`): surface
these as "throwing shoulder", "hip flexors", "glutes", "ankles" — never
as "shoulder girdle complex", "hip flexor complex", "glenohumeral joint".

---

## Source registry (deferred)

Football PDFs not yet ingested. Source IDs will use S20+ range to keep
basketball citations (S1-S16) and football citations (S20+) disambiguated
in tooling. The canonical registry is `backend/src/motion/wiki_ops/sources.py`.

---

## What does NOT change vs basketball

- Cross-ref edge topology (play↔drill↔anatomy↔technique↔defending) — sport-agnostic
- Compiled sidecar file names and JSON shape (`crossref.py` builds the same set)
- Eval harness format
- IP guard pattern (different denylist file — Step 5 ships `sport-terms/football.ts`)
- `wikilink-graph.json` format

## Known gaps (Step 6 scope)

1. **Football factor enum** — `produces_signature` cannot use basketball Four
   Factors. Provisional slugs defined above. A `concept-football-factors.md`
   page and a formal factor enum belong in the Step 4 prompt-architecture
   workstream, not Step 6.
2. **Technique pages** — no `technique-<slug>.md` pages exist for football yet.
   `demands_techniques` front-matter field is omitted from Step 6 plays.
   Add when technique corpus is authored.
3. **Drill corpus** — no football drills exist yet. `anatomy-to-drill.json`
   sidecar will be empty for football until drill authoring begins.
4. **AutoPlayViewer football animation** — field renders but no ball animator
   exists for football (Step 3 memory: `AutoPlayViewer` football branch is
   field-only). Football `AutoPlayViewer` playback is deferred to a separate
   workstream.
