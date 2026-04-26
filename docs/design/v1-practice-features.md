# Practice Generator v1 — Feature Design

> Status: design (no code). Author: Cedric. Date: 2026-04-25.
> v0 reference: commits e77e617, 4e750ca, 19cf78a (drill backfill, composer + endpoint + eval, server-side phase + anatomy enrichment).
> Parent CLAUDE.md voice + IP rules apply to every prose field below.

The v0 generator turns `{level, durationMinutes, focusAreas}` into a 5-7 block phase-tagged plan grounded in the wiki cross-ref graph. v1 adds five capabilities that move the wedge from "graph-grounded but generic" to "this practice is for *this* gym, *this* week, *this* roster". They are designed as additive, opt-in extensions of `PracticeRequest` so the v0 contract keeps working unchanged.

---

## 1. Equipment / facility constraints

### Problem
v0 assumes a fully equipped gym (cones, balls per player, partner bibs, full court). Real youth and HS programs often run on half a court with one ball per pair. The composer currently has no signal that `drill-3-station-shooting` requires three baskets — it just emits the slug.

### Schema change
- Extend `PracticeRequest` (`backend/src/motion/schemas/knowledge.py:223`) with an optional `EquipmentAvailability` block:
  - `court: "full" | "half" | "side-only"`
  - `baskets: int`  (1, 2, 4, 6+)
  - `balls: int`  (per-team count)
  - `cones: bool`
  - `pinnies: bool`
  - `tossback: bool`
- Drill front-matter migration: add an `equipment` array to drill MDs. Today equipment is prose-only inside the `## Setup` section (verified on `drill-two-on-two-recognition.md:40` — "Equipment: 1 basketball"). New schema:
  ```yaml
  equipment:
    - id: basketball
      count_per_pair: 1
    - id: cones
      count: 4
      optional: true
    - court: half
  ```
- Compiled sidecar: a new `drill-equipment.json` index produced by the existing crossref harness — `{drill_slug: equipment_spec}`. Loaded by `CompiledIndexes` (`backend/src/motion/wiki_ops/retrieval.py:237`) as `drill_equipment`.

### Migration approach
Opt-in. Every drill defaults to `equipment: [{id: basketball, count_per_pair: 1}, {court: half}]` if missing — that's the modal case in the 698-drill corpus. The backfill harness (memory: backfill-crossref-harness.md) already supports `--mode drill` additive splices; reuse it. Annotate ~150 high-value drills first (the ones that surface in 80% of plans), then long-tail.

### Composer logic delta
- `build_practice_context` (`retrieval.py:964`) gains a candidate filter step after level + duration filtering: drop drills whose equipment requirement exceeds availability.
- Half-court availability with a half-court drill needing 2 baskets → drop.
- 1 ball, 6 players, drill needs 1-per-player → drop.
- The `_PRACTICE_FOCUS` map (`retrieval.py:859`) is unchanged — equipment is a per-drill constraint, not a per-focus one.
- Stub mode (`practice_brief.py:134`) inherits the filter for free since it just picks from the candidate list.

### Frontend impact
A new "facility" panel on the practice request screen with sensible defaults (full gym, 6 baskets, 12 balls, all bibs/cones). One-tap "small school" preset (half court, 2 baskets, 4 balls).

### Eval rubric updates
Add a constraint check to `score_practice_brief` (`backend/tests/eval/_scoring.py:254`): if the case carries `equipment`, every `drill_slug` in the plan must be compatible. New signal `equipment_ok`. Expand fixtures with 2 small-school cases — these guard against the composer reaching for full-court drills when only half is available.

### Effort
**3 days.** 0.5d schema + sidecar plumbing, 1d backfill of top-150 drills (Claude batch + manual review), 0.5d filter logic, 0.5d frontend panel, 0.5d eval cases.

---

## 2. Days-to-game logic (taper)

### Problem
A practice scheduled the day before tipoff should not be a high-volume conditioning grinder. v0 has no concept of where this practice sits in the weekly arc.

