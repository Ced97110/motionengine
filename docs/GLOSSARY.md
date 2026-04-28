# Motion Backend Glossary

**Last Updated:** 2026-04-28

Every jargon term a junior would not infer from code. Grouped by domain.

## Structural (Data Model)

**Atom**
One discrete UI building block (plate number, callout, court stamp). Locked vocabulary in design system. Motion's "drafting atoms" mimic architectural blueprint elements. See parent CLAUDE.md.

**Archetype**
One of 8 player position profiles: Sharpshooter, Floor General, Two-Way Wing, Athletic Slasher, Paint Beast, Stretch Big, Playmaking Big, Defensive Anchor. No NBA player names attached (IP rule). Used to filter plays + drills by skill profile. Indexed in frontend play data.

**Concept**
A wiki page (`type: concept`) that teaches a technique, rule, or anatomy region. Examples: `concept-first-step-quickness.md`, `concept-anatomy-hip-flexor-complex.md`. Distinguished from plays and drills.

**Demands_anatomy** (front-matter field)
Array on a `play` page listing body regions the play loads. Example: `{region: "hip_flexor_complex", criticality: "required"}`. Used to link plays → anatomy → drills and to filter plays by injury/readiness. Compiler inverts this into `anatomy-to-play.json`.
**File:** `knowledge-base/wiki/basketball/play-black.md` front-matter section.

**Demands_techniques** (front-matter field)
Array on a `play` page listing technical skills (cuts, screens, passes) the play demands. Example: `{id: "baseline-drive-on-catch", role: "2", criticality: "required"}`. Role is digit "1"-"5" (PG, SG, SF, PF, C). Compiler inverts to `technique-to-play.json`.
**File:** same as above.

