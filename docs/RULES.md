# Cross-Cutting Rules

**Last Updated:** 2026-04-28

Four non-negotiable rules that guard the platform. Each has enforcement points and concrete pass/fail examples.

## Rule 1: IP Rule (Structural Metadata OK, Book Prose NOT)

**In one sentence:** Structural metadata derived from books is safe to surface to users. Book prose is not.

**Definition:**

**Structural metadata** (OK to surface):
- Play/drill/concept slugs (e.g., `play-black`, `drill-band-lateral-walk`, `concept-anatomy-hip-flexor-complex`)
- Formation names (e.g., `5-out`, `box-1`, `pick-and-roll`)
- Anatomy region names (e.g., `hip_flexor_complex`, `glute_max`)
- Technique IDs and skill names (e.g., `baseline-drive-on-catch`, `explosive-first-step`)
- Drill tags and categories (e.g., `[shooting, ball-handling, conditioning]`)
- Archetype names (e.g., `Sharpshooter`, `Floor General`)
- Four-Factor statistics (e.g., `efg-pct`, `tov-pct`)
- Position abbreviations (PG, SG, SF, PF, C)
- Page metadata (last_updated, source_count, level, players_needed)

**Book prose** (NEVER surface to users):
- Coaching cues or teaching language from source books (e.g., "stay low, hands active")
- Principles text (e.g., "A good screener must flash hard out of the break")
- Common-mistake symptoms/corrections copied from source (e.g., "knees cave inward — drive through heels")
- Drill objectives or descriptions paraphrased from source
- NBA team names, player names, coach names (e.g., "Lakers", "Olajuwon", "Popovich")
- Book titles (e.g., "Let's Talk Defense", "Basketball Anatomy")
- Chapter summaries
- Quoted statistics or injury data

**Engine's role:** Consumes book prose from `insights:` fields in compiled bundles (Layer 3) to compose its own prose in Motion's voice. It does NOT pass source wording through to users.

**Citation tokens:** `[Sn, p.XX]` footnotes are developer-only (internal only). They never appear on user-facing surfaces or in API responses.

### Pass Examples ✅

```python
# PASS: Surface structural metadata
{
  "brief": "Black uses explosive-first-step cuts to attack the hip-flexor complex.",
  "anatomy_chips": ["hip_flexor_complex", "glute_max"],
  "drills": [
    {"slug": "drill-band-lateral-walk", "region": "hip_flexor_complex"},
    {"slug": "exercise-hip-thrust", "region": "glute_max"}
  ]
}

# PASS: Surface slug + role + formation
{
  "play": "play-black",
  "formation": "5-out",
  "positions": ["PG", "SG", "SF", "PF", "C"],
  "technique_demands": [
    {"id": "baseline-drive-on-catch", "role": "2"},
    {"id": "step-up-screen-set", "role": "4"}
  ]
}

# PASS: Export archetype + anatomy in roster form
[
  {"player": "Alice", "archetype": "Sharpshooter", "flagged_regions": ["shoulder_girdle"]},
  {"player": "Bob", "archetype": "Floor General", "flagged_regions": []}
]
```

### Fail Examples ❌

```python
# FAIL: Quote book prose on user surface
{
  "brief": "Stay low, hands active. [Source: Basketball Anatomy, p.18]",
  # ❌ This is source prose. Even with citation, it's surfaced.
}

# FAIL: Paraphrase book prose as if original
{
  "brief": "The player's knees are turning inward—drive through your heels.",
  # ❌ This describes a form error from source. Should be Engine-composed voice.
}

# FAIL: Surface book title
{
  "source_material": "NBA Playbook chapter 3: Pick-and-Roll Sets",
  # ❌ Book title visible to user. Aggregate language only ("the canon", "the literature").
}

# FAIL: Include NBA player name in public play
{
  "description": "Similar to how Olajuwon executes the drop-step against zone defenses.",
  # ❌ Named player comparison. Forbidden per IP rule v3.
}

# FAIL: Surface coach name
{
  "concept": "Defensive strategies endorsed by Coach Popovich",
  # ❌ Named coach attribution. Violates anonymization.
}

# FAIL: Include book count or stat
{
  "footer": "Compiled from 16 coaching books, 4,500 pages, 700 drills.",
  # ❌ Aggregate stat that reveals source scope. Forbidden per IP rule strictness.
}

# FAIL: Citation token visible to user
{
  "brief": "The player's hips are tight. [S2, p.47]",
  # ❌ Citation tokens are developer-only. Strip before JSON response.
}
```

### Enforcement Points

