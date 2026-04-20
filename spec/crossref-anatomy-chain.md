# Cross-Reference — Anatomy ↔ Technique ↔ Play ↔ Drill

> Status: DRAFT v0 — design doc, not implementation.
> Scope: Highest-moat cross-reference edge in Motion's retrieval layer.
> Authoritative prerequisites: [`spec/karpathy-llm-wiki.md`](./karpathy-llm-wiki.md), [`knowledge-base/SCHEMA.md`](../knowledge-base/SCHEMA.md).
> Companion tooling: [`backend/src/motion/wiki_ops/lint_wiki.py`](../src/motion/wiki_ops/lint_wiki.py), [`frontmatter.py`](../src/motion/wiki_ops/frontmatter.py).

## 1. Why this edge

No competitor (coaching clipboard, HoopsU, FastDraw) links anatomy to play execution. A play that demands hard baseline cuts links to the hip-mobility anatomy page, which links to the mobility drill. Weakest body part becomes a play recommendation filter. The chain enables three Engine outputs no rival can match:

- **Drill prescription**: "Given play X requires hard hip-flexor cutting, the mobility work to stock it is `[[drill-band-lateral-walk]]` and `[[exercise-hip-thrust]]` [S2, pp.18-19]."
- **Readiness filter**: "Player Y flagged tight hips. Tonight's playable rotation excludes plays requiring hip-flexor-*required*; drills prescribed for tomorrow reset that region."
- **Drill justification**: "Why are we doing this? Because it prepares step 2 of `[[play-black]]`."

The Engine retrieves the chain as graph walks over compiled sidecars + wikilinks. The wiki stays the persistent Karpathy artifact. This doc specifies the edge only — not the Engine.

## 2. Locked design decisions

Five decisions below. Each is a response to an R1/R2 contradiction the teammates surfaced.

1. **No new page types.** Anatomy and technique are modeled as `type: concept` pages with naming prefix + tags. Reason: SCHEMA.md recognizes only four types (concept, drill, play, source-summary); amending the constitution is a larger scope than the cross-ref itself. Precedent: `concept-core-anatomy-basketball.md` is already `type: concept`. New anatomy pages follow the pattern `concept-anatomy-{region}.md`. New technique pages (where needed) follow `concept-technique-{name}.md`.
2. **Criticality is a binary**, not ordinal, not numeric. Values: `required | optional`. Previous draft used `required | supporting | optional`; collapsed 2026-04-20 after Q3 resolution (supporting grade was never consumed by the three canonical retrieval queries in §7 — YAGNI). Numeric weights rejected for the same reason given in the previous draft: imply precision the corpus doesn't support. Schema examples in §4 still show `supporting` — read as `optional` until examples are rewritten (deferred hygiene).
3. **Posture is always-on at the data layer, injury-gated at the retrieval layer.** Front-matter always exists on every relevant play/drill. The Engine applies anatomy filters only when an injury flag or mobility-screen score is present. Reconciles the R1-always-on vs R2-Angle-I-dormant tension: both are right, at different layers.
4. **Cross-ref edges live in extended front-matter keys plus mandatory `[[wikilinks]]`.** Front-matter is machine-grain; wikilinks satisfy SCHEMA.md §Cross-Linking (≥2 related pages, bidirectional). The compiler inverts the forward-link metadata; the lint already enforces the visible graph.
5. **Compiler output = JSON sidecars in the wiki directory.** Not a separate database, not a service. Fits Karpathy pattern: wiki owns the cross-refs. One forward index + one reverse index per edge type. Consumed by the Engine at retrieval time; cached by SHA of the source front-matter.

## 3. Canonical vocabularies (seed)

### 3.1 Anatomy regions

**Verified muscle anchors** (extracted verbatim from existing wiki pages — HIGH confidence):

