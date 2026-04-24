# Basketball Coaching Wiki — Schema

> This file tells the LLM how to ingest coaching content and generate wiki pages.
> It is the "constitution" of the wiki. Every ingest, query, and lint operation reads this first.

## Purpose

Build a structured, cross-linked knowledge base from 7 basketball coaching PDFs (2,440 pages).
The wiki replaces RAG — knowledge is compiled once, not re-derived on every query.

## Directory Layout

```
knowledge-base/
  raw/              ← immutable PDFs (never modify)
  wiki/             ← LLM-generated .md pages (LLM owns this entirely)
    index.md        ← master catalog, updated on every ingest
    log.md          ← append-only ingestion history
    *.md            ← concept, drill, play, and source-summary pages
  SCHEMA.md         ← this file (rules for the LLM)
```

## Source Materials

| ID  | Filename                         | Full Title                                                              | Pages |
|-----|----------------------------------|-------------------------------------------------------------------------|-------|
| S1  | lets-talk-defense.pdf            | Let's Talk Defense — Herb Brown                                         | 274   |
| S2  | basketball-anatomy.pdf           | Basketball Anatomy                                                      | 210   |
| S3  | offensive-skill-development.pdf  | Basketball Coaches' Guide to Advanced Offensive Skill Development       | 230   |
| S4  | basketball-for-coaches.pdf       | Basketball For Coaches                                                  | 105   |
| S5  | basketball-shooting.pdf          | Basketball Shooting, Enhanced Edition                                   | 135   |
| S6  | footwork-balance-pivoting.pdf    | The Complete Basketball Coaches Guide to Footwork, Balance, and Pivoting | 288   |
| S7  | nba-coaches-playbook.pdf         | NBA Coaches Playbook — NBCA                                            | 371   |
| S8  | speed-agility-quickness.pdf      | Training for Speed, Agility, and Quickness                              | 265   |
| S9  | explosive-calisthenics.pdf       | Explosive Calisthenics — Superhuman Power, Maximum Speed and Agility    | 347   |

When citing, use the ID: `[S1, p.45]` or `[S5, pp.102-108]`.

## Page Types

### 1. Concept Page

For basketball concepts, strategies, defensive/offensive principles, formations.

```yaml
---
type: concept
level: beginner | intermediate | advanced
positions: [PG, SG, SF, PF, C]  # which positions are most relevant
tags: [offense, defense, transition, half-court, man-to-man, zone, press, etc.]
source_count: 3                   # how many sources contribute to this page
last_updated: 2026-04-11
---
```

**Required sections:**

```markdown
# {Concept Title}

## Summary
1-2 paragraph overview. What is this concept? Why does it matter?

## When to Use
- Game situations, matchups, score context
- What offensive/defensive looks trigger this

## Key Principles
1. Numbered list of core principles
2. Each principle is actionable, not vague
3. Include coaching cues in quotes ("stay low, hands active")

## Player Responsibilities
- **PG**: specific duties
- **SG**: specific duties
- **SF**: specific duties
- **PF**: specific duties
- **C**: specific duties

(Only include positions that are relevant to the concept.)

## Variations
### {Variation Name}
Brief description and when to use it.

## Common Mistakes
1. Mistake → correction
2. Mistake → correction

## Related Concepts
- [[concept-slug]] — how it relates (e.g., "the weak-side rotation that follows")
- [[another-concept]] — relationship

## Sources
- [S1, pp.45-52] — primary explanation of the concept
- [S7, p.201] — variation described by Coach X
```

### 2. Drill Page

For practice drills, exercises, training activities.

```yaml
---
type: drill
level: beginner | intermediate | advanced
positions: [PG, SG, SF, PF, C]
players_needed: 3-5
duration_minutes: 10-15
tags: [shooting, defense, conditioning, ball-handling, passing, rebounding, etc.]
source_count: 1
last_updated: 2026-04-11

# Optional structured cross-refs. The crossref compiler inverts these into
# technique-to-drill.json / anatomy-to-drill.json so the Engine can answer
# "what drill trains technique X" or "what drill loads body region Y" in
# O(1). If the drill's text makes a technique or anatomy region explicit,
# emit the matching entry. Slugs must reference real wiki pages
# (concept-technique-*.md / concept-anatomy-*.md); lint will flag dangling
# refs.
trains_techniques:
  - id: baseline-drive-on-catch   # slug stem of a concept-technique-* page
    emphasis: primary | secondary
trains_anatomy:
  - region: glute_max             # slug stem of a concept-anatomy-* page
    emphasis: primary | secondary
---
```

**Required sections:**

```markdown
# {Drill Name}

## Objective
One sentence: what skill does this drill build?

## Setup
- Number of players
- Court area (half court, full court, paint, etc.)
- Equipment (cones, chairs, etc.)

## Execution
1. Step-by-step instructions
2. Use numbered list
3. Be specific about movements, timing, repetitions

## Coaching Points
- What to watch for
- Common corrections
- Coaching cues in quotes

## Progressions
1. **Beginner**: simplified version
2. **Intermediate**: add complexity
3. **Advanced**: game-speed, decision-making

## Concepts Taught
- [[concept-slug]] — how this drill reinforces the concept

## Sources
- [S5, pp.78-80]
```

### 3. Play Page

For specific offensive/defensive plays with player movements.

