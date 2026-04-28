# Cookbook: Common Tasks

**Last Updated:** 2026-04-28

Five recipes for your first PR. Each follows the same template: ordered file list → gate that fails → verification command.

## Recipe 1: Add a New Play

**Goal:** Author a new `play-*.md` page and make it queryable end-to-end.

**Files to touch (in order):**
1. `knowledge-base/wiki/basketball/play-{slug}.md` — new file
2. `knowledge-base/wiki/basketball/compiled/*.json` — updated by compiler
3. `tests/unit/test_wiki_roundtrip.py` — auto-included (enumerate_play_slugs scans filesystem)

**Step-by-step:**

### 1. Create play markdown file

**File:** `knowledge-base/wiki/basketball/play-black.md` (example, use different slug)

```markdown
---
type: play
category: offense
formation: 5-out
tags: [man-to-man, baseline-drive, step-up-screen, quick-hitter]
source_count: 1
last_updated: 2026-04-28
demands_techniques:
  - id: baseline-drive-on-catch
    role: "2"
    criticality: required
  - id: step-up-screen-set
    role: "4"
    criticality: required
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
  - region: glute_max
    criticality: required
  - region: ankle_complex
    criticality: optional
produces_signature:
  - factor: efg-pct
    direction: lifts
    magnitude: medium
    rationale: "creates baseline drive to layup or kickout"
---

# Black

## Summary
Two-sentence overview of what the play accomplishes.
Emphasize the primary read, not the counter.

## Overview
(One paragraph: initial formation, ball position, trigger.)

## Phases

### Phase 1
[Prose narrating role 1's movement, reading]

### Phase 2
[Prose narrating role 2's movement, role 3's positioning, etc.]

### Phase 3
[Continuation if phases are sequential]

## Counters
- If defense X happens, then Y is the secondary read.
- If defender overplays baseline, role 3 is open mid-range.

## Related Concepts
[[concept-anatomy-hip-flexor-complex]] — required for baseline-drive-on-catch (role 2)
[[concept-anatomy-glute-max]] — required for explosive first step
[[drill-band-lateral-walk]] — prepares hip mobility for cuts
[[defending-drop-coverage]] — likely defensive response

## Sources
[S4, pp.56-58] — primary description
[S3, pp.102-105] — alternative positioning
```

**Key requirements:**
- Slug format: `play-[a-z0-9][a-z0-9-]*` (lowercase, hyphens only)
- No NBA team/player names in slug or body (IP rule)
- Front-matter must have `type: play` and `formation` field
- At least one source citation `[Sn, p.X]` in body
- All `demands_anatomy` regions must exist in canonical vocabulary (27 regions defined in spec/crossref-anatomy-chain.md §3.1)
- All `demands_techniques` ids must resolve to `concept-technique-*.md` pages (or be allowed for later authoring)
- Wikilinks in body must be bidirectional (SCHEMA.md §Cross-Linking)

### 2. Run lint

```bash
cd /Users/ced/Desktop/motion/backend
uv run wiki-lint --sport basketball
```

**What it checks:**
- Front-matter schema (type, formation, demands_anatomy fields)
- All `demands_anatomy[].region` exist in canonical list
- All `demands_techniques[].id` resolve (warns if not found)
- All wikilinks `[[*]]` have matching back-links
- No duplicate regions in demands_anatomy
- Slug format `play-*` matches pattern

**Common lint failures:**
- `region: hiip_flexor_complex` (typo) → "unknown region"
- `demands_techniques[].id: flex-cut` but no `concept-technique-flex-cut.md` → warning
- `[[concept-anatomy-hip-flexor-complex]]` in body but no front-matter link → warning

**Fix:** Correct the issue, re-run lint until green.

### 3. Run compiler

```bash
cd /Users/ced/Desktop/motion/backend
uv run python -m motion.wiki_ops.cli crossref --sport basketball
```

**What it does:**
- Reads all `play-*.md` front-matter
- Inverts `demands_anatomy` → `anatomy-to-play.json`
- Inverts `demands_techniques` → `technique-to-play.json`
- Inverts `trains_anatomy` from drills → `anatomy-to-drill.json`
- Writes all 6 JSON files to `knowledge-base/wiki/basketball/compiled/`

**Verify output:**
```bash
grep "play-black" /Users/ced/Desktop/motion/backend/knowledge-base/wiki/basketball/compiled/play-to-anatomy.json
```

Should show your play with anatomy regions.

### 4. Test round-trip invariant