| Source file | Region-candidates named |
|---|---|
| [`concept-core-anatomy-basketball.md`](../knowledge-base/wiki/concept-core-anatomy-basketball.md) | transversus abdominis, transversospinalis (multifidus, rotators), pelvic floor, diaphragm, rectus abdominis, hip flexors, erector spinae, hamstrings, glutes |
| [`exercise-hip-thrust.md`](../knowledge-base/wiki/exercise-hip-thrust.md) | gluteus maximus, hamstrings (semitendinosus, semimembranosus, biceps femoris), adductor magnus, gluteus medius, gluteus minimus, erector spinae, quadriceps (rectus femoris, vastus lateralis, vastus medialis, vastus intermedius) [S2, pp.18-19] |

**Seed canonical region IDs** — rolled up to coaching-useful grain. Audited 2026-04-20 against `source-basketball-anatomy.md` (S2 chapter breakdown). **S2 is organized by exercise category (Legs / Core / Upper-Pulling / Upper-Pushing / Explosive / Plyometrics / Rehab / Injury Prevention), not by muscle region.** Muscle vocabulary is *derivable* from muscle names inside exercises, not from chapter titles. 2 regions flagged for removal; per-region confidence breakdown is declared below the list:

```
hip_flexor_complex      # iliopsoas, rectus femoris, sartorius, TFL
glute_max               # gluteus maximus — horizontal propulsion
glute_med               # gluteus medius — lateral stability
hamstring_group         # biceps femoris, semitendinosus, semimembranosus
quad_group              # quadriceps — extension, deceleration
adductor_group          # adductor magnus, longus, brevis, pectineus
ankle_complex           # ATFL, CFL, posterior ligaments + proprioception
calf_complex            # gastrocnemius, soleus
core_inner              # transversus abdominis, multifidus, pelvic floor, diaphragm
core_outer              # rectus abdominis, obliques, erector spinae (superficial)
obliques                # internal + external
lower_back_erectors     # erector spinae deep
lat_group               # latissimus dorsi
chest_group             # pectoralis major + minor
shoulder_complex        # deltoids + rotator cuff aggregate
rotator_cuff            # supraspinatus, infraspinatus, teres minor, subscapularis
trap_group              # trapezius upper, mid, lower
bicep_group             # biceps brachii
tricep_group            # triceps brachii
# grip_forearm          # REMOVED — not emphasized in S2 chapter breakdown
knee_joint              # patellofemoral + tibiofemoral
acl_complex             # ACL + dynamic valgus risk chain — S2 Ch 8 dedicated focus, esp. female athletes
patellar_tendon         # jumper's-knee target — S2 Ch 7
# cervical_spine        # REMOVED — absent from S2 source-summary chapter breakdown
thoracic_spine          # mid-back mobility — S2 Ch 7 rehab
```

**S2 chapter → region mapping** (for source citation on future anatomy pages):
- Ch 1 Legs → glute_max, glute_med, hamstring_group, quad_group, adductor_group, hip_flexor_complex, calf_complex
- Ch 2 Lower Back and Core → core_inner, core_outer, obliques, lower_back_erectors
- Ch 3 Upper-Pulling → lat_group, trap_group, bicep_group
- Ch 4 Upper-Pushing → chest_group, shoulder_complex, tricep_group
- Ch 7 Rehabilitation → ankle_complex, rotator_cuff, thoracic_spine, knee_joint
- Ch 8 Injury Prevention → acl_complex, patellar_tendon (ACL-specific chapter for female athletes)

Parents (for rollup queries): `lower_body`, `upper_body`, `core`, `posterior_chain`, `anterior_chain`.

**Confidence on the seed list** (after pruning grip_forearm and cervical_spine; 23 regions remain):
- **HIGH** (~11 regions) — muscle named verbatim in pages already Read: glute_max, glute_med, hamstring_group, quad_group, adductor_group, rotator_cuff, hip_flexor_complex, core_inner, core_outer, lower_back_erectors, and erector-derived regions. Anchored to `exercise-hip-thrust.md:49-51` and `concept-core-anatomy-basketball.md:25`.
- **MEDIUM** (~12 regions) — mapped to an S2 chapter heading via the source-summary (section above), but not yet verified against a specific muscle-name prose line in an existing wiki page: calf_complex, ankle_complex, knee_joint, acl_complex, patellar_tendon, thoracic_spine, lat_group, chest_group, shoulder_complex, trap_group, bicep_group, tricep_group, obliques. Upgrade to HIGH requires a read of the relevant S2 chapter or the authored concept-anatomy page.
- *Completeness check* — the source-summary enumerates Chs 1-8 + 10 but does not list every muscle mentioned inside each exercise; fringe regions (e.g., scapular stabilizers beyond rotator_cuff) may still exist in S2 and need a PDF read before the vocabulary is fully locked.
- One existing anatomy page today: `concept-core-anatomy-basketball.md`. Creating the ~23 new `concept-anatomy-*.md` pages is genuine net-new authoring, not re-organization.

