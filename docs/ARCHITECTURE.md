# Motion Backend Architecture

**Last Updated:** 2026-04-28

The Motion backend is a 5-layer system that takes coaching knowledge (wiki markdown), compiles it into queryable indexes, and surfaces it to coaches via AI-composed briefs. This document describes each layer with concrete file paths and data flow.

## The 5 Layers

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Layer 0: Source Material                                               │
│ Raw PDFs (S1-S9: coaching books) → knowledge-base/raw/ (gitignored)    │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ Layer 1: Wiki Markdown (Karpathy Pattern)                             │
│ knowledge-base/wiki/{sport}/*.md — Human-readable source of truth      │
│ - play-*.md (68 pages)                                                 │
│ - drill-*.md / exercise-*.md (750+ pages)                             │
│ - concept-*.md (anatomy, techniques, rules)                           │
│ - defending-*.md, source-*.md                                         │
│ Front-matter: type, tags, demands_anatomy, demands_techniques, etc.   │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ Layer 2: Compiler (wiki_ops/)                                          │
│ Reads Layer 1 → produces compiled sidecars at wiki/compiled/{sport}/  │
│ - lint_wiki.py: validates front-matter + cross-links, enforces schema │
│ - crossref.py: inverts play→technique + play→anatomy to produce:     │
│   • play-to-anatomy.json                                              │
│   • play-to-technique.json                                            │
│   • anatomy-to-play.json (inverted)                                   │
│   • anatomy-to-drill.json (inverted)                                  │
│   • technique-to-drill.json (inverted)                                │
│ - frontmatter.py: parses YAML front-matter from .md files             │
│ - paths.py: wiki_dir(sport=...) resolves per-sport paths             │
│ - ingest.py: batch ingestion from raw PDFs (for new sources)          │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ Layer 3: Retrieval (wiki_ops/retrieval.py + retrieval_models.py)      │
│ Pure functions that join compiled indexes + wiki insights → bundles   │
│ - load_indexes(sport=...) loads all 6 JSON files + technique-aliases  │
│ - build_play_context(slug, indexes) → PlayContext (anatomy + drills)  │
│ - build_practice_context(level, duration, focus_areas, indexes)       │
│   → PracticeContext                                                   │
│ - build_drill_justification(slug, indexes) → which plays it prepares  │
│ - build_form_context(shot_type, measurements, indexes) → FormContext  │
│ - cached_indexes() — module-level lru_cache loader (default sport)    │
│ No LLM, no HTTP. Dataclass results (frozen for immutability).         │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ Layer 4: Composers (services/)                                         │
│ LLM (Claude Sonnet 4.6) takes Layer 3 bundle → returns brief + cites  │
│ - play_brief.py: 3-sentence coaching brief for a play                │
│   Input: PlayContext (Layer 3 bundle)                                 │
│   Output: BriefResult (brief text + source citations + "claude"|"stub")│
│   Two modes: Claude (API) or Stub (deterministic fallback)            │
│ - practice_brief.py: 5-7 block practice plan                         │
│   Input: PracticeContext (Layer 3 bundle)                            │
│   Output: PracticeResponse (blocks w/ drills + timing + anatomy chips)│
│ - form_brief.py: shot-form coaching, MediaPipe-grounded              │
│   Input: FormContext (pose landmarks + sport)                         │
│   Output: 2-3 sentence correction on camera                          │
│ Prompts: motion/prompts/{basketball,football}.py (sport-switched)    │
│ Byte-identity testing: tests/eval/test_prompt_byte_identity.py       │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ Layer 5: Routers (routers/) + Test Surface                            │
│ HTTP endpoints that wire Layer 3 + 4 together                         │
│ - /api/practice/generate: POST PracticeRequest → practice plan        │
│ - /api/form-coach/analyze: POST FormRequest → form brief             │
│ - /knowledge/ask: POST query → PlayContext (stub for future LLM Q&A) │
│ - /api/playlab/*: wiki importer endpoints                            │
│ - Sport middleware (middleware/sport.py): adds X-Motion-Sport header  │
│   to all requests, threads sport through retrieval → composers       │
│ Test surface: eval/*.jsonl (30 fixtures), tests/unit/*, tests/eval/* │
│   eval fixtures grade the stub + Claude outputs on quality gates     │
│   byte-identity test guards prompt wording from silent drift         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Worked Example: play-black.md → Play Brief

**Input:** Coach clicks "View Brief" for `play-black.md` at `/api/knowledge/plays/black`

**Step 1: Router (routers/knowledge.py)**
```python
GET /api/knowledge/plays/black
├─ current_sport(request) → "basketball" (from X-Motion-Sport header or default)
├─ build_play_context("black", sport="basketball")
```

**Step 2: Retrieval (wiki_ops/retrieval.py)**
```python
build_play_context("black", sport="basketball")
├─ load_indexes(sport="basketball")  # load wiki/basketball/compiled/*.json
├─ read wiki/basketball/play-black.md frontmatter
├─ demands_anatomy: [
│     {region: "hip_flexor_complex", criticality: "required"},
│     {region: "glute_max", criticality: "required"},
│   ]
├─ demands_techniques: [
│     {id: "baseline-drive-on-catch", role: "2", criticality: "required"},
│     {id: "step-up-screen-set", role: "4", criticality: "required"},
│   ]
├─ Q-A query: anatomy-to-drill.json → drill prescriptions
│   hip_flexor_complex → ["drill-band-lateral-walk", "exercise-hip-thrust"]
├─ Q-B query: play-to-defending.json → defensive mirrors
│   shared tags match → [defending-drop-coverage]
├─ Q-C query: play-to-signature.json → four-factor signature
│   produces_signature: [{factor: "efg-pct", direction: "lifts"}]
└─ Return frozen PlayContext dataclass (immutable)
   {
     play_slug: "black",
     anatomy: [AnatomyDemand(...)],
     drills: [DrillPrescription(...)],
     defending: [DefendingEdge(...)],
     signature: [SignatureEntry(...)],
   }
```

**Step 3: Composer (services/play_brief.py)**
```python
build_brief(context, readiness=None, sport="basketball")
├─ if ANTHROPIC_API_KEY is set:
│  └─ _build_claude_prompt(context) assembles the prompt template
│     from motion/prompts/basketball.py (sport-switched)
│  └─ Claude Sonnet 4.6 call with byte-identity constraints
│  └─ Parse response → extract citations [S2, p.18] + [S4, p.56]
│  └─ Return BriefResult(brief="...", source_citations=[...], source="claude")
└─ else:
   └─ _build_stub(context) deterministically builds fallback
      "This play requires hip flexors and glutes. Primary drill: band lateral walk."
      Return BriefResult(..., source="stub")
```

**Step 4: Response (routers/knowledge.py)**
```json
{
  "brief": "Black uses baseline drive timing to create a secondary playmaker read...",
  "source_citations": ["[S4, p.56]", "[S2, p.18]"],
  "source": "claude",
  "anatomy": [...],
  "drills": [...]
}
```

## Key Module Responsibilities

### Layer 1: Wiki Source
- **File:** `knowledge-base/wiki/{basketball,football}/*.md`
- **Owners:** Coaches + AI agents during ingest
- **What's inside:** Narrative prose + front-matter + `[[wikilinks]]` for cross-ref visibility
- **Schema:** `knowledge-base/SCHEMA-core.md` (the constitution)

### Layer 2: Compiler
- **File:** `src/motion/wiki_ops/lint_wiki.py`, `crossref.py`, `frontmatter.py`, `paths.py`
- **Entry:** `python -m motion.wiki_ops.cli crossref --sport basketball` (not yet wired to CI; lint via `wiki-lint` script)
- **Output:** `knowledge-base/wiki/{sport}/compiled/*.json` + linting errors
- **What it validates:**
  - Front-matter schema (type, demands_*, trains_*, etc.)
  - All `concept-anatomy-*`, `concept-technique-*` slugs resolve
  - Cross-links are bidirectional (lint rule `_check_bidirectional`)
  - No duplicate wikilinks per page
  - Anatomy regions exist in the canonical vocabulary (27 regions, hardcoded in spec)

### Layer 3: Retrieval
- **File:** `src/motion/wiki_ops/retrieval.py` (1100+ lines, pure functions + dataclasses)
- **Load time:** `load_indexes()` lru-cached per sport — ~100ms cold start
- **Memory:** All 6 JSON files in RAM (~10 MB per sport)
- **Threadsafe:** Yes (immutable dataclasses, no mutable module state)
- **Consumers:** play_brief, practice_brief, form_brief, routers/knowledge.py

### Layer 4: Composers
- **Files:** `src/motion/services/{play,practice,form}_brief.py`
- **API:** Pure functions `build_*_brief(context, sport=..., [optional])` → frozen dataclass
- **Cost:** ~$0.01-0.05 per call (Claude Sonnet 4.6)
- **Fallback:** Stub mode (deterministic, no API key needed)
- **Prompts:** `src/motion/prompts/{basketball,football}.py` (per-sport preludes)
- **Byte-identity:** Every prompt string is hand-pinned + test-guarded (tests/eval/test_prompt_byte_identity.py)

### Layer 5: Routers + Tests
- **Files:** `src/motion/routers/{practice,form_coach,knowledge,playlab}.py`
- **Entry:** FastAPI app at `src/motion/main.py`
- **Middleware:** `SportMiddleware` threads `X-Motion-Sport` header through all requests
- **Tests:** 
  - Unit: `tests/unit/test_*.py` (syntax, schema, edge cases)
  - Integration: `tests/integration/test_*.py` (router behavior, mock API calls)
  - Eval: `tests/eval/test_*.jsonl` + `tests/eval/test_*.py` (quality gates on output)

## Sport Boundary (Critical Design)

Every module that reads wiki data must accept a `sport: Sport` parameter and pass it to `wiki_dir(sport=...)`. This pattern makes adding football or a third sport a one-line change in `motion/sports.py` and per-sport yaml in prompts.

Example: `build_play_context("black", sport="basketball")` reads from `knowledge-base/wiki/basketball/play-black.md`, not `knowledge-base/wiki/play-black.md`.

If a module doesn't accept sport, it defaults to `DEFAULT_SPORT = "basketball"`. Legacy code paths that predate the sport boundary work without change.

## Eval & Quality Gates

**The eval is the spec.** If a brief prompt changes, eval fixtures must be re-run (`RUN_LIVE_EVAL=1 uv run pytest tests/eval/`) and the golden updated in the same commit. No silent baseline drift allowed.

Three eval test categories:

1. **Byte-identity** (`test_prompt_byte_identity.py`) — parametrizes over defending × signature × readiness × cross-ref counts. Asserts the basketball prompt is byte-identical to hand-pinned golden. Failed on prompt wording change → must update both prompt + golden.

2. **Fidelity** (`test_play_brief_eval.py`, `test_practice_eval.py`) — 30 fixtures covering play-brief, practice, form-coach. Scores Claude output against forbidden-phrase blocklist + slug-form validation + anatomical correctness.

3. **Unit** (`tests/unit/test_wiki_roundtrip.py`) — round-trip invariant: import → write → import produces the same V7Play. Catches importer/writer drift before it corrupts the wiki.

## Common Paths

| What | Where |
|---|---|
| FastAPI app entry | `src/motion/main.py` |
| Router definitions | `src/motion/routers/*.py` |
| Service composers | `src/motion/services/*.py` |
| Sport boundary | `src/motion/sports.py` |
| Sport middleware | `src/motion/middleware/sport.py` |
| Retrieval logic | `src/motion/wiki_ops/retrieval.py` |
| Retrieval models | `src/motion/wiki_ops/retrieval_models.py` |
| Wiki compiler | `src/motion/wiki_ops/lint_wiki.py`, `crossref.py` |
| Wiki frontmatter parser | `src/motion/wiki_ops/frontmatter.py` |
| Path resolution | `src/motion/wiki_ops/paths.py` |
| Prompts (basketball) | `src/motion/prompts/basketball.py` |
| Prompts (football) | `src/motion/prompts/football.py` |
| Prompt registry | `src/motion/prompts/registry.py` |
| Wiki source | `knowledge-base/wiki/{basketball,football}/*.md` |
| Compiled indexes | `knowledge-base/wiki/{sport}/compiled/*.json` |
| Schema (constitution) | `knowledge-base/SCHEMA-core.md` |
| Tests | `tests/{unit,integration,eval}/*` |
| Eval fixtures | `eval/*.jsonl` |