| Where | Mechanism | Catches |
|---|---|---|
| Brief prompts | System message: "do not quote books, do not paraphrase source prose" | Claude paraphrasing |
| Form-coach prompts | Explicit instruction: "speak basketball (shooting elbow), not anatomy (elbow complex)" | Jargon leakage |
| Voice tests | Regex match on `forbidden_phrases.txt` (NBA names, book titles, banned vocab) | IP leaks + promotional language |
| Check command | `npm run check:nba-terms` (frontend) | Team/player/coach names in wiki + code |
| Lint | `wiki-lint` (backend, registered in pyproject.toml) | Detects slugs like `concept-olajuwon-*.md` |

**When you add new wiki pages:** Verify slug, frontmatter fields, and body prose don't leak IP. The slug `concept-olajuwon-whirl-move.md` fails lint. The phrase "as Van Gundy says" in prose fails voice tests.

**When you modify a prompt:** Review the fewshot example. If it paraphrases source prose, replace with Engine-composed voice. Byte-identity test will catch prompt changes — update the golden in same commit.

---

## Rule 2: Voice Rule (Declarative, Prestige, No Banned Vocabulary)

**In one sentence:** User-facing prose is declarative and prestige-register. No hype, no "unlock", no emoji.

**Definition:**

Voice is: Declarative (facts, not questions). Concrete before abstract. Short sentences. Prestige register (professional, not casual).

Voice is NOT: Promotional, hype-driven, rhetorical questions, exclamation marks, casual slang, emoji, brand-speak.

**Banned vocabulary:**
- unlock, level up, game-changer, revolutionary, supercharge, empower, journey, unleash, seamless, insights (as noun), AI-powered, next-generation, reimagine, dominate, crush, grind, hustle

**Form-coach specific:** Speak basketball, not anatomy. A junior's knees caving is "knees caving in" or "losing stability on landing", NOT "knee valgus" or "anti-rotation deficit". Audience = players + coaches, not medical professionals.

### Pass Examples ✅

```
# PASS: Declarative, prestige
"Black targets the hip-flexor complex and glutes through baseline-drive cuts. 
Primary development: band lateral walk (emphasis: hip stability). 
Defending teams often use drop coverage."

# PASS: Form coaching in basketball language
"Your shooting elbow is drifting right on the release. 
Keep it under the ball at the same angle throughout."

# PASS: Concrete before abstract
"This play creates a secondary playmaker read when the initial cutter is denied. 
It develops quick decision-making and baseline footwork."

# PASS: Short sentences
"The drill builds glute activation. 
It pairs well with jump-landing mechanics."
```

### Fail Examples ❌

```
# FAIL: Promotional, exclamation mark
"Unlock your potential with explosive-first-step development!"
# ❌ "Unlock", exclamation mark, hype.

# FAIL: Rhetorical question
"Ready to revolutionize your defense?"
# ❌ Rhetorical question, "revolutionize" (banned).

# FAIL: Casual, no sentence structure
"Hip flexors = key to cutting. Let's go!"
# ❌ Casual, emoji-adjacent tone.

# FAIL: Clinical jargon (form coaching)
"Your knee is demonstrating significant valgus at the landing phase. 
Recommend proprioceptive training to address anti-rotation deficits."
# ❌ Medical jargon. Should be "knees caving in" + "do single-leg hops".

# FAIL: Vague before concrete
"Develop your potential through this drill. 
It trains footwork."
# ❌ Vague opening ("develop your potential"), then concrete.

# FAIL: Branded language
"Next-generation insights powered by AI."
# ❌ "Next-generation", "powered by AI", "insights" (as noun). All banned.
```

### Enforcement Points

| Where | Mechanism | Catches |
|---|---|---|
| Voice tests | Regex match on `forbidden_phrases.txt` | Banned vocab + exclamation marks |
| Brief prompts | Fewshot example + system message | "speak prestige, not promo" |
| Form-coach prompts | Explicit instruction: "basketball language, not anatomy" | Clinical jargon |
| Manual review | Code review step before PR merge | Tone + readability |

**When you update a brief:** Run `uv run pytest tests/eval/test_play_brief_eval.py -v` to check for banned vocab.

**When you write new form-coach feedback:** Have a coach review it. "Knees caving in" ✅. "Knee valgus moment" ❌.

---

## Rule 3: Sport Boundary (Every Module Must Accept sport: Sport)

**In one sentence:** No module hardcodes "basketball". All wiki reads go through `wiki_dir(sport=...)`. All prompts go through `get_prompts(sport)`.

**Definition:**

The sport boundary pattern enables adding football (or a third sport) without touching Layer 3 (retrieval) or Layer 4 (composers). Only changes needed:
1. Add sport literal to `motion/sports.py:Sport`
2. Add per-sport SCHEMA.md doc (or reference shared schema)
3. Create `motion/prompts/{sport}.py` with sport-specific preludes
4. Run compiler on new sport's wiki directory

