# Walkthrough: POST /api/practice/generate

**Last Updated:** 2026-04-28

Trace one complete feature end-to-end: a coach requests a practice plan. Every hop, file:line ref, and what breaks if data is missing.

## Request → Response

```http
POST /api/practice/generate HTTP/1.1
X-Motion-Sport: basketball
Content-Type: application/json

{
  "level": "intermediate",
  "duration_minutes": 60,
  "focus_areas": ["shooting", "defense"],
  "custom_plays": []
}
```

```json
{
  "blocks": [
    {
      "order": 1,
      "phase": "warmup",
      "drills": [
        {
          "drill_slug": "drill-dynamic-stretching",
          "duration_minutes": 10,
          "anatomy_chips": ["hip_flexor_complex", "glute_max"]
        }
      ]
    }
  ],
  "source": "claude"
}
```

## 1. Router Entry: routers/practice.py

**File:** `src/motion/routers/practice.py:145-180`

```python
@router.post("/generate")
async def generate_practice(
    request: Request,
    body: PracticeRequest,
) -> PracticeResponse:
    sport = current_sport(request)  # Extract X-Motion-Sport header (middleware applied in main.py:71)
    
    # Validate inputs
    if body.level not in _VALID_LEVELS:
        raise HTTPException(400, f"invalid level: {body.level}")
    if body.duration_minutes not in _VALID_DURATIONS:
        raise HTTPException(400, f"invalid duration: {body.duration_minutes}")
    for focus in body.focus_areas:
        if focus not in _VALID_FOCUS:
            raise HTTPException(400, f"unknown focus area: {focus}")
    if len(body.focus_areas) > _MAX_FOCUS_AREAS:
        raise HTTPException(400, f"too many focus areas")
    
    # Step 1: Build context (Layer 3)
    context = build_practice_context(
        sport=sport,
        level=body.level,
        focus_areas=body.focus_areas,
        duration_minutes=body.duration_minutes,
    )
    
    # Step 2: Compose brief (Layer 4)
    brief = build_practice_brief(context, sport=sport)
    
    # Step 3: Parse response + enrich
    blocks = _parse_blocks(brief.brief)
    blocks = _enrich_blocks(blocks, context)
    
    return PracticeResponse(
        blocks=blocks,
        source=brief.source,
    )
```

**What breaks:**
- Missing `X-Motion-Sport` header → defaults to `"basketball"` (src/motion/middleware/sport.py:34)
- Invalid level/duration/focus → HTTP 400
- Context builder fails (Step 1) → 500 (see next section)

## 2. Retrieval Layer 3: build_practice_context()

**File:** `src/motion/wiki_ops/retrieval.py:420-500` (pseudo-line, actual is longer)

```python
def build_practice_context(
    sport: Sport = DEFAULT_SPORT,
    level: str = "intermediate",
    focus_areas: list[str] = None,
    duration_minutes: int = 60,
) -> PracticeContext:
    """Assemble a bundle of coach inputs + filtered drills + anatomy/technique graph."""
    
    # Load compiled indexes from disk (cached per sport)
    indexes = cached_indexes(sport=sport)  # File: wiki/{sport}/compiled/*.json
    
    # Resolve focus areas to drill tags
    # focus_areas: ["shooting", "defense"] → tag_filter = {"shooting", "defense"}
    
    # Resolve level to drill tier (via knowledge-base/wiki/{sport}/compiled/level-filter.json)
    # level: "intermediate" → min_level=50, max_level=79 (hypothetical numeric scale)
    
    # Query 1: anatomy-to-drill[level=intermediate, tags in focus_areas]
    # → candidates = [
    #   {slug: "drill-form-shooting", trains_anatomy: ["shoulder_girdle", "wrist_complex"]},
    #   {slug: "drill-defensive-stance", trains_anatomy: ["hip_flexor_complex", "core_outer"]},
    #   ...
    # ]
    
    # Filter by duration constraints
    # A 60-min session typically has 5-7 blocks of 8-15 min each
    # Filter out drills > 20 min or < 5 min
    candidates = [c for c in candidates if 5 <= c.duration_minutes <= 20]
    
    # Sort by emphasis (primary first), then by anatomy criticality
    candidates.sort(key=lambda d: (
        0 if d.emphasis == "primary" else 1,
        -d.trains_anatomy_count,
    ))
    
    return PracticeContext(
        level=level,
        focus_areas=focus_areas,
        duration_minutes=duration_minutes,
        candidate_drills=candidates,
        plays_library=body.custom_plays or [],  # For drill justification
    )
```