### 3.2 Techniques

Techniques are athletic actions — cuts, jumps, landings, contact, ball-handling moves. Many already exist in the corpus as `concept-*` pages. Examples confirmed from earlier agent scans (MEDIUM confidence on file existence):

- `concept-first-step-quickness`
- `concept-five-jumping-skills`
- `concept-curl-shot-off-screen`
- `concept-defensive-box-out-footwork`
- `concept-dribble-curl-shot`
- `concept-hop-back-crossover-combo`
- `concept-jump-shot-release-and-follow-through`
- `concept-flex-bump-option-footwork`

Seed canonical technique IDs for the play→technique edge. Audited 2026-04-20 against all 270 `concept-*.md` files (Bash+Grep).

**Corpus convention observed (with caveat)**: existing concept files use a filename convention where `concept-X-footwork.md` emphasizes screener/setter mechanics and `concept-X-reads.md` emphasizes cutter/recipient decisions. **Content-verified by reading `concept-back-screen-reads.md` and `concept-flex-back-screen-footwork.md` on 2026-04-20: both page types are hybrid** (both cover cutter AND screener actions). Filename indicates primary emphasis, not strict role partition. Seed-ID aliases below are valid alias targets; HIGH-confidence labels mean the target page exists and covers the named action, not that content is role-purist.

**Technique-id → existing concept-slug mapping**:

| Technique ID | Mapped slug | Confidence |
|---|---|---|
| explosive-first-step | `concept-first-step-quickness` | HIGH |
| pin-down-screen-set | `concept-pin-screen` + `concept-pin-screen-footwork` | HIGH |
| pin-down-screen-recipient | `concept-down-screen-reads` | HIGH |
| back-screen-recipient | `concept-back-screen-reads` | HIGH |
| flare-screen-recipient | `concept-flare-screen-reads` | HIGH |
| stagger-screen-set | `concept-stagger-screen-footwork` | HIGH |
| spin-screen-set | `concept-spin-screen-footwork` | HIGH |
| post-seal-footwork | `concept-offensive-post-footwork` + `concept-post-receiving-footwork` | HIGH |
| screen-the-screener | `concept-screen-the-screener-footwork` | HIGH |
| baseline-drive-on-catch | `concept-dribbling-driving-techniques` (general) | MEDIUM |
| step-up-screen-set | `concept-setting-screens` (general) | MEDIUM |
| back-screen-set | `concept-flex-back-screen-footwork` (flex-specific) | MEDIUM |
| lateral-shuffle-recovery | `concept-defensive-footwork-breakdown-drills` (general) | MEDIUM |
| flare-screen-set | *no page* | NEW REQUIRED |
| hard-cut-to-paint | *no page* | NEW REQUIRED |
| flash-cut | *no page* | NEW REQUIRED |
| soft-landing-mechanics | *no page* | NEW REQUIRED |
| closeout-contest-verticality | *no page* | NEW REQUIRED |
| dump-off-pass | *no page* | NEW REQUIRED |
| skip-pass | *no page* | NEW REQUIRED |
| dribble-handoff-receipt | *no page* | NEW REQUIRED |

**Coverage summary**: 9 HIGH-confidence alias mappings, 4 MEDIUM (general pages can be referenced; specific variants not yet authored), 8 NEW pages to author. Ratio roughly 60/40 existing vs. needed.