**Criticality**
Binary flag on a demand: `required` (play's primary read fails without it) or `optional` (variant or counter path). Compiler filters on `criticality == "required"` for the three canonical queries (Q-A, Q-B, Q-C in spec/crossref-anatomy-chain.md).

**Emphasis** (in trains_* fields)
Binary flag on a drill/technique pairing: `primary` or `secondary`. Used to rank prescription results (primary drills shown first). Less strict than criticality because drills can train multiple skills.

**Frontmatter**
YAML header of a wiki page (lines 1–N before first blank line). Defines type, level, tags, cross-refs, sources. Parser at `wiki_ops/frontmatter.py`.

**Intent**
One of 5 high-level coaching requests: "Game Plan", "Matchup Analysis", "Drill Prescription", "Readiness Report", "Form Coaching". Maps to endpoints (`/api/practice/generate`, `/api/form-coach/analyze`, etc.). (Not fully implemented in backend; documented in parent product spec.)

**Sidecar**
A small JSON file living next to wiki pages. Examples: `technique-aliases.json` (technique-id → concept slug), `play-to-anatomy.json` (inverted index). Compiler creates these from front-matter. No inference, no LLM.

**Sport** (Literal["basketball", "football"])
The sport boundary primitive. Every wiki read, prompt, retrieval operation is sport-aware. Type: `from motion.sports import Sport`. Default: `"basketball"`. Thread via `sport` parameter to `wiki_dir()`, `get_prompts()`, retrieval builders.
**File:** `src/motion/sports.py`.

**Trains_anatomy / Trains_techniques** (front-matter fields)
Arrays on a `drill` page listing body regions and techniques the drill develops. Example: `{region: "glute_max", emphasis: "primary"}`. Mirrors `demands_*` structure. Compiler inverts to `anatomy-to-drill.json` and `technique-to-drill.json`.

**V7Play** (data shape)
The frontend's canonical play shape. Produced by `wiki_importer.py`. Contains phases, actions (arrow/pass/dribble), coordinates, timing. Round-trip invariant tested in `test_wiki_roundtrip.py`: import → write → import must produce the same V7Play.

## Cross-Reference Edges (The Moat)

**Edge #1: Anatomy Chain**
Play → demands_anatomy → concept-anatomy page → trained_by drills. Enables "this play requires ankle mobility, so we're working on ankle stability drills." Fully shipped (spec/crossref-anatomy-chain.md §1).
**Compiler:** `crossref.py`.
**Inverted indexes:** `anatomy-to-play.json`, `anatomy-to-drill.json`.

**Edge #2: Counters**
Play → counters against a defensive look. Prose provenance not yet audited (spec §10 open Q4). Blocked from edge #2 (failure-mode counters). Not yet compiled.

**Edge #4: Defending**
Play ↔ defending page (defensive mirrors). Tag-intersection match (shared tags → likely defensive response). Produces sentence 5 of play brief: "Defending teams often use drop coverage here."
**Compiler:** `crossref.py` (via tag match).
**Inverted indexes:** `play-to-defending.json`.

**Edge #6: Defending Symptoms**
Defending page → `## Common Mistakes` → symptom/remedy pairs. When a defender makes mistake X, they're vulnerable to exploit Y. Engine maps to failure-mode ID tokens, not prose (IP rule).

**Edge #8: Four-Factor Signature**
Play → `produces_signature` (Four-Factor analytic impact). Example: `{factor: "efg-pct", direction: "lifts", magnitude: "medium"}`. Enables "this play lifts effective field goal %" in analytics dashboards.
**Compiler:** `crossref.py`.
**Inverted indexes:** `play-to-signature.json`.

**Produces_signature** (front-matter field)
Array on a `play` page declaring which Four-Factor statistics the play lifts/protects/lowers by design. Example: `{factor: "efg-pct", direction: "lifts", magnitude: "high", rationale: "creates layup looks"}`. Authored by backfill harness or hand. Must be kibitzed from play mechanics, NOT from source book prose (IP rule).

## Wiki Structure & Taxonomy

**Concept-anatomy-***
Prefix convention: `concept-anatomy-{region-slug}.md`. Pages that teach a body region (hip flexors, glutes, core, etc.). Front-matter carries `anatomy_region` field. Examples: `concept-anatomy-hip-flexor-complex.md`, `concept-anatomy-glute-max.md`.
**File location:** `knowledge-base/wiki/basketball/*.md`.

**Concept-technique-***
Prefix convention: `concept-technique-{skill-slug}.md`. Pages that teach a technique (baseline drive, screen setting, defensive positioning, etc.). 9 HIGH-confidence aliases to existing `concept-*` pages; 8 NEW pages authored as structured concept-technique pages. Alias mapping at `technique-aliases.json`.

**Defending-***
Prefix convention: `defending-{defensive-look}.md`. Pages that teach defensive responses (drop coverage, ice, blitz, zone rotations, etc.). Linked to plays via tag intersection + edge #4 graph.
**File location:** `knowledge-base/wiki/basketball/*.md`.

**Drill-*** / **Exercise-***
Practice activities. Drill pages carry `trains_anatomy` and `trains_techniques` front-matter for cross-ref compilation. 750+ pages, ~100 with structured diagram JSON.
**File location:** `knowledge-base/wiki/basketball/*.md`.

**Play-***
68 shipped plays (as of 2026-04-26). Front-matter carries `demands_anatomy`, `demands_techniques`, `produces_signature`. Body carries `## Phases` (prose narrative), `## Counters` (defensive responses), diagram blocks with JSON.
**File location:** `knowledge-base/wiki/basketball/play-*.md`.

**Source-***
Source-summary pages (one per ingested PDF). Metadata only: chapter breakdown, page counts, key themes. Not retrieval payloads.
**File location:** `knowledge-base/wiki/basketball/source-*.md`.

**Wikilink** / **Wikilink-graph**
Markdown links like `[[concept-anatomy-hip-flexor-complex]]` embedded in page bodies. SCHEMA.md §Cross-Linking requires ≥2 related pages with bidirectional links. Compiler lints this. Graph of all wikilinks is queryable (6,346 native pairs as of 2026-04-21).

**Citation-graph**
Network of pages that cite the same source (e.g., 5 pages cite `[S2, p.18]`). Used to find related content. No explicit front-matter; inferred from `[Sn, p.X]` citation footers in page bodies.

**Formation-graph**
Plays grouped by `formation` front-matter field (5-out, 4-1, pick-and-roll, etc.). Used for play-set filtering and play siblings.

## Pipeline & Ingestion

**Batch API** (ingest from new PDF)
Remote Claude-as-a-service. Sends raw PDF chapter → receives structured YAML (concept + drill pages). 50% API cost vs standalone runs. Entry point: `pipeline/03_generate_concepts.py`.

**Compiled directory**
Output of the compiler. Path: `knowledge-base/wiki/{sport}/compiled/`. Contains 6 inverted indexes (JSON) + `technique-aliases.json`. Loaded at startup by `cached_indexes()`.

**Ingest pipeline** (python -m motion.wiki_ops.ingest)
Batch ingestion of raw PDFs into wiki markdown. Steps: download → parse → chunk → generate-concepts (via batch API) → generate-drills → generate-plays → commit. Dangerous operation — always audits before commit.
**File:** `pipeline/01_download_dataset.py` through `pipeline/11_test_ml.py`.

**Alembic migration**
Database schema version control. Migrations are additive (never destructive). New table → new migration file in `alembic/versions/`. Run via `uv run alembic upgrade head` at boot.
**Gotcha:** Don't use `text(...)` constraints in autogen (breaks alembic). Use explicit column names.

**RUN_LIVE_EVAL** (environment variable)
When set, pytest runs against live Claude API calls (not stubs). Used to validate eval baseline after prompt changes. Example: `RUN_LIVE_EVAL=1 uv run pytest tests/eval/`. Cost: ~$1-3 per run.

## Brief Composers & Modes

**Stub mode**
Deterministic fallback when `ANTHROPIC_API_KEY` is not set or Claude call fails. Builds brief from bundle metadata (anatomy names, drill slugs, defending tags). UX never dead-ends.
**File:** `src/motion/services/play_brief.py:_build_stub()`.

**Claude mode**
LLM composition via Claude Sonnet 4.6. Takes PlayContext (Layer 3 bundle) + prompt template (with byte-identity constraints) → returns structured brief + citations.
**File:** `src/motion/services/play_brief.py:_build_claude_prompt()`.

**Byte-identity test**
Each prompt string is hand-pinned + test-guarded. Any wording change requires updating the golden in `tests/eval/test_prompt_byte_identity.py` in the same commit. Prevents silent prompt drift that corrupts eval baselines.
**File:** `tests/eval/test_prompt_byte_identity.py`.

**Source citation token** ([Sn, p.XX])
Developer-only footer marking source page. Example: `[S2, p.18]` (source 2 = Basketball Anatomy, page 18). Never surfaced to users (IP rule). Embedded in brief composer output at the JSON level; routers strip citations before user response.

**Fewshot**
Example play (hand-chosen for diversity) included in prompt so Claude learns the style. For backfill_crossref: `play-black.md` is the fewshot for demands_* annotation.
**File:** `src/motion/wiki_ops/backfill_crossref.py:_PLAY_SYSTEM_PROMPT`.

## Form Coach (MediaPipe Integration)

**Keyframe**
A single video frame from the coach's phone video, with pose landmarks detected by MediaPipe. Processed in-browser via `@mediapipe/tasks-vision`.

**FormMeasurement**
One skeleton measurement (e.g., knee-angle, elbow-height). Computed from pose landmarks. Used to detect form flaws (knees caving, elbow drifting, etc.).
**File:** `src/motion/wiki_ops/retrieval_models.py:FormMeasurement`.

**FormContext**
Bundle of measurements + sport context passed to form_brief composer. Result: 2-3 sentence correction on-camera.
**File:** `src/motion/wiki_ops/retrieval_models.py:FormContext`.

**MediaPipe pose landmarker**
Google's skeletal pose estimation model. Runs in-browser. Detects 33 body landmarks (head, shoulders, hips, knees, ankles, wrists, etc.). Latency ~100ms per frame on modern phones.

**Flagged signal**
A measurement that exceeds a threshold (e.g., knee-angle < 90 degrees on landing = knees caving). Engine maps to anatomy region + trains suggested drills.

**Threshold**
Numeric boundary. Example: `knee_valgus_angle > 20 degrees` = flagged. Hard-coded in form-coach logic. Not coach-configurable (yet).

## Practice Generator

**PracticeContext**
Bundle of coach inputs (level, duration, focus areas, sport) + retrieved drills + filtered by anatomy/technique demands. Input to practice_brief composer.
**File:** `src/motion/wiki_ops/retrieval_models.py:PracticeContext`.

**Candidate drill**
One drill that matches level + duration + focus area filters. Ranked by emphasis (primary first). Subset passed to composer for prose + timing.

**Focus area**
Coach-selected skill emphasis: "shooting", "ball-handling", "finishing", "defense", "conditioning", "scrimmage", "free-throws", "rebounding". Maps to drill tags for filtering.
**File:** `routers/practice.py:_VALID_FOCUS`.

**Level** (beginner / intermediate / advanced)
Drill difficulty tier. Coach-selected. Filters drill candidates to avoid mismatches. No mixed-level drills in one practice (today).

**Block** (practice unit)
One 5-15 min segment of the practice plan. Contains drills, timing (start_ms, duration_ms), anatomy chips (visual tags showing trained regions), phase (warmup, skill, competitive, cooldown).
**File:** `schemas/knowledge.py:PracticeBlockOut`.

## Sport & IP / Voice

**Sport literal** (Literal["basketball", "football"])
Type-safe enum. Every code path that reads wiki or produces prose must accept `sport: Sport` parameter and dispatch accordingly. Adding a third sport = one new line in `motion/sports.py` + one new prompt module.

**Sport boundary**
Architecture pattern: no module hardcodes "basketball". All wiki reads go through `wiki_dir(sport=...)`. All prompts go through `get_prompts(sport)`. Enables multi-sport portability.

**Default sport** (DEFAULT_SPORT = "basketball")
Fallback when no sport is specified (legacy code, partial deployments). Backward-compatible.

**Banned vocabulary**
User-facing surfaces never contain: unlock, level up, game-changer, revolutionary, supercharge, empower, journey, unleash, seamless, insights (as noun), AI-powered, next-generation, reimagine, dominate, crush, grind, hustle. No emoji. No exclamation marks. No rhetorical questions.
**Enforced by:** voice tests + parent CLAUDE.md.

**IP rule** (Structural metadata OK, book prose NOT)
Book titles, page counts, author names never surface to users. Structural metadata (play slugs, anatomy regions, drill names, technique tags, formation names) IS surfaced. Coaching prose (principles, cues, error symptoms) is NOT quoted or paraphrased on user surfaces — the Engine composes its own voice.
**Enforced by:** brief prompts (hardcoded "do not quote"), voice fixtures, `frontend/scripts/check-nba-terms.ts`.

**Structural metadata**
Derived from books but not book-specific: slugs (play-black, concept-anatomy-hip-flexor-complex), formation names, region names, drill tags, technique IDs. Safe to surface.

**Book prose**
Anything authored by the source book: coaching cues, principles text, common-mistake descriptions, drill objectives copied from source. Forbidden on user surfaces per IP rule. Lives in compiled `insights:` fields for internal retrieval only.

**Citation token** ([Sn, p.XX] format)
Developer-only notation. `S` = source ID (1-9), `n` = page number. Example: `[S2, p.18]`. Appears in routers' JSON output at the field level but is stripped before returning to user.

**Anonymized stats**
Player data and game stats are either fully anonymized (no names, team, date) or omitted. GDPR as global baseline. Under-16 players require parental consent.

## Testing & Eval

**Eval fixture** (.jsonl file)
One test case: inputs, expected outputs, forbidden outputs, notes. Format: JSON line per fixture. 30 fixtures total across play-brief (20), practice (5), form-coach (5).
**File location:** `eval/` directory at repo root.

**Precision@5 / Recall@all**
Scoring metrics for drill prescription eval. Precision@5: of the top 5 prescribed drills, how many match expected? Recall: total expected drills retrieved (regardless of rank).

**Forbidden-phrase blocklist**
Regex patterns that should NEVER appear in brief output. Catches IP leakage (coach names, book titles), banned vocab, clinical jargon. Example: `\b(Shaq|Olajuwon|Lakers)\b` (NBA-specific names).
**File:** `tests/eval/_scoring.py`.

**Slug-form normalization**
Brief must emit slugs that match `[a-z0-9-]+` (lowercase, hyphens, no spaces). Engine must not output `Play Black` or `play_black` — only `play-black`.

**Prompt byte-identity test**
Test guards exact prompt wording. Any change to a prompt string breaks the test → must update the golden in the same commit. Prevents silent prompt drift between commits.
**File:** `tests/eval/test_prompt_byte_identity.py`.

## Field Abbreviations & Shorthand

| Term | Meaning |
|---|---|
| `v7_a`, `v7_b` | V7Play before and after round-trip (import → write → import) |
| `md0`, `md1` | Markdown source before and after transformation |
| `PG`, `SG`, `SF`, `PF`, `C` | Positions: Point Guard, Shooting Guard, Small Forward, Power Forward, Center |
| `LRU` | Least Recently Used cache (Python functools.lru_cache) |
| `O(1)` | Constant-time lookup (via index inversion) |
| `[Sn, p.X]` | Citation footer: Source n, page X |
| `YAGNI` | "You Aren't Gonna Need It" — don't implement unused features |