### Schema change
- `PracticeRequest` gains `days_to_next_game: int | None` (0–7, optional). 0 = game today, 1 = day-before, 7+ = no game in the cycle.

### Heuristic for taper
Mapping is intentionally simple — the composer reads the heuristic, doesn't compute it.

| Days to game | Intensity ceiling | Phase mix bias                           | Examples banned                       |
|--------------|-------------------|-------------------------------------------|---------------------------------------|
| 0            | walkthrough only  | mostly skill (mental), no competitive    | conditioning, contact drills          |
| 1            | light             | warmup + skill + light scrimmage + cooldown; no high-rep conditioning | suicides, full-court press drills |
| 2            | medium            | full arc, half-volume conditioning       | none                                  |
| 3-4          | full-go           | full arc                                 | none                                  |
| 5-7+         | conditioning OK   | full arc + extended conditioning block   | none                                  |

### Composer logic delta
- `PracticeContext` carries a new `intensity_ceiling: str | None` field (`retrieval.py:191`). Set by `build_practice_context` from the days-to-game value.
- The candidate-drill filter drops drills tagged `intensity: high` when ceiling is `light` or `walkthrough`. (Drills lack an `intensity` tag today — backfill required, see Dependency below.)
- `_build_text_prompt` (`practice_brief.py:200`) adds a section "Intensity ceiling: {ceiling}. {1-line rule}" near the top of the prompt. Sonnet then biases its arc.