**Gap cluster**: the 8 NEW pages cluster around **landing mechanics, closeouts, pass types, handoff reception, flash cuts**. Screens are richly covered (54 files match screen-* patterns); skill-execution and pass-type techniques are under-indexed.

**Decision on aliasing vs renaming** (answers Open Q2): **alias, don't rename**. The cross-ref compiler maintains a `technique-id → existing-slug` lookup table in `knowledge-base/wiki/compiled/technique-aliases.json`. Renaming 54+ screen-related files would cascade dead-wikilink lint failures.

**Confidence on the technique vocabulary**: HIGH for the 9 aliased + MEDIUM for the 4 general + pending for the 8 new authored pages. Upgraded from LOW after full concept-* audit.

## 4. Front-matter schema extensions

All additive. Parser (`frontmatter.py`) passes unknown keys through silently. Lint does not yet validate these keys — adding optional lint rules is a follow-on.

### 4.1 Play page

```yaml
---
type: play
category: offense
formation: 5-out
tags: [man-to-man, step-up-screen, baseline-drive]
source_count: 1
last_updated: 2026-04-20
# NEW — cross-ref extensions:
demands_techniques:
  - id: baseline-drive-on-catch
    role: "2"               # role-labelled digit per play data convention
    criticality: required
  - id: step-up-screen-set
    role: "4"
    criticality: required
  - id: hard-cut-to-paint
    role: "5"
    criticality: required
demands_anatomy:            # denormalized from techniques; compiler verifies consistency
  - region: hip_flexor_complex
    criticality: required
  - region: glute_max
    criticality: required
  - region: ankle_complex
    criticality: supporting
  - region: core_outer
    criticality: supporting
---
```

### 4.2 Concept-as-technique page (`concept-technique-*.md`)

```yaml
---
type: concept
level: intermediate
tags: [technique, cutting, first-step]
source_count: 2
last_updated: 2026-04-20
# NEW:
movement_family: cutting    # cutting | jumping | landing | contact | dribble | screen | closeout | recovery
chain: lower_body           # lower_body | posterior | core | upper_body | full_body
demands_anatomy:
  - region: hip_flexor_complex
    quality: mobility
    criticality: required
  - region: glute_max
    quality: strength
    criticality: required
  - region: ankle_complex
    quality: elastic_strength
    criticality: supporting
trained_by_drills:
  - id: drill-band-lateral-walk
    emphasis: primary
  - id: exercise-hip-thrust
    emphasis: primary
---
```

### 4.3 Concept-as-anatomy page (`concept-anatomy-*.md`)

```yaml
---
type: concept
level: beginner
tags: [anatomy, lower-body, mobility-critical]
source_count: 1
last_updated: 2026-04-20
# NEW:
anatomy_region: hip_flexor_complex
parent_region: lower_body
muscles: [iliopsoas, rectus_femoris, sartorius, tensor_fasciae_latae]
joints: [hip]
qualities_trainable: [mobility, strength, elastic_strength]
assessment_signals: [hip_rotation_rom, overhead_squat_depth]
---
```

### 4.4 Drill / exercise page

```yaml
---
type: drill
level: intermediate
positions: [PG, SG, SF, PF, C]
players_needed: 1
duration_minutes: 15-20
tags: [strength, glutes, landing]
source_count: 1
last_updated: 2026-04-20
# NEW:
trains_anatomy:
  - region: glute_max
    emphasis: primary
  - region: hamstring_group
    emphasis: secondary
trains_techniques:
  - id: explosive-first-step
    emphasis: primary
  - id: soft-landing-mechanics
    emphasis: supporting
---
```

## 5. Visible cross-links (SCHEMA.md compliance)

Front-matter is machine-grain. SCHEMA.md §Cross-Linking requires human-visible `[[wikilinks]]` in body, bidirectional.

For each forward edge declared in front-matter, a matching wikilink appears in the page body:

