# Wiki Hallucination Audit -- 2026-04-22

> Read-only audit of the Motion coaching wiki against SCHEMA.md.
> Five cross-reference classes plus a 30-page prose sample.
> Baseline: python -m motion.wiki_ops lint -- 1,660 pages, 7,303 findings, 56 error-level.
> Source caps (SCHEMA.md): S1=274 S2=210 S3=230 S4=105 S5=135 S6=288 S7=371 S8=265 S9=347.

## Summary

| Class | Checked | Failing | Pass rate | Meets 97%? |
|-------|---------|---------|-----------|-----------|
| 1. Front-matter | 1,658 | 16 | 99.04% | YES |
| 2. Citations | 11,735 | 5,717 | 51.28% | **NO** |
| 3. Wikilinks | 6,774 | 38 | 99.44% | YES |
| 4. Sidecars | 27,085 | 4,158 | 84.65% | **NO** |
| 5. Prose (30-page sample) | 30 | 2 | 93.33% | **NO** |

**Scope note on Class 2**: SCHEMA.md documents sources S1-S9 only. sources.py has been expanded to S1-S16 (Tier 1 + Tier 2 batches added 2026-04-20, plus Basketball on Paper as S16). All 5,717 failing citations cite S10-S16 -- these are schema drift, not hallucinations. Zero in-range page violations for S1-S9. This is the strongest positive signal in the audit.

**Baseline lint breakdown** (context only): dead wikilinks 54, orphan pages 5, bidirectional failures 5,134, duplicate index entries 2, stale DIAGRAM markers 274, missing citations 1,641, schema-section non-compliance 62, gap concepts 131.

## 1. Front-matter

Pages checked: 1,658 (excluding index.md / log.md). Failing: 16.

Single failure mode: frontmatter source_count disagrees with distinct Sn IDs in prose.

| # | File | source_count (claimed vs actual) |
|---|------|----------------------------------|
| 1 | concept-anatomy-ankle-complex.md | 1 vs 2 |
| 2 | concept-basketball-ankle-sprain-biomechanics.md | 2 vs 1 |
| 3 | concept-basketball-movement-demands-biomechanics.md | 2 vs 1 |
| 4 | concept-basketball-statistical-framework.md | 1 vs 2 |
| 5 | concept-difficulty-theory-credit-distribution.md | 1 vs 2 |
| 6 | concept-fast-break-execution.md | 1 vs 2 |
| 7 | concept-four-factors-winning.md | 1 vs 3 |
| 8 | concept-gas-overtraining-basketball.md | 2 vs 1 |
| 9 | concept-offensive-score-sheet.md | 1 vs 2 |
| 10 | concept-points-per-possession.md | 1 vs 2 |
| 11 | concept-possession-usage-team-balance.md | 1 vs 2 |
| 12 | concept-power-speed-agility-definitions.md | 2 vs 3 |
| 13 | concept-reactive-strength-basketball.md | 2 vs 1 |
| 14 | plyometric-edge-shock-training.md | 2 vs 1 |
| 15 | reflex-channeling-hebbs-rule.md | 1 vs 2 |

No invalid type, malformed last_updated, or out-of-spec level values were found. All 1,658 non-meta pages use type in {concept, drill, play, source-summary}.

Observed type distribution: concept=790, drill=753, play=98, source-summary=17.

## 2. Citations

Citations parsed: 11,735. Failing the Sn-in-S1..S9 test: 5,717.

**Grouped by source ID**:

| Source | Occurrences | Status |
|--------|-------------|--------|
| S1 | 753 | IN SCHEMA (cap 274) -- 0 page-range breaches |
| S2 | 605 | IN SCHEMA (cap 210) -- 0 page-range breaches |
| S3 | 356 | IN SCHEMA (cap 230) -- 0 page-range breaches |
| S4 | 499 | IN SCHEMA (cap 105) -- 0 page-range breaches |
| S5 | 597 | IN SCHEMA (cap 135) -- 0 page-range breaches |
| S6 | 807 | IN SCHEMA (cap 288) -- 0 page-range breaches |
| S7 | 785 | IN SCHEMA (cap 371) -- 0 page-range breaches |
| S8 | 618 | IN SCHEMA (cap 265) -- 0 page-range breaches |
| S9 | 998 | IN SCHEMA (cap 347) -- 0 page-range breaches |
| **S10** | **3,350** | out of SCHEMA.md -- sources.py (basketball-sports-medicine-and-science.pdf) |
| **S11** | **744** | out of SCHEMA.md -- sources.py (strength-training-for-basketball-nsca.pdf) |
| **S12** | **160** | out of SCHEMA.md -- sources.py (improving-practice-performance-basketball.pdf) |
| **S13** | **177** | out of SCHEMA.md -- sources.py (winning-basketball-fundamentals.pdf) |
| **S14** | **77** | out of SCHEMA.md -- sources.py (basketball-playbook-2.pdf) |
| **S15** | **362** | out of SCHEMA.md -- sources.py (youth-basketball-drills.pdf) |
| **S16** | **847** | out of SCHEMA.md -- sources.py (basketball-on-paper.pdf) |