```bash
cd /Users/ced/Desktop/motion/backend
uv run pytest tests/unit/test_wiki_roundtrip.py::test_roundtrip[play-black] -v
```

**What it checks:**
- Import wiki page → V7Play `v7_a`
- Write V7Play to markdown `md1`
- Import markdown again → V7Play `v7_b`
- Assert `v7_a == v7_b` (semantic identity)

**Common failure:** Duplicate `### Phase 1` headers in body → importer binds phase by number, not position → ambiguous. Rename to `### Phase 1a`, `### Phase 1b` if you have parallel options.

### 5. Test retrieval end-to-end

```bash
cd /Users/ced/Desktop/motion/backend
python3 << 'EOF'
from motion.wiki_ops.retrieval import build_play_context

context = build_play_context("black", sport="basketball")
print(f"Play: {context.play_slug}")
print(f"Anatomy demands: {[a.region for a in context.anatomy]}")
print(f"Drills prescribed: {[d.drill_slug for d in context.drills]}")
EOF
```

**Expected output:**
```
Play: black
Anatomy demands: ['hip_flexor_complex', 'glute_max', 'ankle_complex']
Drills prescribed: ['drill-band-lateral-walk', 'exercise-hip-thrust', ...]
```

**Gate that catches mistakes:**
- Missing `demands_anatomy` field → empty anatomy list (should have >0)
- Missing drill pages for trained regions → empty drills list
- Typo in region name → "unknown region" at compile time

---

## Recipe 2: Add a New Drill

**Goal:** Author a drill page and link it to anatomy/techniques.