### Detection & eval
- Add JSONL fixtures with `days_to_next_game: 1` and assert `forbidden_drill_slugs` (e.g. no `drill-suicide-conditioning`, no `drill-full-court-press`) absent from the plan.
- New rubric signal `intensity_ok` checks the plan against a per-case denylist.
- Manual signal: cooldown phase fraction ≥ 25% on day-1 plans (vs. v0's flat 20%).

### Frontend impact
A "next game" date picker on the request screen; backend computes days. Display the taper banner on the response: "Day-before practice — light intensity, walkthrough flavor."

### Dependencies
- **Drill `intensity` tag** is a prerequisite. Add to drill front-matter in the same backfill pass as equipment. Default = `medium` for unannotated drills.

### Effort
**2 days.** 0.25d schema, 0.5d backfill the intensity tag (top-150 drills), 0.5d filter + prompt update, 0.25d eval fixtures, 0.5d FE date picker + banner.

---

## 3. Team playbook context

### Problem
A team that runs Horns sets all season should see Horns-relevant drills surface. v0 accepts `plays_in_library` (`schemas/knowledge.py:233`) but explicitly ignores it ("v0 accepts but ignores the field").

### Schema change
No new fields — wire through the existing `plays_in_library: list[str]`. Validation already caps at 20 plays (`routers/practice.py:49`).

### Composer logic delta
- `build_practice_context` (`retrieval.py:964`) gains a play-context join. For every slug in `plays_in_library`:
  - Look up `play_to_anatomy` and `play_to_technique` (`CompiledIndexes`, `retrieval.py:240–241`).
  - Union those anatomy regions and technique slugs with the focus-derived ones.
  - **Up-weight** drills that surface via a play-anchored region/technique vs. focus-only ones — boost their sort order in the candidate list.
- Add `via_play: str | None` to `PracticeDrillCandidate` (`retrieval.py:174`) so the composer prompt can render "trains hard cuts for `play-horns-flex`" instead of "trains `hip_flexor_complex`".
- Sonnet prompt update: an extra rule — "If a drill carries `via_play`, your reasoning sentence should name the play in basketball language (e.g. 'sharpens the back-cut you run in your Horns set')."

### Dependencies
- **M5 Intent Engine** is the upstream that decides *what* `plays_in_library` should contain (auto-detected from the team's history vs. coach-typed). v1 of the practice generator only consumes the list — it does not infer it. Flag in the v1 launch note: "Team-context bias works only when M5 ships the play-tagging side, or when the coach manually picks plays." This is a soft dependency: the API works either way.

### Frontend impact
A "your playbook" section on the request screen with a multi-select of slugs the user has authored. If empty, no behavior change.

### Eval rubric updates
- New fixtures: a 4-focus request with `plays_in_library: ["play-horns-flex", "play-zipper-cut"]` should produce a plan whose plurality of drills surface via those plays' anatomy/technique edges, not pure focus traversal.
- New signal `playbook_relevance`: count of blocks where `drill_slug ∈ play-derived candidate set` ≥ 50% of total blocks.

### Effort
**2 days.** 0.5d retrieval delta, 0.25d candidate prompt rendering, 0.25d composer prompt rule, 0.5d eval fixtures, 0.5d FE multi-select.

---

## 4. Per-archetype personalization

### Problem
A practice for a roster of 10 with three Sharpshooters and two Paint Beasts should not over-index on slasher footwork drills. Coach mode delivers a *team* practice — with archetype context, individual blocks can be flagged "weak side: shooters work form, slashers work finishing".

### Schema change
- `PracticeRequest` gains `archetypes_present: list[str]` — slugs from the 8 fixed archetypes (parent CLAUDE.md):
  `sharpshooter`, `floor-general`, `two-way-wing`, `athletic-slasher`, `paint-beast`, `stretch-big`, `playmaking-big`, `defensive-anchor`. Validate against this fixed set in `routers/practice.py` alongside the existing `_VALID_FOCUS` list.

### Archetype → anatomy/technique mapping
**This mapping does not exist today.** Verified: `find … concept-archetype-*.md → no matches`; only `concept-extreme-physical-archetypes.md` exists at the corpus level. v1 must author 8 new concept pages, one per archetype, with structured front-matter:

```yaml
type: concept
subtype: archetype
slug: concept-archetype-sharpshooter
weak_points:
  - region: shoulder_girdle
    rationale: shoulders fatigue late in catch-and-shoot reps
  - region: ankle_complex
    rationale: footwork on relocation cuts
priority_techniques:
  - concept-shooting-confidence-rhythm
  - concept-relocation-after-pass
```

### Composer logic delta
- `build_practice_context` adds a third edge source after focus + plays: archetype weak_points. For each archetype slug in `archetypes_present`, union its weak_points anatomy + priority_techniques into the seed lists.
- Drills already reachable via two or more sources (focus + archetype, or focus + play + archetype) get a strong boost to the top of the candidate list.
- A new optional response field per block: `target_archetypes: list[str]` — set when the drill is reached primarily via a single archetype's weak_points, so the FE can render "for your shooters" pills.

### Frontend impact
On the request screen: roster checkboxes ("which archetypes are on the floor today?"). On the response: chips on each block when applicable.

### Dependencies
- **Authoring the 8 archetype concept pages** is the prerequisite (~0.5 day each with insight from existing wiki — this is a curation task, not a research one). Without those pages, the field validates but has no graph effect.
- Soft-coupled to M5 if M5 auto-classifies players → archetypes. v1 only takes the list.

### Eval rubric updates
- New fixtures: same focus + duration, vary `archetypes_present`. Assert candidate-set differences (sharpshooter-heavy plans surface shooting-form drills more than slasher-heavy plans).
- New signal `archetype_alignment`: % of blocks where `drill_slug ∈ archetype-derived candidate set` ≥ 30%.

### Effort
**4 days.** 2d author 8 archetype concept pages + run cross-ref compile, 0.5d retrieval delta, 0.25d response field plumbing, 0.5d eval fixtures, 0.75d FE roster + chip rendering.

---

## 5. Recurring weekly view + anti-repetition

### Problem
A coach who generates a practice every day for a week today gets the same blocks because retrieval is stateless. The graph naturally clusters around the same primary-emphasis drills. Two-week practices need a memory.

### Schema change (backend)
Three additive endpoints. No persistence model change — the wiki itself doesn't track per-coach state, so this is a service-layer concern.

- `GET /api/practice/history?coach_id=…&limit=4` → returns the last N plans this coach generated. Stores plans in a Postgres table `practice_history(coach_id, generated_at, plan_json)` — uses the existing asyncpg layer (`backend/CLAUDE.md` stack section). One row per generated plan.
- `POST /api/practice/generate` is unchanged on the wire but optionally accepts `coach_id` (Clerk user id passed by the FE). When present, the router writes the response to history after composing.
- `GET /api/practice/weekly?coach_id=…` → arc summary across the last 7 days: drill repetition counts, focus-area distribution, anatomy region coverage. Used by the FE for the weekly view; not consumed by the composer.

### Schema change (frontend cache)
Localstorage cache `motion:practice:history:v1` mirroring the last 4 plans (id + summary). Read-through; backend is source of truth on conflict.

### Anti-repetition heuristic
- Inside `build_practice_context`, after computing the candidate list, optionally accept `recent_drill_slugs: list[str]` (passed by the router from the last 4 history rows, deduped, capped at ~30).
- Down-weight any candidate whose slug appears in `recent_drill_slugs` — drop it 5 sort-positions per recent appearance, but never exclude entirely (a coach who runs `drill-form-shooting` daily *should* keep getting it).
- Sonnet sees no signal of this — the candidate list reordering is sufficient.
- Special case: a "fresh angle" toggle on the FE forces a stricter filter that drops the top-3 most-repeated drills from the candidate list entirely. Power-user feature, not default.

### Weekly arc planning hint
When the FE renders the 7-day calendar, a backend stub can suggest a phase distribution: e.g. day-1 focus shooting, day-2 ball-handling, day-5 scrimmage, day-7 cooldown / walkthrough. v1 ships this as a static suggestion — heuristic later, ML never (a coach plans, the system supports).

### Frontend impact
- A new `/coach/practice/week` page with a 7-day grid. Each cell is empty or a generated-plan summary card.
- Cache hydrates instantly; live fetch reconciles.

### Eval rubric updates
- A meta-eval: run the generator 4× back-to-back with the same `(focus, duration)` tuple and `coach_id`. Plans 1–4 should have at most 50% drill-slug overlap pairwise. New signal `repetition_acceptable`.
- The existing per-plan rubric (`score_practice_brief`) is unchanged.

### Effort
**4 days.** 1d Postgres table + Alembic migration + history endpoint, 0.5d weekly endpoint, 0.5d retrieval anti-repetition delta, 0.25d meta-eval harness, 1.5d FE weekly view + cache + hydration, 0.25d "fresh angle" toggle.

---

## Dependency map (cross-feature)

| Feature | Hard deps | Soft deps |
|---|---|---|
| 1. Equipment | drill `equipment` backfill (~150 drills) | — |
| 2. Days-to-game | drill `intensity` tag backfill | — |
| 3. Team playbook | — | M5 Intent Engine for auto-tagging |
| 4. Archetypes | 8 archetype concept pages authored + compiled | M5 auto-classification |
| 5. Weekly view | Postgres table + migration | — |

**Critical path to v1: features 1, 2, 5 are independent and shippable.** Feature 4 blocks on archetype-page authoring; feature 3 is fully shippable with manual play selection but only delivers full value when M5 lands.

## Out of scope for v1

- **Per-player practice plans** — wedge stays at coach surface. Player mode consumes the practice but doesn't request its own.
- **Auto-detected fatigue / readiness chips** — the readiness query (Q-B) exists and could feed in, but composing it into the practice request is a v2 product call.
- **Practice export to LMS / video assignment** — separate workstream; not graph-related.

## Open questions

1. Where does `coach_id` live before Clerk integration? — Use Clerk's `userId` consistently; don't introduce a Motion-internal coach id.
2. Does the FE want raw plans or pre-summarized cards from `/api/practice/history`? — Default to cards (drill_slug + duration + phase), 5-10× smaller than full reasoning prose. Full plan available on click.
3. Should `archetypes_present` be a count map (`{sharpshooter: 3}`) or a set (`[sharpshooter]`)? — Set in v1; counts buy little graph signal and add validation surface.