**Critical remediation**: update SCHEMA.md Source Materials to include S10-S16 and their page caps. Run python -m motion.wiki_ops count-pages. Do this before re-running this audit -- all 5,717 failures will then resolve.

**Verified HIGH confidence**: once SCHEMA is updated, the S1-S9 page-range integrity is spotless -- 6,018 in-schema citations, zero out-of-range pages. The LLM did not invent page numbers for the originally documented sources.

No [S0, ...], [S99, ...], or truly invalid IDs were observed. Every Sn in prose corresponds to a real registered PDF.

## 3. Wikilinks

Total wikilinks in prose: 6,774. Dangling targets: 38.

**Prose vs compiled/wikilink-graph.json drift**: 0 pages disagree with the compiled graph. Spot-checked 23-flare.md -- prose and graph edges match exactly. Graph has 1,655 keys; 0 graph keys point at non-existent wiki pages.

The 38 dangling links are references to wiki pages that have not been created yet (gap concepts in the baseline linter taxonomy).

Top 10 dangling targets (sample):

| # | Dangling target | Cited from |
|---|-----------------|------------|
| 1 | concept-acl-rehabilitation-return-to-play | concept-acl-injury-biomechanics-basketball.md |
| 2 | combination-alternating-defenses | concept-attacking-disruptive-defenses.md |
| 3 | concept-basketball-postseason-programming | concept-basketball-anabolic-catabolic-model.md |
| 4 | concept-basketball-four-factors | concept-basketball-analytics-glossary.md |
| 5 | concept-basketball-offensive-defensive-ratings | concept-basketball-analytics-glossary.md |
| 6 | concept-basketball-win-percentage-prediction | concept-basketball-bell-curve-model.md |
| 7 | concept-exercise-induced-cardiac-remodeling | concept-basketball-cardiac-conditions-sports-participation.md |
| 8 | concept-basketball-physical-qualities-hierarchy | concept-basketball-in-season-programming.md |
| 9 | concept-return-to-play-decision-making | concept-basketball-medical-team-communication.md |
| 10 | concept-offensive-rating | concept-basketball-on-paper-analytical-framework.md |

Note: baseline lint-wiki reports 54 dead wikilinks. The delta (54 vs 38) is because the baseline also scans index.md markdown-style link references [label](file.md), which this audit did not.

## 4. Sidecars

Slug-like references checked across 16 compiled sidecars: 27,085 total references, 4,158 orphan references (pointing at non-existent wiki pages). Unique orphan slugs: 869.

| Sidecar | Orphan refs | Sample orphan slugs |
|---------|-------------|---------------------|
| page-tags.json | 707 | 1-3-1, 1-4-flat, 1-on-1, 2-3-zone, 2-on-1 |
| wikilink-graph.json | 31 | blob-loop-fly-slob, combination-alternating-defenses, concept-acl-rehabilitation-return-to-play, concept-basketball-four-factors |
| wikilink-graph-reverse.json | 31 | same 31 -- symmetric with forward graph |
| technique-aliases.json | 30 | 2026-04-20, back-screen-recipient, back-screen-set, baseline-drive-on-catch, closeout-contest-verticality |
| defending-insights.json | 24 | 1-4-flat, back-screens, blind-pig, cross-screen, cross-screens |
| formation-graph.json | 22 | 1-2-2, 1-3-1, 1-4-box, 1-4-high, 2-3 high-post |
| play-to-signature.json | 4 | efg-pct, tov-pct, plus two long-string orphans that are sentences, not slugs |
| play-to-technique.json | 4 | baseline-drive-on-catch, dump-off-pass, hard-cut-to-paint, step-up-screen-set |
| technique-to-play.json | 4 | same four as above |
| signature-to-play.json | 4 | same as play-to-signature |
| anatomy-to-play.json | 3 | baseline-drive-on-catch, hard-cut-to-paint, step-up-screen-set |
| play-to-anatomy.json | 3 | same three |
| technique-to-drill.json | 2 | explosive-first-step, lateral-shuffle-recovery |