- Play page → `## Related Concepts` block adds `[[concept-anatomy-hip-flexor-complex]] — required for baseline-drive-on-catch (role 2)`
- Technique page → `## Related Concepts` adds `[[concept-anatomy-*]]` per demanded region, plus `[[drill-*]]` per training drill
- Anatomy page → `## Related Concepts` back-links to every technique demanding it
- Drill page → existing `## Concepts Taught` extended with `[[concept-anatomy-*]]`

The existing lint rule `_check_bidirectional` (lint_wiki.py:418) enforces the back-link. The compiler emits a pre-commit warning if front-matter declares an edge without the matching wikilink.

## 6. Compiler spec

**Location**: `backend/src/motion/wiki_ops/crossref.py` — sibling of `lint_wiki.py`.

**Input**: the wiki directory (`knowledge-base/wiki/*.md`).

**Output**: four JSON files under `knowledge-base/wiki/compiled/`:

```
compiled/
  play-to-anatomy.json        # {play-slug: [{region, criticality}]}
  play-to-technique.json      # {play-slug: [{technique-id, role, criticality}]}
  anatomy-to-play.json        # {region: [{play-slug, criticality}]}      ← inverted
  anatomy-to-drill.json       # {region: [{drill-slug, emphasis}]}        ← inverted
  technique-to-play.json      # {technique-id: [play-slugs]}              ← inverted
  technique-to-drill.json     # {technique-id: [drill-slugs]}             ← inverted
```

All outputs are inversions of front-matter `demands_*` and `trains_*` arrays. No inference. No LLM in the compile path. Expected run cost is low (seconds, not minutes) on the current 1,036-file corpus — **not benchmarked; verify at implementation time**.

**Invariants the compiler enforces**:
1. Every `demands_anatomy[].region` exists in the anatomy vocabulary registry (lint error if unknown region).
2. Every `demands_techniques[].id` resolves to a `concept-technique-*.md` or a whitelisted existing concept (warning if unresolved).
3. Every `trains_*` reference to a technique or anatomy resolves (warning if unresolved).
4. Every forward edge in front-matter has a matching `[[wikilink]]` in the body (warning; SCHEMA.md §Cross-Linking bidirectional).
5. A play with more than 5 `required` anatomy regions is flagged (warning; likely over-tagging).

**Integration with existing pipeline**: hook into `wiki_ops/cli.py` as `motion wiki crossref compile`. Runs after `lint_wiki.py`. Output files committed to the wiki directory (Karpathy pattern: wiki owns cross-refs).

## 7. Retrieval query patterns

Three queries the Engine runs. Each is a direct index lookup — no graph walk unless noted.

### Q-A. Drill prescription for a play

```
input: play-slug
step 1: play-to-technique[slug] → techniques[]
step 2: for each technique, technique-to-drill[id] → drills[]
step 3: play-to-anatomy[slug] → anatomy[]
step 4: for each anatomy, anatomy-to-drill[region] → drills[]
step 5: dedup, rank by emphasis=primary first
output: ranked drill list with cited [S2, p.X] per drill
```

### Q-B. Readiness filter

```
input: set of flagged regions (e.g. {hip_flexor_complex})
step 1: for each region, anatomy-to-play[region] → plays[]
step 2: filter to criticality==required → EXCLUDE set
step 3: all plays MINUS EXCLUDE → SAFE set
step 4: anatomy-to-drill[region] (filter emphasis=primary) → PRESCRIPTION set
output: {playable_tonight: SAFE[], recovery_work: PRESCRIPTION[]}
```

### Q-C. Drill justification

```
input: drill-slug
step 1: drill.trains_anatomy → regions[]
step 2: drill.trains_techniques → techniques[]
step 3: for each technique, technique-to-play[id] → plays[]
step 4: for each region, anatomy-to-play[region] (criticality=required) → plays[]
step 5: intersect and dedup
output: "This drill prepares you to run: [[play-X]], [[play-Y]]"
```

## 8. Eval fixtures

File: `backend/eval/crossref-anatomy.jsonl`. Initial seed — 5 cases covering the three query types. Each case:

```json
{
  "case_id": "q-a-play-black-drill-rx",
  "query": "Q-A",
  "input": {"play_slug": "black"},
  "expected_chunk_ids": ["drill-band-lateral-walk", "exercise-hip-thrust", "drill-bird-dog"],
  "forbidden_chunks": ["drill-shoulder-press-overhead"],
  "notes": "Expected drills target hip-flexor-complex and glute-max per play-black.md front-matter; forbidden shows the compiler is not over-matching."
}
```

Scoring function: precision@5, recall@all. Eval runs in CI on every wiki PR. Same harness as the parked CV fidelity eval (`tests/cv/test_cv_fidelity.py`) — reuse the parametrized pytest pattern.

## 9. Worked example — `play-black.md`

Source: [`/Users/ced/Desktop/motion/backend/knowledge-base/wiki/play-black.md`](../knowledge-base/wiki/play-black.md), verified 2026-04-20.

Existing front-matter (verbatim):
```yaml
type: play
category: offense
formation: 5-out
tags: [man-to-man, step-up-screen, baseline-drive, post-flash, layup, kickout, quick-hitter]
source_count: 1
last_updated: 2026-04-11
```

Body already has phases citing [S4, p.56]. The Counters section has 2 bullets, **unverified provenance** (R2-failures audit flagged as LLM-inferred — do not ingest into the cross-ref chain until provenance audit is complete).

**Proposed front-matter additions**:

```yaml
demands_techniques:
  - id: baseline-drive-on-catch
    role: "2"
    criticality: required
  - id: step-up-screen-set
    role: "4"
    criticality: required
  - id: hard-cut-to-paint
    role: "5"
    criticality: required
  - id: dump-off-pass
    role: "2"
    criticality: supporting
demands_anatomy:
  - region: hip_flexor_complex
    criticality: required
  - region: glute_max
    criticality: required
  - region: ankle_complex
    criticality: supporting
  - region: core_outer
    criticality: supporting
```

**Full chain traverse** (verified endpoints in italic; proposed in plain):

| Step | Via | Target | Status |
|---|---|---|---|
| play-black | demands_techniques | baseline-drive-on-catch | technique page **does not exist yet** — needs creation or alias to existing concept |
| baseline-drive-on-catch | demands_anatomy | hip_flexor_complex | anatomy page **does not exist yet** — needs `concept-anatomy-hip-flexor-complex.md` |
| hip_flexor_complex | backed by | [S2, pp.47] iliopsoas/horizontal propulsion | *verified verbatim in `exercise-hip-thrust.md`* |
| hip_flexor_complex | trained_by | [`exercise-hip-thrust.md`](../knowledge-base/wiki/exercise-hip-thrust.md) | *verified existing file* |
| hip_flexor_complex | trained_by | [`drill-band-lateral-walk.md`](../knowledge-base/wiki/drill-band-lateral-walk.md) | *existence claimed by R2-anatomy teammate; not re-verified in this session* |

The chain can be **partially** traversed today with extant pages. Full traversal requires:
1. Creating `concept-anatomy-{region}.md` for the ~25 seed regions.
2. Creating `concept-technique-{name}.md` (or aliasing to existing concepts) for the ~16 seed techniques.
3. Back-annotating `play-black.md` + 4 other PoC plays with the new front-matter keys.

Rough authoring estimate for step 1 alone: ~25 regions, **unbenchmarked** — budget at least a half-day, likely more, once an S2 chapter audit clarifies scope and per-region depth.

## 10. Open questions