**Data flow:**
1. `cached_indexes()` loads `wiki/{sport}/compiled/anatomy-to-drill.json` (via lru_cache)
2. Focus areas filter drills by tags (tag intersection)
3. Level filter prunes by front-matter `level: beginner|intermediate|advanced`
4. Duration prunes by `duration_minutes` front-matter field
5. Emphasis ranking ensures primary drills show first
6. Return frozen PracticeContext dataclass

**What breaks:**
- Missing `wiki/{sport}/compiled/anatomy-to-drill.json` → FileNotFoundError at index load
  Fix: Run `python -m motion.wiki_ops.cli crossref` first
- Drill page missing `trains_anatomy` or `trains_techniques` → skipped (optional field)
- Unknown focus area slug → no candidates filtered (empty result)
- All drills exceed duration bounds → no candidates (coach gets empty blocks)

**Example**: Basketball session for "intermediate shooting defense 60 min":
- `focus_areas = ["shooting", "defense"]` → filters to drills tagged with both
- `level = "intermediate"` → filters to `level: intermediate` drills
- `duration_minutes = 60` → candidates with 5-20 min duration only
- Result: ~8-10 candidates sorted by emphasis

## 3. Composer Layer 4: build_practice_brief()

**File:** `src/motion/services/practice_brief.py:50-180`

```python
def build_practice_brief(
    context: PracticeContext,
    sport: Sport = DEFAULT_SPORT,
) -> BriefResult:
    """Turn PracticeContext into a structured practice plan with timing + rationale."""
    
    # Fetch sport-switched prompt template
    prompts = get_prompts(sport=sport)  # Returns motion.prompts.{basketball|football}
    prelude = prompts.PRACTICE_PRELUDE  # Sport-specific opening line
    
    # Serialize context for Claude
    # Extract: focus_areas, level, duration, candidate drills + their anatomy
    context_json = asdict(context)
    
    if os.getenv("ANTHROPIC_API_KEY"):
        # Claude mode: invoke Sonnet 4.6 with strict template
        prompt = _build_prompt_instructions(
            context,
            sport=sport,
            prelude=prelude,
        )
        # Prompt includes:
        # - System message: "You are a practice planner..."
        # - Context JSON: candidate drills, focus areas, constraints
        # - Task: "Generate 5-7 blocks in JSON format:
        #   [{order, phase, drills: [{slug, duration_min, rationale}]}]"
        # - Constraints: byte-identity test guards this exact template
        
        response = anthropic.Anthropic().messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1200,
            system=PRACTICE_SYSTEM_MESSAGE,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        brief_text = response.content[0].text
        return BriefResult(
            brief=brief_text,
            source_citations=[],  # Practice brief doesn't cite sources (no prose)
            source="claude",
        )
    else:
        # Stub mode: deterministic fallback
        return _build_stub_practice(context)
```

**Data flow:**
1. Load sport-switched prompts: `motion/prompts/{basketball,football}.py`
   - Basketball: "High-tempo focused practice prioritizing ball-screen fluency"
   - Football: "Coverage-based drill progressions emphasizing gap discipline"
2. Serialize PracticeContext to prompt JSON
3. If API key exists: Claude Sonnet → structured JSON response (5-7 blocks)
4. If no API key: Stub mode → deterministic blocks from context
5. Return frozen BriefResult dataclass (brief + source + citations)