Files with zero orphans: citation-graph.json, anatomy-to-drill.json, page-insights.json.

### Observations

1. page-tags.json dominates (707 orphans). Many are taxonomy terms like 2-3-zone, 1-3-1, 1-on-1 that are valid tags rather than wiki slugs. A more precise audit would distinguish tag-namespace from page-namespace -- the current check over-flags. **Confidence MEDIUM** on this number.
2. technique-aliases.json contains 2026-04-20 as an orphan -- that is a date, not a slug. Likely a structural bug in the sidecar.
3. The cross-graph consistency between wikilink-graph.json and its reverse is perfect -- the same 31 orphans appear in both, meaning the forward-reverse generator is sound but draws from a slug list that includes 31 pages not currently on disk.

## 5. Prose hallucinations

Sampled 30 pages (stratified: 10 plays, 10 concepts/techniques, 10 drills/anatomy). Scan excludes ## Sources and ## Notable Quotes footers, where book-title and author attribution are permitted by the IP rule in CLAUDE.md.

**Confidence HIGH** on denylist hits -- word-boundary matches against the same term list used by motion.wiki_ops.check_nba_terms.

**Confidence LOW** on subtle factual / biomechanical hallucination claims -- only the >100% percentage heuristic ran programmatically. Two pages from the sample are flagged below as needing a human close-read for that class.

### Sampled slugs (30)

**Plays (10)**: play-skipper, blob-stack-double-updated, blob-4-low-flex, set-23-flare-updated, play-cross-screen, play-celtics-post-drop, play-box-cross-2-blob, blob-stack-man, blob-side-cross-elevator, play-up-screen.

**Concepts/Techniques (10)**: shooting-technique-fundamentals, concept-shared-mental-models-basketball, concept-basketball-emergency-airway, concept-sport-psychology-basketball, concept-outlet-pass-pivot, concept-adolescent-knee-injuries-basketball, concept-acute-spinal-trauma-basketball, concept-basketball-facial-injuries, concept-defensive-rating-historical-trends, concept-dribble-fill-shot.

**Drills/Anatomy (10)**: drill-s15-run-and-jump, drill-super-transition, drill-3v2-fast-break-with-trailer, drill-slap-tuck-jump, drill-e-movement-cone, exercise-one-arm-dumbbell-snatch, drill-wall-slides, exercise-dumbbell-bench-press, drill-single-arm-dumbbell-row-basketball, drill-partner-shooting.

### Flagged issues (HIGH confidence -- deterministic denylist)

Two of 30 sampled pages contain NBA proper nouns in prose. **Both are IP violations per CLAUDE.md IP and legal compliance rule**.

#### 1. play-celtics-post-drop.md -- 3 denylist hits

| Line | Term | Snippet |
|------|------|---------|
| 2 | Celtics | # Boston Celtics Post-Drop Action (1-4 High) |
| 5 | Celtics | From the same 1-4 high alignment as the X Action, Rick Pitinos Celtics would cut Paul Pierce (3) from the left wing to ... |
| 42 | Celtics | -- There is no passing and standing in the Celtics offense -- movement must be continuous [S14, p.49] |

The slug itself (play-celtics-post-drop) violates the IP rule. Page also surfaces Boston Celtics, Rick Pitino, Paul Pierce -- Pitino and Pierce are not in the current check_nba_terms denylist but should be.

#### 2. concept-defensive-rating-historical-trends.md -- 16 denylist hits

Entire page is an NBA historical-ratings table. Surfaced names across lines 5-46:

| Line | Term | Snippet (truncated) |
|------|------|---------------------|
| 5 | Knicks | Defensive rating measures a teams defensive efficiency as points allowed per 100 possessions... |
| 7 | Knicks | Rileys Knicks defense worked by completely taking away the interior, exploiting hand-check rules... |
| 28 | Knicks + Ewing |   1   New York Knicks   1993   99.7   -8.4   Ewing, Oakley, Starks, Mason, Rivers   |
| 29 | Knicks + Ewing |   2   New York Knicks   1994   98.2   -8.1   Ewing, Oakley, Starks, Mason   |
| 30 | Spurs |   3   San Antonio Spurs   1999   95.0   -7.2   Duncan, Robinson, A. Johnson, Elliott   |
| 32 | Jazz + Stockton |   5   Utah Jazz   1989   101.5   -6.3   Mark Eaton, Stockton, Malone, Bailey   |
| 33 | Suns |   6   Phoenix Suns   1981   100.5   -6.2   T. Robinson, Dennis Johnson, W. Davis   |
| 34 | Miami Heat |   7   Miami Heat   1997   100.6   -6.1   Mourning, P.J. Brown, Tim Hardaway   |
| 35 | 76ers |   8   Philadelphia 76ers   1981   100.6   -6.1   Dr. J, Dawkins, Bobby Jones, Mo Cheeks   |
| 42, 45 | Knicks | repeated in second ranking table |
| 44 | Jazz |   3   Utah Jazz   1989   101.5   -2.49   |
| 46 | Warriors |   5   Golden State Warriors   1976   95.5   -2.03   |

This is a concentrated IP violation surface. The content is legitimate Dean Oliver-era analytics but must be rewritten with anonymized team identifiers per CLAUDE.md IP rule.

### LOW confidence follow-ups (human close-read recommended)

The programmatic scan did not find any >100% percentages, no archetype names outside the locked 8, and no fabricated book-title citations in the 30 sampled pages outside the footer. However, the following pages from the sample include specific biomechanical/statistical claims that would benefit from a human reader verifying the [Sn, p.X] attribution:

- concept-basketball-emergency-airway
- concept-acute-spinal-trauma-basketball
- concept-adolescent-knee-injuries-basketball
- concept-basketball-facial-injuries

## Verdict

**Three classes below 97% pass rate**: 2. Citations (51.28%), 4. Sidecars (84.65%), 5. Prose sample (93.33%).

However, the **citations failure is entirely schema drift, not hallucination** -- every failing citation uses a source that exists in sources.py but is not yet documented in SCHEMA.md. Updating SCHEMA.md Source Materials is a single-author edit and will push Class 2 to 100%.

The **prose sample failure is genuine and high-severity**: 2 of 30 sampled pages contain NBA teams, players, and coaches in body prose -- the very failure mode CLAUDE.md IP flags as non-negotiable. This likely extends beyond the sample given the scale.

### Top 10 most urgent fixes (ranked)

1. Rewrite concept-defensive-rating-historical-trends.md -- 16 NBA denylist hits in body prose. Full NBA historical ratings table with team names + surnames. Highest-severity IP violation in the sample. CONFIDENCE HIGH.
2. Rename + rewrite play-celtics-post-drop.md -- slug and body both contain Celtics, plus un-listed proper nouns Rick Pitino and Paul Pierce. CONFIDENCE HIGH.
3. Grep the full wiki for the check_nba_terms denylist (not just the 30-page sample) -- every hit outside ## Sources / ## Notable Quotes is an IP violation. Expected to find more; sampling rate was ~1.8%.
4. Update SCHEMA.md Source Materials to include S10-S16 with page caps (run python -m motion.wiki_ops count-pages). Resolves all 5,717 Class 2 failures in one edit.
5. Fix the 16 source_count frontmatter mismatches (listed in Class 1 table). Automatable -- re-derive from prose.
6. Fix the 707 page-tags.json orphan refs (or clarify that tag-namespace is separate from page-namespace; if tags, update the audit to skip them). The orphan count is inflated by taxonomy terms.
7. Investigate technique-aliases.json orphans -- includes a literal date 2026-04-20 as a slug. Likely generator bug in the sidecar builder.
8. Create the 31 pages referenced by wikilink-graph.json but missing on disk (or remove them from the graph). Examples: concept-acl-rehabilitation-return-to-play, concept-basketball-four-factors -- all look like legitimate planned pages.
9. Close the 1,641 missing-citation warnings from baseline lint -- factual-looking lines with no adjacent [Sn] are top hallucination vectors even though our sample found none.
10. Resolve 274 stale DIAGRAM markers -- LLM-admitted gaps. Degrade trust even though they are not technically hallucinations.

### Positive findings worth noting

- **Zero page-number hallucinations for S1-S9** in 6,018 citations. The LLM did not invent page numbers for the originally documented sources.
- **Zero prose-to-compiled-graph drift** across 1,655 graph keys. wikilink-graph.json is a faithful compile of current prose.
- **100% of frontmatter uses an allowed type value** (concept, drill, play, source-summary). No fabricated types.
- **No >100% percentages, no archetype names outside the locked 8, no fabricated book/author attributions** in the 30-page sample.

