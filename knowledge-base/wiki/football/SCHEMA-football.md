# Football Coaching Wiki — Sport-Specific Schema

> Sport-specific addendum to `../basketball/SCHEMA.md` (or whatever the
> SCHEMA core split lands as in Step 4 of the sport-portable foundations
> blueprint). This file is a **placeholder** — the football corpus is not
> yet ingested. Authoring begins after blueprint Steps 1-5 are complete.

## Position vocabulary

```
Offense: QB, RB, FB, WR, TE, OL (LT/LG/C/RG/RT)
Defense: DL (DE/DT/NT), LB (ILB/OLB/MLB), DB (CB/S/SS/FS), NB (nickel)
Special teams: K, P, LS, KR, PR
```

## Tag vocabulary (drafts — finalize when content authoring begins)

```
Formations:    pro, shotgun, pistol, i-formation, singleback,
               5-wide, empty, jumbo, goal-line
Concepts:      RPO, play-action, screen, zone-run, gap-run, draw,
               quick-game, dropback, rollout
Coverages:     cover-0, cover-1, cover-2, cover-3, cover-4, cover-6,
               man-free, palms, quarters
Fronts:        4-3, 3-4, nickel, dime, 46, bear
Pressure:      blitz, twist, stunt, simulated-pressure
Situation:     red-zone, two-minute, third-down, fourth-down,
               goal-line, two-point
```

## File naming convention

Same prefix conventions as basketball:

- `play-<slug>.md` — one play
- `concept-<slug>.md` — atomic football idea (e.g. `concept-rpo-mesh-point`)
- `defending-<slug>.md` — defensive answer to an offensive concept
- `drill-<slug>.md` — practice drill
- `exercise-<slug>.md` — strength/conditioning movement (shared anatomy
  vocabulary applies)

## Source registry (TBD)

Football PDFs not yet ingested. The `sources.py` registry will gain
entries like `S20: "football-coaching-bible.pdf"` when content authoring
begins. Source IDs use a different range (S20+) to keep basketball/football
citations disambiguated in tooling.

## What does NOT need to change vs basketball

- Cross-ref edge schema (`play↔drill↔anatomy↔technique↔defending`) —
  topology is sport-agnostic
- Anatomy front-matter (body regions are universal)
- Compiled sidecar names + JSON shape (`crossref.py` builds the same set)
- Eval harness format
- IP scrubber pattern (just a different denylist file)