**Files to touch (in order):**
1. `knowledge-base/wiki/basketball/drill-{slug}.md` — new file
2. `knowledge-base/wiki/basketball/compiled/*.json` — updated by compiler
3. `tests/unit/test_wiki_roundtrip.py` — tests integration (optional for drills, but run if you're adding complex diagram)

**Step-by-step:**

### 1. Create drill markdown

**File:** `knowledge-base/wiki/basketball/drill-band-lateral-walk.md`

```markdown
---
type: drill
level: intermediate
positions: [PG, SG, SF, PF, C]
players_needed: 1
duration_minutes: 8-10
tags: [conditioning, lateral-movement, lower-body-strength]
source_count: 1
last_updated: 2026-04-28
trains_anatomy:
  - region: glute_med
    emphasis: primary
  - region: hip_flexor_complex
    emphasis: primary
trains_techniques:
  - id: lateral-shuffle-recovery
    emphasis: primary
---

# Band Lateral Walk

## Objective
Build lateral stability and glute-medius activation for defensive footwork.

## Setup
- Resistance band looped around legs just above knees
- Player standing, slight knee bend, hands on hips
- Half court or open space

## Execution
1. Step laterally 8-10 steps, maintaining constant tension on band
2. Keep chest up, knees bent, hips level
3. Return walking backward (controlled tension, no slack)
4. Repeat 3 sets of 10 steps each direction

## Coaching Points
- Band tension should resist motion — player fights against it
- Knees stay level (don't drop one side)
- No internal/external knee rotation — move from hips
- Glute activation should be felt on the working side

## Progressions
- Add hand/arm movement (simulate defensive closeout)
- Increase band resistance
- Increase speed (march→walk→quick-step)

## Depressions
- Remove band (bodyweight only)
- Shallow knee bend (easier range)

## Related Concepts
[[concept-anatomy-glute-med]] — target region for this drill
[[concept-technique-lateral-shuffle-recovery]] — skill trained
[[play-black]] — this drill prepares role 5's lateral movement
[[exercise-glute-activation]] — progression or related exercise

## Sources
[S2, pp.18-19] — glute-medius activation protocols
[S8, pp.45-48] — lateral training progression
```

**Key requirements:**
- Type: `drill` (or `exercise`)
- Level: `beginner`, `intermediate`, or `advanced`
- Positions: relevant roles (can be all 5 if universal)
- Duration: realistic range (5-30 min typical)
- At least one `[Sn, p.X]` citation
- `trains_anatomy` and `trains_techniques` should reference real pages

### 2. Run lint + compile

```bash
uv run wiki-lint --sport basketball
uv run python -m motion.wiki_ops.cli crossref --sport basketball
```

### 3. Verify anatomy-to-drill inversion

```bash
grep "glute_med" /Users/ced/Desktop/motion/backend/knowledge-base/wiki/basketball/compiled/anatomy-to-drill.json
# Should show: "drill": "drill-band-lateral-walk"
```

### 4. Test integration (optional, if diagram added)

If you added a `json name=diagram-positions` block to the drill:
```bash
uv run pytest tests/unit/test_wiki_roundtrip.py -k drill -v
```

---

## Recipe 3: Add a New Endpoint

**Goal:** Create a new HTTP endpoint that threads sport through layers 3 + 4.

**Files to touch (in order):**
1. `src/motion/schemas/knowledge.py` — request/response Pydantic models
2. `src/motion/routers/knowledge.py` (or new `routers/new_feature.py`) — endpoint definition
3. `src/motion/main.py` — register router (if new file)
4. `tests/integration/test_knowledge_router.py` — integration test

**Step-by-step:**

### 1. Define request/response schemas

**File:** `src/motion/schemas/knowledge.py`

```python
from pydantic import BaseModel, Field

class MyFeatureRequest(BaseModel):
    """Input to the new endpoint."""
    play_slug: str = Field(..., pattern=r"^play-[a-z0-9-]+$")
    readiness: list[dict] | None = Field(None, description="optional roster context")

class MyFeatureResponse(BaseModel):
    """Output from the new endpoint."""
    summary: str
    recommendations: list[str]
    source: str  # "claude" | "stub"
```

### 2. Define endpoint

**File:** `src/motion/routers/knowledge.py` (append to existing router or create new file)

```python
from fastapi import APIRouter, Request
from motion.middleware.sport import current_sport
from motion.schemas.knowledge import MyFeatureRequest, MyFeatureResponse
from motion.wiki_ops.retrieval import build_play_context, cached_indexes
from motion.services.play_brief import build_brief

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])

@router.post("/my-feature")
async def my_feature(
    request: Request,
    body: MyFeatureRequest,
) -> MyFeatureResponse:
    """Endpoint description for OpenAPI."""
    # Step 1: Resolve sport
    sport = current_sport(request)

    # Step 2: Build context (Layer 3) — pass the shared index cache
    context = build_play_context(body.play_slug, cached_indexes())

    # Step 3: Compose brief (Layer 4)
    brief = build_brief(context, readiness=body.readiness, sport=sport)
    
    # Step 4: Transform response
    return MyFeatureResponse(
        summary=brief.brief,
        recommendations=[d.drill_slug for d in context.drills[:3]],
        source=brief.source,
    )
```

**Key patterns:**
- Always extract `sport = current_sport(request)` first
- Pass `sport` to all Layer 3 builders
- Pass `sport` to all Layer 4 composers
- Return frozen dataclass (Pydantic model)
- Validate inputs early (Pydantic does this automatically)

### 3. Register router (if new file)

**File:** `src/motion/main.py`

```python
from motion.routers.my_feature import router as my_feature_router

def create_app() -> FastAPI:
    # ...
    app.include_router(my_feature_router)
    # ...
```

### 4. Test integration

**File:** `tests/integration/test_knowledge_router.py`

```python
import pytest
from fastapi.testclient import TestClient
from motion.main import create_app

@pytest.fixture
def client():
    return TestClient(create_app())

def test_my_feature_success(client):
    response = client.post(
        "/api/knowledge/my-feature",
        headers={"x-motion-sport": "basketball"},
        json={"play_slug": "play-black", "readiness": None},
    )
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "recommendations" in data
    assert "source" in data

def test_my_feature_invalid_sport(client):
    response = client.post(
        "/api/knowledge/my-feature",
        headers={"x-motion-sport": "cricket"},  # Invalid
        json={"play_slug": "play-black"},
    )
    assert response.status_code == 400
```

### 5. Test end-to-end smoke test

```bash
PORT=8080 uv run motion-api &
sleep 2
curl -X POST http://localhost:8080/api/knowledge/my-feature \
  -H "X-Motion-Sport: basketball" \
  -H "Content-Type: application/json" \
  -d '{"play_slug":"play-black"}'
```

**Gate that catches mistakes:**
- Missing `sport` parameter to Layer 3 builder → wrong wiki directory loaded
- Missing endpoint from router registration → 404
- Pydantic validation error → 422 (request validation failed)

---

## Recipe 4: Modify a Prompt

**Goal:** Change a brief prompt and keep the baseline stable.

**Files to touch (in order):**
1. `src/motion/services/play_brief.py` (or `practice_brief.py`, `form_brief.py`) — modify `_PLAY_SYSTEM_MESSAGE` (or equivalent)
2. `src/motion/prompts/basketball.py` (or `football.py`) — modify `PLAY_PRELUDE` if sport-specific
3. `tests/eval/test_prompt_byte_identity.py` — update golden
4. Run eval (local or CI)

**Step-by-step:**

### 1. Modify prompt

**File:** `src/motion/services/play_brief.py`

```python
_PLAY_SYSTEM_MESSAGE = """You are composing a coaching brief for a basketball play.

Input: a play's structure (phases, anatomy demands, defending mirrors, four-factor signature)

Output: a 3-sentence brief in Motion's voice. Format:

- Sentence 1: play's primary objective + key anatomy region
- Sentence 2: defending response (if any) or tactical note
- Sentence 3: drill prescription or readiness implication

Rules:
- NEVER quote or paraphrase source books
- Speak basketball, not anatomy jargon
- Avoid promotional language (unlock, revolutionize, etc.)
- Include exactly one citation [Sn, p.X] if available
"""
```

### 2. Update golden in test

**File:** `tests/eval/test_prompt_byte_identity.py`

Find the golden for basketball play-brief:

```python
_BASKETBALL_PLAY_BRIEF_GOLDEN = """You are composing a coaching brief for a basketball play.

Input: a play's structure (phases, anatomy demands, defending mirrors, four-factor signature)

Output: a 3-sentence brief in Motion's voice. Format:

- Sentence 1: play's primary objective + key anatomy region
- Sentence 2: defending response (if any) or tactical note
- Sentence 3: drill prescription or readiness implication

Rules:
- NEVER quote or paraphrase source books
- Speak basketball, not anatomy jargon
- Avoid promotional language (unlock, revolutionize, etc.)
- Include exactly one citation [Sn, p.X] if available
"""
```

Ensure it matches EXACTLY (byte-for-byte).

### 3. Run byte-identity test (local)

```bash
cd /Users/ced/Desktop/motion/backend
uv run pytest tests/eval/test_prompt_byte_identity.py::test_play_brief_basketball -v
```

**Expected:** ✅ PASSED

### 4. Run live eval (local or request in PR)

```bash
cd /Users/ced/Desktop/motion/backend
RUN_LIVE_EVAL=1 uv run pytest tests/eval/test_play_brief_eval.py -v
```

**Expected output:**
```
test_play_brief_eval.py::test_play_brief[case-0] PASSED
test_play_brief_eval.py::test_play_brief[case-1] PASSED
...
test_play_brief_eval.py::test_play_brief[case-19] PASSED
======================== 20 passed in X.XXs ========================
```

All 20 fixtures passing. If any fail, investigate whether the new prompt is worse, or whether the fixture expectation needs updating.

### 5. Commit message

```
refactor(play-brief): tighten sentence structure to 3 explicit parts

Rules are clearer now: sentence 1 = objective + anatomy, sentence 2 = defending response, 
sentence 3 = readiness. Updated golden in test_prompt_byte_identity.py to match. 
Re-baselined eval: 20/20 passing.
```

**Gate that catches mistakes:**
- Prompt changed, golden NOT updated → byte-identity test fails
- Prompt changed, golden updated, but eval NOT re-run → eval baseline may regress silently
- Eval re-run shows < baseline passing → new prompt is worse, revert

---

## Recipe 5: Add a Third Sport

**Goal:** Make the platform support a new sport (soccer, volleyball, etc.).

**Files to touch (in order):**
1. `src/motion/sports.py` — add sport literal
2. `src/motion/prompts/{sport}.py` — new prelude module
3. `src/motion/prompts/registry.py` — register new sport
4. `knowledge-base/wiki/{sport}/` — new wiki directory
5. `knowledge-base/wiki/{sport}/compiled/` — will be created by compiler
6. Tests — parametrize over SUPPORTED_SPORTS

**Step-by-step:**

### 1. Add sport literal

**File:** `src/motion/sports.py`

```python
Sport = Literal["basketball", "football", "soccer"]
SUPPORTED_SPORTS: tuple[Sport, ...] = get_args(Sport)
# Automatically updates from Literal
```

### 2. Create prelude module

**File:** `src/motion/prompts/soccer.py`

```python
"""Soccer-specific prompt preludes."""

PLAY_PRELUDE = """You are composing a coaching brief for a soccer play."""

PRACTICE_PRELUDE = """You are building a soccer practice plan focused on team positioning."""

FORM_PRELUDE = """You are analyzing a player's kicking form from video."""
```

### 3. Register in registry

**File:** `src/motion/prompts/registry.py`

```python
from motion.prompts import basketball, football, soccer

_REGISTRY: dict[Sport, ModuleType] = {
    "basketball": basketball,
    "football": football,
    "soccer": soccer,
}
```

### 4. Create wiki directory

```bash
mkdir -p /Users/ced/Desktop/motion/backend/knowledge-base/wiki/soccer
mkdir -p /Users/ced/Desktop/motion/backend/knowledge-base/wiki/soccer/compiled
```

### 5. Ingest wiki content

Use the batch API or manual authoring to populate `knowledge-base/wiki/soccer/play-*.md`, `drill-*.md`, etc. Follow same schema as basketball.

### 6. Run compiler

```bash
uv run python -m motion.wiki_ops.cli crossref --sport soccer
```

### 7. Test parametrization

**File:** `tests/unit/test_sports.py`

```python
import pytest
from motion.sports import SUPPORTED_SPORTS

@pytest.mark.parametrize("sport", SUPPORTED_SPORTS)
def test_sport_is_valid(sport):
    from motion.sports import is_valid_sport
    assert is_valid_sport(sport)

@pytest.mark.parametrize("sport", SUPPORTED_SPORTS)
def test_prompts_exist(sport):
    from motion.prompts import get_prompts
    prompts = get_prompts(sport)
    assert hasattr(prompts, "PLAY_PRELUDE")
```

### 8. Smoke test

```bash
curl -X POST http://localhost:8080/api/practice/generate \
  -H "X-Motion-Sport: soccer" \
  -H "Content-Type: application/json" \
  -d '{"level":"intermediate","duration_minutes":60,"focus_areas":["passing"]}'
```

**Expected:** 200 OK with practice blocks

**Gate that catches mistakes:**
- Missing prompt module → ValueError in get_prompts()
- Missing wiki directory → FileNotFoundError at index load
- Missing compiled/ directory → FileNotFoundError at cached_indexes()
- Forgot to add to registry → KeyError in _REGISTRY

---

## Testing Checklist (for all recipes)

Before committing:

```bash
# Lint
uv run ruff check src/ tests/

# Format
uv run ruff format src/ tests/

# Type check
uv run mypy src/motion/ (if available)

# Unit tests
uv run pytest tests/unit/ -v

# Integration tests (if router change)
uv run pytest tests/integration/ -v

# Eval tests (if prompt or output format changed)
RUN_LIVE_EVAL=1 uv run pytest tests/eval/ -v

# Full test suite
uv run pytest
```

**Quick smoke test (no DB required):**
```bash
cd /Users/ced/Desktop/motion/backend
python3 -c "
from motion.wiki_ops.retrieval import build_play_context, cached_indexes
from motion.services.play_brief import build_brief

context = build_play_context('play-black', cached_indexes())
brief = build_brief(context)
print('OK — retrieval + composer work')
print(brief.brief)
"
```

---

## Common Errors & Fixes

| Error | Cause | Fix |
|---|---|---|
| `FileNotFoundError: knowledge-base/wiki/basketball/play-*.md` | Play slug in URL doesn't exist | Check slug spelling, run lint |
| `ValueError: unknown region: hip_flexor_foo` | Typo in anatomy region | Check canonical list (spec §3.1), fix spelling |
| `json.JSONDecodeError: No JSON object could be decoded` | Claude response not JSON | Check prompt template, review Claude response in test |
| `KeyError: play-black` (in anatomy-to-play.json) | Compiler not run after adding play | Run `python -m motion.wiki_ops.cli crossref` |
| `AssertionError: expected 36/36, got 32/36` | Eval baseline degraded | Review new output in eval fixture, decide: revert prompt or update fixture |
| `test_prompt_byte_identity failed` | Prompt changed, golden not updated | Update golden in test file, ensure byte-exact match |
| `400 Invalid sport: football` | Football not added to sports.py Literal | Add to Literal, add module, add to registry |
| `ModuleNotFoundError: motion.prompts.soccer` | New sport module created but not registered | Add to _REGISTRY in registry.py |

---

## Getting Help

- **Confused about layers?** Read `docs/ARCHITECTURE.md`
- **Don't know a term?** Check `docs/GLOSSARY.md`
- **Tracing one endpoint?** Read `docs/WALKTHROUGH-practice-generate.md`
- **Rule enforcement unclear?** Read `docs/RULES.md`
- **Need a detailed example?** This file (you're reading it)

If you're stuck: flag the PR with a note, tag a senior reviewer. Better to ask than to commit a rule violation.