**Prompt template byte-identity:**
The prompt instruction text (not context data) is hand-pinned and test-guarded in `tests/eval/test_prompt_byte_identity.py:_practice_golden`. Any wording change breaks the test → must update golden in same commit.

**What breaks:**
- Missing `motion/prompts/{sport}.py` module → ValueError in `get_prompts()`
  Fix: Add new sport to registry in `prompts/registry.py`
- Invalid JSON in Claude response → parse fails → BriefResult.brief is empty string
  Fix: eval fixture catches malformed JSON output
- Claude timeout (>30s) → HTTPException 504 propagates from router
- Missing context fields → schema validation fails before composer runs

## 4. Response Parsing: _parse_blocks()

**File:** `src/motion/routers/practice.py:200-250`

```python
def _parse_blocks(brief_text: str) -> list[PracticeBlockOut]:
    """Extract JSON array from Claude's response text."""
    # Claude response might be:
    # "Here's your practice plan:\n[{...}, {...}]\n\nEnjoy!"
    # Extract the JSON array only
    
    match = re.search(r"\[.*\]", brief_text, re.DOTALL)
    if not match:
        raise ValueError(f"no JSON array found in response")
    
    blocks_json = json.loads(match.group())
    # Validate schema
    blocks = [PracticeBlockOut(**b) for b in blocks_json]
    return blocks
```

**What breaks:**
- Claude response has no JSON array → ValueError → 500
- JSON is malformed (extra comma, missing quote) → json.JSONDecodeError → 500
- Block missing required field (order, phase, drills) → PracticeBlockOut validation fails

## 5. Response Enrichment: _enrich_blocks()

**File:** `src/motion/routers/practice.py:250-310`

```python
def _enrich_blocks(
    blocks: list[PracticeBlockOut],
    context: PracticeContext,
) -> list[PracticeBlockOut]:
    """Attach anatomy chips to each drill in each block."""
    
    # Load drill→anatomy map (precomputed)
    drill_to_anatomy = _drill_to_anatomy()
    
    for block in blocks:
        for drill in block.drills:
            if drill.drill_slug in drill_to_anatomy:
                drill.anatomy_chips = drill_to_anatomy[drill.drill_slug]
    
    return blocks
```

**Data flow:**
1. Load inverted index: `wiki/{sport}/compiled/anatomy-to-drill.json` →
   flip to drill_slug → [regions]
2. For each drill in response, attach trained regions as visual chips
3. UI renders as colored badges: "hip flexor", "glutes", etc.

**What breaks:**
- Drill slug not in wiki → no anatomy chips attached (ok, UI handles gracefully)
- anatomy-to-drill.json missing → _drill_to_anatomy() KeyError → 500

## 6. Final Response

**File:** `src/motion/routers/practice.py:310-330`

```python
return PracticeResponse(
    blocks=[
        PracticeBlockOut(
            order=1,
            phase="warmup",
            drills=[
                {
                    "drill_slug": "drill-dynamic-stretching",
                    "duration_minutes": 10,
                    "anatomy_chips": ["hip_flexor_complex", "glute_max"],
                    "rationale": "prepares ankle mobility for shooting cuts"
                }
            ]
        ),
        # ... 4-6 more blocks
    ],
    source="claude",  # or "stub"
)
```

## Full Data Flow Diagram