Every code path that reads wiki or produces prose must:
1. Accept `sport: Sport` parameter (or inherit from `Request` context)
2. Pass it to `wiki_dir(sport=...)` for path resolution
3. Pass it to `get_prompts(sport)` for prompt dispatch
4. Default to `DEFAULT_SPORT = "basketball"` for backward compatibility

**Current sport state (as of 2026-04-28):**
- Basketball: fully wired (wiki, compiled indexes, prompts, tests)
- Football: partial wiring (wiki directory exists, prompts exist, middleware threads sport, but routers not yet sport-parameterized)

### Pass Examples ✅

```python
# PASS: Router accepts sport via middleware
@router.post("/api/practice/generate")
async def generate_practice(request: Request, body: PracticeRequest):
    sport = current_sport(request)  # Via SportMiddleware
    context = build_practice_context(sport=sport, ...)
    brief = build_practice_brief(context, sport=sport)
    return PracticeResponse(...)

# PASS: Retrieval accepts sport
def build_play_context(slug: str, sport: Sport = DEFAULT_SPORT) -> PlayContext:
    indexes = load_indexes(sport=sport)  # Loads wiki/{sport}/compiled/
    return PlayContext(...)

# PASS: Service accepts sport
def build_practice_brief(
    context: PracticeContext,
    sport: Sport = DEFAULT_SPORT,
) -> BriefResult:
    prompts = get_prompts(sport)  # Returns motion.prompts.{basketball|football}
    prelude = prompts.PRACTICE_PRELUDE
    # ... compose with sport-switched prompt

# PASS: Adding a third sport
# 1. motion/sports.py: Sport = Literal["basketball", "football", "soccer"]
# 2. motion/prompts/soccer.py: new module with PLAY_PRELUDE, PRACTICE_PRELUDE
# 3. motion/prompts/registry.py: add "soccer": soccer to _REGISTRY
# 4. knowledge-base/wiki/soccer/: new wiki directory + compiled/
# Done — no changes to retrieval, routers, composers.
```

### Fail Examples ❌

```python
# FAIL: Hardcoded sport
def build_practice_context(level: str, focus_areas: list[str]) -> PracticeContext:
    indexes = load_indexes()  # Assumes basketball
    # Missing sport parameter

# FAIL: Sport not threaded through
@router.post("/api/practice/generate")
async def generate_practice(body: PracticeRequest):
    context = build_practice_context(sport="basketball")  # Hardcoded
    # Should be: sport = current_sport(request)

# FAIL: Wiki read hardcoded to basketball
def get_play_by_slug(slug: str) -> dict:
    path = Path("knowledge-base/wiki/basketball") / f"{slug}.md"
    # Should be: path = wiki_dir(sport=...) / f"{slug}.md"

# FAIL: Prompt dispatch hardcoded
def compose_brief(context: PlayContext) -> str:
    prompt = basketball.PLAY_PRELUDE  # Hardcoded
    # Should be: prompts = get_prompts(sport); prompt = prompts.PLAY_PRELUDE

# FAIL: New sport not added to registry
# You create motion/prompts/volleyball.py but forget to add it to _REGISTRY
def get_prompts(sport: Sport = DEFAULT_SPORT):
    if sport == "volleyball":
        return volleyball  # KeyError — not in _REGISTRY
```

### Enforcement Points

| Where | Mechanism | Catches |
|---|---|---|
| Type hints | `sport: Sport` parameter on public functions | Missing sport threading |
| Middleware | `SportMiddleware` sets `request.state.sport` | Ensures header is available |
| Wiki path resolution | `wiki_dir(sport=...)` raises ValueError for unknown sport | Hardcoded paths |
| Prompt registry | `get_prompts(sport)` raises ValueError for missing module | Forgotten prompt modules |
| Test parametrization | Tests parametrize over SUPPORTED_SPORTS | Catches sport-specific regressions |

**When you add a new endpoint:** Accept `Request` parameter, call `current_sport(request)`, pass sport to all layer 3 + 4 calls.

**When you add a new sport:** Create FOUR things: (1) wiki directory, (2) prompts module, (3) registry entry, (4) compiled directory.

---

## Rule 4: Eval-as-Spec (Prompt Strings Are Byte-Identity Tested)

**In one sentence:** Prompt wording is part of the spec. Change it → update the test golden in the same commit. No silent baseline drift allowed.

**Definition:**

Eval fixtures define correctness. The 30 fixtures in `eval/*.jsonl` are the source of truth for what correct output looks like. The test baseline (e.g., "36/36 passing") is a contract.

If you modify a prompt string:
1. The byte-identity test (`tests/eval/test_prompt_byte_identity.py`) breaks
2. You MUST update the test golden (the hand-pinned string) in the same commit
3. You MUST run `RUN_LIVE_EVAL=1 uv run pytest tests/eval/` to re-baseline the output against the new prompt
4. You MUST verify the eval baseline survives (e.g., still 36/36)

