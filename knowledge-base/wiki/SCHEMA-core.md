# Coaching Wiki — Sport-Agnostic Core Schema

> This file extracts the **sport-agnostic** rules from the original
> `knowledge-base/SCHEMA.md`. Every sport (basketball, football, future
> sports) shares the page-type taxonomy, file-naming convention,
> cross-link rules, citation rules, and quality standards. Sport-specific
> details (positions, tag vocabulary, source registry) live in per-sport
> addenda:
>
> - [`basketball/SCHEMA-basketball.md`](basketball/SCHEMA-basketball.md)
> - [`football/SCHEMA-football.md`](football/SCHEMA-football.md)
>
> The parent `knowledge-base/SCHEMA.md` remains the authoritative entry
> point and links into this file plus the per-sport addenda.

## Directory layout

```
knowledge-base/
  raw/                    ← immutable PDFs (never modify)
  wiki/
    SCHEMA-core.md        ← this file (sport-agnostic structure)
    basketball/
      SCHEMA-basketball.md  ← basketball positions / tags / sources
      *.md                  ← basketball wiki pages
      compiled/             ← compiled cross-ref sidecars (basketball)
    football/
      SCHEMA-football.md    ← football positions / tags / sources
      *.md                  ← football wiki pages
      compiled/             ← compiled cross-ref sidecars (football)
```

## Page types (universal)

Every sport's wiki uses the same five page types. The sport addendum
defines which positions, tags, formations, and source IDs are valid.

| Type | Slug prefix | Purpose |
|---|---|---|
| Concept | `concept-` | A strategic idea, principle, or formation |
| Drill | `drill-` | A practice activity that trains a skill |
| Play | `play-` | A specific offensive/defensive sequence |
| Defending | `defending-` | A defensive answer to an offensive concept |
| Source summary | `source-` | One per ingested book |

Per-sport addenda define optional sport-specific subtypes (e.g.
`exercise-` for strength/conditioning under basketball).

## Front-matter shape (universal)

The structural cross-ref edges (`demands_techniques`, `demands_anatomy`,
`trains_techniques`, `trains_anatomy`, `produces_signature`, `counters`)
are **sport-agnostic** — the slugs they reference are sport-scoped, but
the edge names and YAML shapes are the same across sports.

```yaml
---
type: concept | drill | play | defending | source-summary
level: beginner | intermediate | advanced
positions: [...]                # SPORT-SPECIFIC — see addendum
tags: [...]                     # SPORT-SPECIFIC — see addendum
source_count: int
last_updated: YYYY-MM-DD

# Cross-ref edges (universal shapes)
trains_techniques:
  - id: technique-slug-stem
    emphasis: primary | secondary
trains_anatomy:
  - region: anatomy-slug-stem
    emphasis: primary | secondary
demands_techniques:
  - id: technique-slug-stem
    role: "<position>"          # uses sport-specific position vocabulary
    criticality: required | optional
demands_anatomy:
  - region: anatomy-slug-stem
    criticality: required | optional
    supports_technique: technique-slug-stem
    for_role: "<position>"
counters:
  - text: "Motion-voice rewrite of the counter"
    extraction: verbatim | paraphrase | llm-inferred
    source_hint: null | "[Sn, p.X]"
---
```

## File naming (universal)

- **Kebab-case only** — `pick-and-roll-defense.md`, `cover-2-beater.md`
- **Slug uniqueness is per-sport** — basketball and football may both
  have a page called `play-screen-pass.md`; the path discriminates them
- **No spaces, no uppercase, no special chars** except hyphens
- **Source summaries** — `source-{short-name}.md` per sport directory

## Cross-linking rules (universal)

1. Use `[[page-slug]]` (no `.md` extension) for wikilinks
2. Every page MUST link to at least 2 related pages
3. When creating a new page, check the per-sport index for existing
   pages to link to
4. Bidirectional linking: if A links to B, B should link back to A
5. **Wikilinks are sport-scoped** — never link from a basketball page
   to a football page; the resolver does not cross-traverse sports

## Citation rules (universal)

1. Every factual claim MUST cite at least one source
2. Format: `[S1, p.45]` or `[S5, pp.102-108]`
3. Multiple sources: `[S1, p.45; S7, p.201]`
4. **Source IDs are sport-disambiguated** — basketball uses `S1` through
   `S16`; football uses `S20+`. Never reuse an ID across sports.
5. Citations appear only in developer-facing surfaces; user chrome
   never renders source IDs (per IP-rule v2)

## IP rules (universal — restated for cross-sport application)

- Books are internal retrieval substrate only. Their prose never
  surfaces — not quoted, not paraphrased, not attributed
- No team / player / institution names on public surfaces (per-sport
  denylists enforce this; see `frontend/scripts/sport-terms/<sport>.ts`)
- Aggregate language only ("the canon", "coaching thought") — never
  enumerate book titles, page totals, or counts on user chrome

## Ingestion guidelines (universal)

The ingest pipeline (`backend/src/motion/wiki_ops/ingest.py`) reads
this file plus the per-sport addendum at startup. The
sport-specific Claude prompts that compose new wiki pages live in
`backend/src/motion/prompts/<sport>.py` (see Step 4 of the
sport-portable foundations blueprint).

When processing a chunk of PDF content:

1. **One concept per page** — don't combine unrelated concepts
2. **Merge, don't duplicate** — update existing pages rather than
   creating duplicates
3. **Cross-link aggressively** — every concept connects to others
4. **Use coaching language native to the sport** (see addendum's
   translation tables and banned vocabulary)
5. **Preserve specifics** — player counts, positions, timing, angles
6. **Flag diagrams** — if you can interpret a figure, describe the
   positions and movements; otherwise note as
   `<!-- DIAGRAM: needs visual extraction, p.XX -->`

## Quality standards (universal)

A good wiki page:

- Can stand alone — a coach reads it and knows what to do
- Cites its sources — every claim is traceable
- Links to related pages — the wiki is a web, not a list
- Uses sport-native coaching language — see per-sport addendum's
  translation table
- Includes common mistakes — coaches learn from what NOT to do
- Has clear progressions — beginner → intermediate → advanced

## What MUST be defined in the per-sport addendum

The addendum is the only place sport-specific content lives. It must
define:

1. **Position vocabulary** — the literal strings used in `positions:`
   front-matter (basketball: `PG/SG/SF/PF/C`; football: `QB/RB/WR/...`)
2. **Tag vocabulary** — the controlled vocabulary for `tags:` (formations,
   coverages, situations)
3. **Source registry** — `S1` … `Sn` mappings for this sport's books
4. **Sport-specific page subtypes** — beyond the universal five (e.g.
   `exercise-` for basketball strength/conditioning)
5. **Translation table** — anatomy/biomech vocabulary → sport-native
   coach voice (see `feedback-coach-voice-not-clinical.md` memory)
6. **Naming exceptions** — sport abbreviations (PnR for basketball, RPO
   for football) that pass the lint denylist