```
POST /api/practice/generate
    ↓
SportMiddleware (main.py:71)
    ├─ extract X-Motion-Sport header
    └─ set request.state.sport
    ↓
routers/practice.py:generate_practice()
    ├─ validate inputs (level, duration, focus_areas)
    │
    ├─ [Step 1] build_practice_context(sport, level, focus_areas, duration)
    │   ├─ cached_indexes(sport)
    │   │   ├─ load wiki/{sport}/compiled/anatomy-to-drill.json
    │   │   ├─ load wiki/{sport}/compiled/technique-to-drill.json
    │   │   └─ lru_cache all 6 indexes (per-sport)
    │   │
    │   ├─ Focus filter: drills tagged with ["shooting", "defense"]
    │   ├─ Level filter: drills with level="intermediate"
    │   ├─ Duration filter: drills with 5-20 min
    │   └─ Return PracticeContext(candidates=[...], focus_areas=[...])
    │
    ├─ [Step 2] build_practice_brief(context, sport)
    │   ├─ get_prompts(sport)
    │   │   ├─ return motion.prompts.basketball (or football)
    │   │   └─ fetch PRACTICE_PRELUDE (sport-specific)
    │   │
    │   ├─ [if ANTHROPIC_API_KEY set]
    │   │   ├─ _build_prompt_instructions(context, sport, prelude)
    │   │   ├─ Claude Sonnet 4.6 call (max_tokens=1200)
    │   │   ├─ Extract JSON array from response
    │   │   └─ Return BriefResult(brief=json_str, source="claude")
    │   │
    │   └─ [else stub mode]
    │       └─ Return BriefResult(brief=stub_json, source="stub")
    │
    ├─ [Step 3] _parse_blocks(brief.brief)
    │   ├─ Regex extract JSON array
    │   ├─ json.loads()
    │   └─ Validate against PracticeBlockOut schema
    │
    ├─ [Step 4] _enrich_blocks(blocks, context)
    │   ├─ Load _drill_to_anatomy() (lru_cached)
    │   ├─ For each drill, attach anatomy_chips
    │   └─ Return enriched blocks
    │
    └─ Return PracticeResponse(blocks=blocks, source=source)
         ↓
        JSON → Coach's browser (frontend/src/app/coach/practice/page.tsx)
```

## Testing

**Unit tests:** `tests/unit/test_practice_gen.py` (stub mode only, no API calls)
- Input validation (bad level, duration)
- Context builder filters correctly
- Response schema validation

**Integration tests:** `tests/integration/test_practice_router.py`
- Full router call with mocked Claude response
- Anatomy chip enrichment

**Eval fixtures:** `eval/practice.jsonl` (5 cases, live or stub)
- Input: coach request
- Expected: blocks contain correct drills for focus area
- Forbidden: coach should never see advanced drills when requesting beginner
- Scoring: precision (correct drill count), recall (all expected drills included)

**Smoke test:**
```bash
curl -X POST http://localhost:8080/api/practice/generate \
  -H "X-Motion-Sport: basketball" \
  -H "Content-Type: application/json" \
  -d '{"level":"intermediate","duration_minutes":60,"focus_areas":["shooting"]}'
```

## Common Pitfalls

**Missing wiki compilation**
If you add a new drill page but don't run `python -m motion.wiki_ops.cli crossref`, the drill won't appear in `anatomy-to-drill.json`. Result: practice plans never suggest it.
Fix: Compiler must run after any wiki edit.

**Empty focus area**
If you request focus_areas=["unknown-focus"], the query finds zero drills. Coach gets empty blocks. No error — frontend should catch and warn.
Fix: Validate focus area against `_VALID_FOCUS` before calling build_practice_context.

**Missing anatomy field on drill**
Drill page has no `trains_anatomy` front-matter. Enrichment skips it, anatomy_chips stays empty. UI renders drill without visual context. Valid but less informative.
Fix: Not critical — drills without trains_anatomy are still valid.

**Claude timeout**
Sonnet takes >30s to respond. Router times out → 504 Gateway Timeout. UI shows degradation.
Fix: Increase max_tokens bound or split the request (not yet implemented).

**Prompt wording change**
You modify `PRACTICE_SYSTEM_MESSAGE` but forget to update the golden in `test_prompt_byte_identity.py`. Commit lands, CI passes locally but fails in CI runner with different Claude version/temperature. Silent eval drift.
Fix: Always update byte-identity golden in same commit. Run `RUN_LIVE_EVAL=1 uv run pytest tests/eval/` to re-baseline.