1. ~~**S2 chapter audit**~~ — **ANSWERED 2026-04-20**: S2 is organized by exercise category, not muscle. Vocabulary stays muscle-region-organized (queryable shape); each region is citation-anchored to an S2 chapter via the mapping above. Pruned to 23 regions; `grip_forearm` and `cervical_spine` removed.
2. ~~**Technique aliasing vs. new files**~~ — **ANSWERED 2026-04-20**: alias, don't rename. Cross-ref compiler maintains a `technique-id → existing-slug` lookup at `knowledge-base/wiki/compiled/technique-aliases.json`. Existing pages stay at their current slugs to avoid cascading dead-wikilink failures across 54+ screen-referencing files. 9 HIGH + 4 MEDIUM aliased today; 8 NEW pages authored fresh as `concept-technique-*` under the naming prefix.
3. ~~**Criticality of `supporting` vs `optional`**~~ — **ANSWERED 2026-04-20**: collapsed to binary `required | optional`. Dropped `supporting`. Reason: all three canonical queries in §7 filter only on `criticality==required`; supporting was never consumed. §2 updated; §4 examples flagged for later rewrite (deferred hygiene).
4. ~~**Provenance gate**~~ — **ANSWERED 2026-04-20**: anatomy chain (edge #1) is NOT gated on the provenance audit — it runs on front-matter, not on the Counters prose the audit flagged. Failure-mode edge (#2) IS gated. A standing `source_confidence: verbatim | paraphrase-with-source | inferred` field is added to the schema now so edge #2 is ready when it lands.
5. ~~**Team-name conflict**~~ — **ANSWERED 2026-04-20**: the conflict is latent, not active. `check_nba_terms.py` scans all wiki `.md` content (front-matter included; only `log.md` whitelisted) and would fail any play using `team: Lakers`. Grep on `play-*.md` for `^team:` returned zero matches — no play uses the field. **Recommendation: remove `team:` from SCHEMA.md §Play to resolve the documentation-vs-enforcement conflict**; archetypes replace team attribution per parent CLAUDE.md. This is a SCHEMA.md cleanup, not a cross-ref concern.

## 10a. Corpus hygiene observations (found during audits)

Orthogonal to the cross-ref design, but needs logging:

- `post-double-team-rotation.md` / `post-double-team-rotations.md` — near-duplicate, both cite `[S1, p.15]`.
- `concept-backdoor-cut.md` / `concept-backdoor-cut-continuity.md` — near-duplicate, both cite `[S7, pp.117-119]`.
- `concept-defensive-strategies-del-harris.md` / `concept-defensive-strategy-del-harris.md` — singular/plural twin.
- `acl-injury-prevention.md` / `acl-and-shoulder-injury-prevention.md` — overlapping topic coverage, found during anatomy audit.
- IP-leaking slugs: `concept-olajuwon-whirl-move.md`, `concept-dribble-moves-van-gundy.md`, `concept-jab-step-van-gundy.md`, and the two `del-harris` concept pages above.
- `source-basketball-anatomy.md` line 37 contains a typo: `"the pro team' team orthopedic physician"`. Line 11: `"pro team team physician"` (double "team").
- 5/5 sampled plays contain at least one LLM-inferred bullet in `## Counters` with no provenance tag (see §10 Q4).
- SCHEMA.md §Play documents a `team: Lakers | Warriors` front-matter field that `check_nba_terms.py` would block on lint. Grep found zero plays using it. Recommend removing from SCHEMA.md to close the latent conflict.

Hygiene cleanup is a prerequisite for edges #2-6 (especially defense-mirror and contradictions) but the anatomy chain (edge #1) can proceed in parallel — it doesn't touch these files.

## 11. Non-goals

- UX / Obsidian browsing surface — the wiki is retrieval-layer only per user direction.
- Graph DB — wiki owns the cross-refs per Karpathy pattern.
- Multi-sport abstraction — football in fall 2026 is a separate spec.
- Implementation code — this doc is schema + queries + eval seed only.
- Defense-mirror, failure-mode, symptom-catalog, contradictions — separate cross-ref edges, separate specs.
- Amending SCHEMA.md — deliberately avoided.

## 12. Gate checklist (for sign-off)

- [ ] Phase 1 — node-type decisions in §2 accepted
- [ ] §3 anatomy seed list audited against S2 chapter structure
- [ ] §3 technique seed list mapped to existing `concept-*` pages where possible
- [ ] §4 front-matter schema reviewed against `frontmatter.py` behaviour
- [ ] §7 retrieval queries match what the Engine (router `knowledge.py`) actually needs
- [ ] §8 eval fixture shape approved before first case is authored
- [ ] §9 worked example on `play-black.md` accepted or re-scoped
- [ ] §10 open questions answered or explicitly deferred