If you don't, you risk silent regression: the prompt drifts, Claude's output changes subtly, eval fixtures fail (or worse, silently pass with lower precision).

### Pass Examples ✅

```python
# PASS: Commit 1 — update prompt + golden + re-baseline
# File: motion/services/play_brief.py
_PLAY_SYSTEM_MESSAGE = """You are composing a brief for a basketball play...
Emit exactly three sentences...
"""  # ← Changed "exactly three" to "2-3"

# File: tests/eval/test_prompt_byte_identity.py
_BASKETBALL_PLAY_BRIEF_GOLDEN = """You are composing a brief for a basketball play...
Emit exactly 2-3 sentences...
"""  # ← Updated golden

# Terminal:
$ RUN_LIVE_EVAL=1 uv run pytest tests/eval/test_prompt_byte_identity.py
# Result: ✅ 36/36 passing (baseline survives)
# Commit message: "refactor(play-brief): tighten sentence count to 2-3"

# PASS: Prompt structure change with backward-compatible fallback
# Old: emit JSON with "brief" field only
# New: emit JSON with "brief" + "focus" fields
_PLAY_SYSTEM_MESSAGE = """...
Output JSON: {"brief": "...", "focus": "..."}
"""

# Golden updated, eval re-run: 36/36 passing
```

### Fail Examples ❌

```python
# FAIL: Update prompt, forget golden
# File: motion/services/play_brief.py
_PLAY_SYSTEM_MESSAGE = """You are composing a brief for a basketball play.
NEW INSTRUCTION: Always start with 'This play'.
"""  # ← Changed

# File: tests/eval/test_prompt_byte_identity.py
_BASKETBALL_PLAY_BRIEF_GOLDEN = """You are composing a brief for a basketball play.
"""  # ← Forgot to update!

# Terminal:
$ uv run pytest tests/eval/test_prompt_byte_identity.py
# Result: ❌ FAILED — byte mismatch. Caught by CI.

# FAIL: Update prompt, skip live eval
# Prompt changed, golden updated, but RUN_LIVE_EVAL=1 not run
$ uv run pytest tests/eval/test_prompt_byte_identity.py
# Result: ✅ Test passes (bytes match), BUT
$ RUN_LIVE_EVAL=1 uv run pytest tests/eval/
# Result: ❌ 28/36 failing — eval baseline degraded silently during dev

# FAIL: Subtle prompt drift over multiple commits
# Commit A: add a word → byte-identity test catches it, golden updated, eval re-run
# Commit B: different word → test catches it, golden updated, eval re-run  
# ... but by Commit F, the prompt has drifted so much that eval is now 20/36
# Risk: if golden was updated but eval re-run was skipped, baseline silently regressed
```

### Enforcement Points

| Where | Mechanism | Catches |
|---|---|---|
| Unit test | `test_prompt_byte_identity.py` | Prompt wording changes |
| CI gate | Test fails if prompt != golden | Catches drift before merge |
| Eval gate | `RUN_LIVE_EVAL=1` re-baselines against live Claude | Catches output degradation |
| Commit discipline | Code review step: "did you update golden + re-baseline?" | Silent baseline drift |

### Checklist Before Merging a Prompt Change

- [ ] Prompt wording changed in `motion/services/*.py` or `motion/prompts/*.py`
- [ ] Golden updated in `tests/eval/test_prompt_byte_identity.py` (match byte-for-byte)
- [ ] Ran `RUN_LIVE_EVAL=1 uv run pytest tests/eval/` locally (or approved by senior)
- [ ] Eval baseline stable (e.g., still 36/36, 30/30, 10/10)
- [ ] Commit message mentions prompt change + eval baseline

**When you're uncertain:** Ask in PR: "Does this prompt change need re-baselining?" The answer is almost always yes.

**When you change a prompt and eval fails:** Don't adjust fixtures to match the new output. Investigate whether the new prompt is actually better. If it's regressed, revert the prompt change. If it's improved, update fixtures only after re-reading the memory notes on eval discipline.

---

## Rule 5: Backward Compatibility via DEFAULT_SPORT

**In one sentence:** Legacy code paths that predate the sport boundary default to basketball. No breaking changes for partial deployments.

Code that doesn't explicitly accept/thread a `sport` parameter falls back to `DEFAULT_SPORT = "basketball"`. This preserves pre-sport-boundary behavior during phased rollouts.

Example: If frontend hasn't yet sent `X-Motion-Sport: football` header, backend still works (falls back to basketball). No 400 errors or crashes.

When all frontend code has been deployed with sport headers, the default can be made stricter (future Step 7+). For now, it's a safety valve.
