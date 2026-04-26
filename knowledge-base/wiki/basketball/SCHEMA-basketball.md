# Basketball Wiki — Sport-Specific Schema

> Sport-specific addendum to [`../SCHEMA-core.md`](../SCHEMA-core.md).
> The core file owns the page-type taxonomy, file-naming rules,
> cross-link rules, citation rules, and quality standards. This file
> owns the basketball-specific position vocabulary, tag vocabulary,
> source registry, and coach-voice translation table.

## Position vocabulary

```
On-court roles: PG (1), SG (2), SF (3), PF (4), C (5)
```

Front-matter `positions:` and `for_role:` accept either the position
abbreviation (`PG`) or the digit (`"1"`). The cross-ref compiler
normalizes them.

## Tag vocabulary (controlled)

```
Formations:   horns, spread, 1-4-high, 2-3-zone, 3-2-zone, 1-3-1,
              box-and-1, triangle, flex, motion, princeton-cut,
              pistol, side-pick-and-roll, ucla-cut, etc.
Concepts:     ball-screen, flare, slip, backdoor, post-up, hand-off,
              dribble-handoff, pick-and-roll, pick-and-pop, iverson,
              elbow-screen, baseline-screen, cross-screen,
              off-ball-screens, weave, etc.
Coverages:    man-to-man, switch, hedge, drop-coverage, ice, blitz,
              show-and-recover, top-lock, chase, deny, help-defense
Press:        full-court-press, half-court-press, zone-press,
              run-and-jump, trap, scramble
Situation:    transition, half-court, OOB (BLOB / SLOB), ATO,
              press-break, end-of-game, two-for-one, foul-trouble
```

## Source registry

| ID  | Filename                         | Pages |
|-----|----------------------------------|-------|
| S1  | lets-talk-defense.pdf            | 274   |
| S2  | basketball-anatomy.pdf           | 210   |
| S3  | offensive-skill-development.pdf  | 230   |
| S4  | basketball-for-coaches.pdf       | 105   |
| S5  | basketball-shooting.pdf          | 135   |
| S6  | footwork-balance-pivoting.pdf    | 288   |
| S7  | nba-coaches-playbook.pdf         | 371   |
| S8  | speed-agility-quickness.pdf      | 265   |
| S9  | explosive-calisthenics.pdf       | 347   |
| S10–S16 | (additional ingested sources — see `src/motion/wiki_ops/sources.py`) |   |

Citation format: `[S1, p.45]` or `[S5, pp.102-108]`. Source IDs are
basketball-only; football reuses `S20+` (see football addendum).

## Sport-specific page subtypes

In addition to the five universal types defined in core, basketball uses:

- `concept-anatomy-*` — body region (anatomy chain) e.g.
  `concept-anatomy-hip-flexor-complex.md`
- `concept-technique-*` — atomic skill e.g.
  `concept-technique-baseline-drive-on-catch.md`
- `exercise-*` — strength/conditioning movement e.g.
  `exercise-back-squat.md`

## Coach-voice translation table

Per `feedback-coach-voice-not-clinical.md`: anatomy/biomech vocabulary
is structural only (used for graph routing). User-facing prose uses
sport-native words.

```
elbow_complex      -> 'shooting elbow' or 'elbow'
shoulder_girdle    -> 'shoulder' or 'shoulder line'
wrist_complex      -> 'wrist' or 'shooting hand'
ankle_complex      -> 'ankles' or 'feet'
hip_flexor_complex -> 'hips' or 'hip flexors'
glute_max          -> 'glutes' or 'hips'
core_outer         -> 'core'
```

The full translation tables (including measurement-name → tape-language
mappings used by the form-coach surface) live in
`backend/src/motion/prompts/basketball.py` and are consumed by the
service-layer prompt builders.

## Naming exceptions (allowed in slugs / body)

- `PnR`, `PG`, `SG`, `SF`, `PF`, `C` — position abbreviations
- `OOB`, `BLOB`, `SLOB`, `ATO` — game-situation abbreviations
- `2-3-zone`, `1-3-1`, `box-and-1` — defensive formations

## IP-specific notes for basketball

- The book titled "NBA Playbook" is an ingested source; refer to it only
  via `[S7]` in developer-facing citations
- 8 archetypes stand alone — no NBA-player comparisons (Sharpshooter,
  Floor General, Two-Way Wing, Athletic Slasher, Paint Beast, Stretch
  Big, Playmaking Big, Defensive Anchor)
- Team names (Lakers, Celtics, etc.) and NCAA institution names (UCLA,
  Princeton) are denylisted by `frontend/scripts/sport-terms/basketball.ts`
- Player first/last names are denylisted; check
  `frontend/scripts/check-nba-terms.ts` before authoring