```yaml
---
type: play
category: offense | defense | out-of-bounds | press-break | transition
formation: horns | spread | 1-4-high | 2-3-zone | etc.
tags: [ball-screen, flare, slip, backdoor, post-up, etc.]
source_count: 1
last_updated: 2026-04-11

# Optional structured cross-refs. The crossref compiler inverts these into
# play-to-technique.json / play-to-anatomy.json so the Engine can answer
# "what techniques does my 2 need to execute this play" and "what body
# regions are loaded for role X". Slugs must reference real wiki pages
# (concept-technique-*.md / concept-anatomy-*.md); lint will flag dangling
# refs.
demands_techniques:
  - id: baseline-drive-on-catch   # slug stem of a concept-technique-* page
    role: "2"                      # which role (digit 1-5) needs this
    criticality: required | optional
demands_anatomy:
  - region: hip_flexor_complex    # slug stem of a concept-anatomy-* page
    criticality: required | optional
    supports_technique: baseline-drive-on-catch
    for_role: "2"

# Optional structured counters with provenance — gates which bullets are
# safe to surface on user chrome. The body's `## Counters` section remains
# the human-readable view; this YAML mirrors it with Motion-voice rewrites
# and per-bullet extraction labels. Engine surfaces only entries with
# extraction == "llm-inferred".
counters:
  - text: "When the defense switches the pick-and-roll, 5 slips to the rim."
    extraction: llm-inferred       # verbatim | paraphrase | llm-inferred
    source_hint: null              # optional [Sn, p.X] inferred from body
---
```

Note: `team: Lakers | Warriors | etc.` was documented in earlier revisions but
is deprecated and MUST NOT be emitted — team names leak IP and fail the
`check-nba-terms` lint. Use `tags:` for attribution-free categorization.

**Required sections:**

```markdown
# {Play Name}

## Overview
1-2 sentences: what this play achieves, what defense it attacks.

## Formation
Starting positions described in words (e.g., "1 at top of key, 4 and 5 at elbows").

## Phases
### Phase 1: {Phase Label}
- Player movements described step by step
- Key reads and decision points
- What the defense typically does in response

### Phase 2: {Phase Label}
- ...

## Key Coaching Points
- Timing cues
- Spacing principles
- Read progressions

## Counters
What to do when the defense adjusts (e.g., "if they switch, 4 slips to the rim").

## Related Concepts
Required. Link each technique and anatomy region the play demands — these
wikilinks are the human-readable twin of the `demands_techniques` /
`demands_anatomy` YAML front-matter. At minimum one per field entry.

- [[concept-technique-slug]] — technique a specific role needs to execute this play
- [[concept-anatomy-region]] — body system loaded by a role's movement in this play

## Related Plays
- [[play-slug]] — similar action or counter

## Sources
- [S6, p.142]
```

### 4. Source Summary Page

One per source book. Created on first ingest of that source.

```yaml
---
type: source-summary
source_id: S1
pages_ingested: 274
last_updated: 2026-04-11
---
```

**Required sections:**

```markdown
# {Book Title} — Summary

## Overview
2-3 paragraph summary of the book's scope and perspective.

## Key Themes
1. Theme with brief explanation
2. ...

## Chapter Breakdown
- **Ch 1: {Title}** — summary (→ wiki pages: [[page-a]], [[page-b]])
- **Ch 2: {Title}** — summary (→ wiki pages: [[page-c]])
- ...

## Unique Contributions
What does this source add that others don't?

## Notable Quotes
> "Quote" — Author, p.XX
```

## File Naming

- **Kebab-case only**: `pick-and-roll-defense.md`, `3-on-3-shell-drill.md`
- **Descriptive and searchable**: prefer `high-ball-screen-coverage.md` over `hbs.md`
- **Standard abbreviations allowed**: PnR, PG, SG, SF, PF, C, OOB, ATO
- **Source summaries**: `source-{short-name}.md` (e.g., `source-herb-brown-defense.md`)
- **No spaces, no uppercase, no special chars** except hyphens

## Cross-Linking Rules

1. Use `[[page-slug]]` (without `.md` extension) for wiki links
2. Every page MUST link to at least 2 related pages (concepts, drills, or plays)
3. When creating a new page, check the index for existing pages to link to
4. If you reference a concept that doesn't have its own page yet, still link it — the lint operation will flag it as a gap to fill later
5. Bidirectional linking: if A links to B, B should link back to A (update B if it exists)

## Citation Rules

1. Every factual claim MUST cite at least one source
2. Format: `[S1, p.45]` or `[S5, pp.102-108]`
3. Multiple sources: `[S1, p.45; S7, p.201]`
4. When sources disagree, note the disagreement explicitly
5. Never fabricate page numbers — if unsure, cite the source without a page number: `[S1]`

## Ingestion Guidelines

When processing a chunk of PDF content:

1. **Read carefully.** Understand the coaching concepts being taught, not just the words.
2. **Extract actionable knowledge.** Skip filler, acknowledgments, table of contents, bibliography.
3. **One concept per page.** Don't combine unrelated concepts into a single wiki page.
4. **Merge, don't duplicate.** If a concept already exists in the index, update the existing page rather than creating a new one. Add the new source's perspective and citation.
5. **Cross-link aggressively.** Every concept connects to others — offense connects to defense, drills connect to concepts.
6. **Use coaching language.** Write for basketball coaches. Use correct terminology. Include coaching cues.
7. **Preserve specifics.** Player counts, court positions, timing, angles — these details matter.
8. **Flag diagrams.** If the content references a court diagram or figure you can interpret, describe the player positions and movements. If you can't interpret it, note it as `<!-- DIAGRAM: needs visual extraction, p.XX -->`.

## Quality Standards

A good wiki page:
- Can stand alone — a coach reads it and knows what to do
- Cites its sources — every claim is traceable
- Links to related pages — the wiki is a web, not a list
- Uses specific coaching language — "close out high hand, low hand" not "defend the shot"
- Includes common mistakes — coaches learn from what NOT to do
- Has clear progressions — beginner → intermediate → advanced
