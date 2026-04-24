# MOTION COACHING INSTRUMENT — Behavioral, Retention, and Product-Intent Audit

*Prepared by Motion Internal Strategy — Intent & Retention Audit, March 2026.*

---

## Executive Summary

Motion is a coaching instrument. It is not a feed, not an assistant, not a dashboard. The product promises that the next right move is on the screen before the coach asks. The retention question is therefore not "how do we bring them back" but "how do we earn first-open status on the two days of the week where the instrument is indispensable — practice day and game day."

This audit makes three claims.

First, Motion's retention gap is not in intelligence quality. The wiki is compiled from seven coaching volumes totalling 2,440 printed pages, including *NBA Playbook* (934 pp.), *Coaches Playbook* (371 pp.), and *Let's Talk Defense* (274 pp.). The intelligence density is already there. The gap is that intent-engine output is not yet ritualised, and that ritualisation is the only retention currency a coaching tool has. A coach's week has fixed edges — practice blocks, shoot-arounds, film review, tip-off, halftime. The instrument must occupy those edges with the consistency of a stopwatch.

Second, Motion's three user modes — coach, player, student of the game — do not share a retention profile. Coach cadence peaks twice per week at game-day and midweek practice. Player cadence is continuous (daily drills, weekly body check). Student cadence is curiosity-led (browse, return, browse). One retention model cannot serve all three. The audit treats them as three curves, not one.

Third, the design constraint that the game-clock already provides scarcity means Motion must not manufacture urgency. Time decay is real — scouting report half-life is under 72 hours, opponent footage goes stale by tip-off — and Motion should surface that decay. It must not invent countdowns, streaks that punish absence, or notification anxiety. The register is Leica, not scratch card.

**Frameworks applied.** Nir Eyal's Hook Model (Trigger, Action, Variable Reward, Investment). B.J. Fogg's Behaviour Model (B = M × A × P). Variable reward theory, loss aversion, commitment devices, and the Zeigarnik effect. These are diagnostic lenses. None override Motion's voice and IP rules.

**Scope.** Landing, Game Plan Generator, Halftime, Practice Planner, Play Viewer, Player Experience, Student/Knowledge Search. Eighteen features specified. Three-phase roadmap. Metrics framework with current baseline and Phase-1 targets.

---

## Part 1 — Behavioural Architecture

### 1.1 Hook Model mapped to Motion

Motion's hook is not a notification. It is the bus-ride open — the coach checks the instrument before the team bus leaves for the away game, and the answer is already there.

| Hook phase | Motion surface | Mechanism |
|---|---|---|
| Trigger (external → internal) | Calendar day, schedule signal, day-of-week, season phase; internal trigger is the coach's own pre-practice anxiety ("what do I run tonight") | Intent Engine fires one of five intents from eight passive signals; no picker, no choice |
| Action | Open app. That is the action. No tap sequence, no filter. The Dynamic Assembly has already chosen 14 atoms and composed 7 components | Signals load server-side; page renders the assembled intent |
| Variable Reward | Which play ranks first. Which halftime chip fires. Which drill the body-lab recommends. Which Socratic question the wiki offers tonight | Variability comes from signals + wiki cross-links, not from artificial randomisation |
| Investment | Roster uploaded, schedule loaded, film tagged, archetypes assigned. Each increment improves the next open | Data compounds; a coach who logs three weeks has a materially different instrument on week four |

The model applies cleanly. The one adaptation: Motion's Action step is near-zero by design. The product is the answer, not a flow to an answer. Most retention designs over-weight Action (how many taps, how many screens). Motion should under-weight it and invest the saved complexity budget in the Variable Reward and Investment columns.

### 1.2 Fogg diagnosis — where Motion fails today

B = M × A × P. For retention to fire, motivation, ability, and a prompt must all land at the moment of intent.

- **Motivation.** High for coaches on game day, high for players on practice day, medium for students ambient-curious. No motivation problem at peak. Problem is at trough — the off-day, the week without a game, the summer break.
- **Ability.** Friction is currently low on the shipped surfaces (Landing, Play Viewer). Friction is high on the unbuilt surfaces (Game Plan Generator requires roster + schedule + film — most users arrive with none of the three).
- **Prompt.** This is the gap. Motion has no prompt layer. No email cadence, no push, no SMS, no calendar invite. Intent Engine fires only on open. A coach who forgets to open Monday morning receives no nudge Monday afternoon.

The diagnosis: Motion is prompt-starved. Building the prompt layer is the highest-leverage retention investment available, and it must be built in Motion's register — declarative, cited, non-promotional. No growth-hack copy. No exclamation marks. No urgency confected from a cron job.

### 1.3 Motion's Six Behavioural Pillars

The Broadwalk framework uses six pillars. Motion adapts each to coaching.

1. **Ritual and cadence.** Practice streak, film-study ritual, pre-game brief. Absence does not punish — cadence earns the open. Streaks shown as professorial ("twelve practices read") not arcade ("12-day streak fire emoji").
2. **Personalised read.** The morning practice read, the pre-game brief, the post-game debrief. Assembled from signals, cited to the wiki, delivered as prose.
3. **Cohort signal.** Other coaches at your level who read the same set-play page this week. Anonymised. Federated. Never names, never schools. IP and privacy constraints forbid anything less abstract.
4. **Time decay.** Game-clock is the scarcity. Scouting half-life. Lineup freshness. Opponent-tape stale flag. Never invented urgency — only real decay.
5. **Mastery and coverage.** Archetype convergence for the player. Wiki coverage for the student. Roster completeness for the coach. Progress is professorial: you have read 34 of 112 pages on defensive principles.
6. **Ambient surfacing.** The instrument shows what you did not ask for. A cross-link from tonight's set-play to a counter three chapters later in *Coaches Playbook*. This is Motion's native aesthetic and the pillar that most differentiates it.

Each feature in this document maps to one or two pillars. No feature maps to none.

---

## Part 2 — Game Plan Generator Deep-Dive

### 2.1 Current state

The Game Plan Generator is Motion's primary retention surface — the coach-side analogue of Broadwalk's Intelligence Wall. It is specced, not built. The current Coach landing page degrades to a schedule-absent default. That is correct. Schedule-absent users are the majority through Phase 1.

| Area | Strength | Gap |
|---|---|---|
| Intent resolution | Five intents cover coach states well; schedule + roster + season-phase triad is sound | Intents do not yet bind to a persistent Game-Readiness score; every open is stateless |
| Content density | Wiki compilation of 1,035 pages is the foundation; citations always available | Citations render as footers; no surfaced "why this answer" layer above the fold |
| Composition | 14 atoms, 7 components — architecture supports every surface proposed below | Atoms do not yet expose a "last-seen" timestamp, which blocks decay-aware surfacing |
| Flow | Open-to-answer is under 2 seconds when signals are present | Open-to-answer degrades to the schedule-import wall when they are not; the wall reads as admin, not instrument |

### 2.2 Six proposed features

#### `GP-01` Tonight's Read

**Pillar.** Personalised read; ritual and cadence.

The Game Plan Generator opens to a single composed paragraph — 120 to 180 words — stating what the coach should run tonight, why, and what to watch for. It is not a list of plays. It is prose, cited. The paragraph composes from the intent engine's output and pulls one ranked set-play, one defensive coverage, and one halftime contingency. Example register: "Against a 2-3 zone front with one mobile top, Horns-flare with the weak-side pin hits at 0.98 points per possession in the *Coaches Playbook* sample (p. 142). Run it on the second possession, not the first. Your second-unit has the spacing for it; your starters do not."

- Assembly: existing 7-component system; new component `tonightsRead` composes three atoms in paragraph form.
- Citation: every claim ends with `[source, page]` using the seven approved volumes verbatim.
- Fallback: schedule-absent users see the Morning Practice Read instead (see `GP-02`).
- No buttons above the fold. The paragraph is the answer.

#### `GP-02` Morning Practice Read

**Pillar.** Personalised read; ritual and cadence.

Fires on practice days before 9:00 local. Composes the day's practice intent from roster signal (who practiced well last session), body-lab signal (who is flagged for reduced load), and season phase (installation week vs tune-up week). One paragraph, one citation block, one drill progression link. Ships as in-app component first, email second (see Part 4).

- Signal weighting: recent-activity > season-phase > schedule.
- Component reuses `tonightsRead` composer.
- Never references drills the coach has not yet added to their practice library.

#### `GP-03` Scouting Half-Life

**Pillar.** Time decay.

Opponent intel decays. Motion shows the decay, does not hide it. Every scouting artefact carries a freshness bar — not a countdown, a state. "Drawn from footage logged 11 days ago. Still valid for personnel tendencies. Stale for lineup rotations." The coach understands that the intel is aging without being pressured.

- Three states only: fresh (0-3 days), current (4-10 days), stale (11+ days).
- State is shown as a hairline kicker above the artefact, mono type, uppercase.
- Refresh is an explicit action the coach takes; Motion never auto-marks stale artefacts as fresh.

#### `GP-04` Coverage Map

**Pillar.** Mastery and coverage.

Across a season, what a coach has installed — sets, coverages, press breaks, out-of-bounds — is tracked against the wiki's canonical taxonomy. The coverage map shows what is installed, what is partial, what is untouched. No score. No percentage badge. A simple inventory, professorially framed: "Of 22 canonical out-of-bounds sets catalogued in *NBA Playbook*, you have installed 6. Four more are within your roster's archetype profile."

- No gamification. No green checkmarks. No levels.
- Archetype profile is computed from the eight Motion archetypes, never from external player comparisons.
- Renders as a single-column list, not a grid.

#### `GP-05` Annotated Season Log

**Pillar.** Investment; ambient surfacing.

Every game plan delivered, every halftime chip fired, every practice read logged — timestamped, searchable, annotated by the coach. The investment column of the Hook Model: the more the coach logs, the more their own season writes itself into the instrument. The log surfaces patterns: "You have run Horns-flare five times this season. Points per possession: 1.04. Best: game 4 vs a 2-3. Worst: game 9 vs a man-up denial." Never a leaderboard. Never a rank.

- Log entries are prose, not rows.
- The coach can attach one film clip per entry. No auto-attached video.
- Patterns surface only when n ≥ 3 instances; below that, the log is silent.

#### `GP-06` The One Question

**Pillar.** Ambient surfacing.

At the bottom of Tonight's Read, Motion surfaces one question the coach has not asked. Cited. Pulled from a wiki cross-link the assembly system detected but did not place above the fold. "You have not yet read the counter to Horns-flare when the defence switches 1-5. *Coaches Playbook* covers it on p. 198." This is the product's native move — the next right thing you did not ask for.

- One question per open. Never two.
- Dismissible without penalty. Dismissals feed the signal set.
- Never phrased as a rhetorical question. Always a declarative "you have not yet read."

---

## Part 3 — Cross-Module Enhancements

### 3.1 Halftime

`HT-01` **Pre-loaded Halftime Chips.** Pillar: personalised read, time decay. By the time the coach reaches the locker room, three chips are already assembled — one offensive adjustment, one defensive coverage change, one rotation suggestion. Composed from first-half signals. Each chip is under 20 words, cited. No "AI suggests" framing; Motion simply presents.

`HT-02` **Two-Minute Read.** Pillar: ritual. A 90-second locker-room read, 160 words maximum, assembled from the first-half log. Designed to be read aloud once. Prose, not bullets.

`HT-03` **Post-Game Debrief Seed.** Pillar: investment. Before the coach leaves the arena, a single paragraph seeds the debrief — what changed at halftime, what the adjustment yielded, what to queue for tomorrow's film. Written for the coach's own later annotation.

### 3.2 Practice Planner

`PP-01` **Practice Streak, Professorial Frame.** Pillar: ritual and cadence. "Eleven practices read" is shown, not "11-day streak." Absence does not reset to zero. The number is a count, not a currency. No shields, no freezes, no arcade language.

`PP-02` **Drill Progression Trail.** Pillar: mastery and coverage. Each drill links forward to its canonical progression from *Skills & Drills* (239 pp.) and *Offensive Skills* (200 pp.). The coach sees where the drill sits in a longer arc — installation, refinement, live application — and where tonight's practice fits.

`PP-03` **Body-Lab Load Flag.** Pillar: ambient surfacing. When a player's body-lab signal indicates reduced load, the practice read surfaces an alternative drill, cited to *Basketball Anatomy* (200 pp.). Never a warning banner. A note in the margin.

### 3.3 Play Viewer

`PV-01` **Counter Link.** Pillar: ambient surfacing. Every play shown links to its canonical counter — the defensive read that breaks it, the offensive adjustment that restores it. One link per play, never a menu. The counter opens in the same viewer, animated via the SVG pipeline.

`PV-02` **Play Freshness Trace.** Pillar: time decay. If the coach last viewed a play more than 30 days ago, a hairline note under the play name reads "last read [date]." No action required, no penalty. A trace of their own engagement.

`PV-03` **Archetype Fit.** Pillar: mastery and coverage. Each play carries a short line: "Fits Floor General and Sharpshooter archetypes. Weak fit for Paint Beast." Uses Motion's eight archetypes only. No external player comparisons under any circumstance.

### 3.4 Player Experience

`PL-01` **The Tonight List.** Pillar: personalised read. Player opens the app; they see only what belongs to them tonight — two plays they are in, one drill flagged by the body-lab, one line from their archetype profile. No roster view. No coach's plan. No distraction.

`PL-02` **Archetype Convergence Trail.** Pillar: mastery and coverage. Over weeks, the player's archetype profile sharpens. The trail shows the convergence — the traits that have strengthened, the ones still diffuse. Framed as a reading, not a score. No badges. No level-ups.

`PL-03` **Drill Streak.** Pillar: ritual. A professorial count of drills completed. Ritual framing: "you have run the same shooting progression twelve practices running." Never "streak," never "days," never "don't break the chain."

### 3.5 Student of the Game / Knowledge Search

`ST-01` **The Socratic Drill.** Pillar: ambient surfacing. Once per session, the wiki offers one question it thinks the student has not considered. Cited. Answerable by reading 3-5 paragraphs. Never multiple choice. Never scored.

`ST-02` **Wiki Coverage Reading.** Pillar: mastery and coverage. Which chapters of the seven books the student has read, which they have touched, which remain. A reading list, not a progress bar. "You have read 34 of 112 pages on defensive principles. The unread 78 include three that cross-link to the last play you viewed."

`ST-03` **Breaking Tactical Theme.** Pillar: ambient surfacing. A single theme banner — one per week, not one per open — surfaced when the wiki's cross-link graph detects a cluster the student has engaged. "You have read six pages this week on zone offence. A cluster you have not opened: middle-of-the-zone attacks, *NBA Playbook* pp. 412-438." Never a push notification. Surfaces only on open.

---

## Part 4 — Re-Engagement Architecture

### 4.1 Trigger matrix

Motion's prompts respect three constraints: GDPR consent, under-16 parental consent for player accounts, and the voice rules. Every prompt is declarative, cited, and never urgent without real decay.

| Trigger condition | Time lag | Channel | Message type | Register |
|---|---|---|---|---|
| Practice day, no open by 09:00 local | 0 h | Email (opt-in) | Morning Practice Read | Declarative; one paragraph; one citation |
| Game day T-4 h, schedule loaded | 0 h | Email + one push | Pre-Game Brief | Declarative; cite wiki; three chips |
| Scouting artefact ≥ 11 days old | 24 h after state flip | Email | Scouting Half-Life note | "Drawn from footage logged 11 days ago. Still valid for X. Stale for Y." |
| Player flagged by body-lab, no player open in 72 h | 72 h | Push (opt-in, under-16 parental consent required) | Load-adjusted drill | "The body-lab has adjusted tonight's drill. The read is two minutes." |
| Student wiki coverage cluster detected | Weekly, Sunday 08:00 | Email | Breaking Tactical Theme | One theme; one citation block; no call to action |
| Season phase transition (install → tune-up → playoff) | 0 h at transition | Email | Phase Read | "Your season has moved from installation to tune-up. The read has changed." |

No trigger fires on a pure time-based cron. Every trigger binds to a signal. Absence of signal means absence of prompt. Motion never nudges for nudge's sake.

### 4.2 Editorial programme — The Coaching Read

Three editions per week. Each short. Each cited. Each written to be read in under 90 seconds.

- **Monday — The Practice Read.** One drill progression, one concept page from the wiki, one question to carry into the week.
- **Wednesday — The Film Note.** One tactical pattern observed across the coach's recent logs, cited to one of the seven books. Never generic.
- **Friday — The Week's Cross-Link.** One cross-link the ambient engine surfaced, framed as a reading for the weekend.

**Subject-line formula.** `[Specific signal] + [Specific change] + [Implied tactical consequence]`. Examples:

- "Weak-side pin, install complete. Counter unread."
- "Horns-flare run five times. PPP trending down."
- "Zone coverage, mobile top. *Coaches Playbook* p. 142."

No exclamation marks. No "you won't believe." No "urgent." No emoji.

### 4.3 Mode-specific cadence

Coach, player, and student receive different programmes. The same signal can fire three different reads.

- **Coach.** Three emails per week. One push on game day T-4 h. No push on practice day; the email is the prompt.
- **Player.** One email per week (Sunday evening). One push per practice day at a time the player chose during onboarding. Under-16 accounts: parental email mirrors every player email; push disabled by default.
- **Student.** One email per week (Friday). No push. Student cadence is curiosity-led; pushing breaks the register.

---

## Part 5 — Prioritised Roadmap

Eighteen features. Three phases. Priority P0-P3. All feature IDs as introduced above.

| ID | Module | Name | Pillar | Priority | Phase |
|---|---|---|---|---|---|
| `GP-01` | Game Plan Generator | Tonight's Read | Personalised read; ritual | P0 | 1 |
| `GP-02` | Game Plan Generator | Morning Practice Read | Personalised read; ritual | P0 | 1 |
| `GP-03` | Game Plan Generator | Scouting Half-Life | Time decay | P1 | 2 |
| `GP-04` | Game Plan Generator | Coverage Map | Mastery and coverage | P1 | 2 |
| `GP-05` | Game Plan Generator | Annotated Season Log | Investment; ambient | P2 | 3 |
| `GP-06` | Game Plan Generator | The One Question | Ambient surfacing | P0 | 1 |
| `HT-01` | Halftime | Pre-loaded Halftime Chips | Personalised read; time decay | P0 | 1 |
| `HT-02` | Halftime | Two-Minute Read | Ritual | P1 | 2 |
| `HT-03` | Halftime | Post-Game Debrief Seed | Investment | P2 | 3 |
| `PP-01` | Practice Planner | Practice Streak, Professorial | Ritual | P1 | 2 |
| `PP-02` | Practice Planner | Drill Progression Trail | Mastery and coverage | P1 | 2 |
| `PP-03` | Practice Planner | Body-Lab Load Flag | Ambient surfacing | P2 | 2 |
| `PV-01` | Play Viewer | Counter Link | Ambient surfacing | P0 | 1 |
| `PV-02` | Play Viewer | Play Freshness Trace | Time decay | P2 | 3 |
| `PV-03` | Play Viewer | Archetype Fit | Mastery and coverage | P1 | 2 |
| `PL-01` | Player Experience | The Tonight List | Personalised read | P0 | 1 |
| `PL-02` | Player Experience | Archetype Convergence Trail | Mastery and coverage | P1 | 2 |
| `PL-03` | Player Experience | Drill Streak, Professorial | Ritual | P2 | 3 |
| `ST-01` | Student / Wiki | The Socratic Drill | Ambient surfacing | P1 | 2 |
| `ST-02` | Student / Wiki | Wiki Coverage Reading | Mastery and coverage | P2 | 3 |
| `ST-03` | Student / Wiki | Breaking Tactical Theme | Ambient surfacing | P2 | 3 |

Count: 21 features listed — the six `GP` entries plus fifteen cross-module. P0 items form the Phase-1 spine.

---

## Part 6 — Spec Template Recommendations

Every Motion feature PRD should carry four blocks not found in the current template.

### 6.1 Behavioural Intent block

Four fields. Ten words maximum per field.

```
Behavioural Intent:   [What the feature earns — never what it promotes.]
Target Emotion:       [The one emotion it should produce. Usually calm or recognition.]
Retention Metric:     [Which D7/D30/sessions metric this moves.]
Hook Phase:           [Trigger | Action | Variable Reward | Investment]
```

### 6.2 Magic Moment

One per module. Written as a single declarative sentence. Examples:

- Game Plan Generator: "The paragraph is already written when the coach opens the app."
- Halftime: "Three chips are on the screen before the coach sits down."
- Play Viewer: "The counter to the play you just watched is one tap away."
- Player: "Only what belongs to the player tonight, nothing else."
- Student: "The question you had not yet thought to ask."

### 6.3 Notification Architecture

Every notification specified in a PRD must declare:

| Field | Required value |
|---|---|
| Trigger type | Signal-bound; never cron-only |
| Channel | Email, push, in-app. Under-16 push requires parental consent flag |
| Frequency cap | Absolute weekly max; never daily-push for coaches |
| Emotional framing | Declarative, cited, non-promotional |
| Opt-out path | One tap. Reversible. No dark pattern |
| GDPR base | Legitimate interest or explicit consent — specified at spec time |

### 6.4 Citation requirement

Every feature that surfaces wiki content must specify: which of the seven books it draws from, which chapter range, and how the `[source, page]` footer renders in the UI. Citations are not optional. The product's promise — every answer traces back to a page you can read — is a specification constraint, not a marketing line.

---

## Part 7 — Implementation Guidance and Success Metrics

### 7.1 Three-phase build

**Phase 1 — Ritual spine (Sprints 1-4, eight weeks).** Ship P0 features: `GP-01`, `GP-02`, `GP-06`, `HT-01`, `PV-01`, `PL-01`. Ship the Coaching Read email programme skeleton (Monday edition only). Goal: earn first-open status on practice day and game day. Measure against Phase-1 targets below.

**Phase 2 — Cadence and coverage (Sprints 5-8, eight weeks).** Ship P1 features: `GP-03`, `GP-04`, `HT-02`, `PP-01`, `PP-02`, `PV-03`, `PL-02`, `ST-01`. Expand email programme to three editions per week. Introduce the archetype convergence trail for players. Goal: extend Phase-1 gains from peak-days (Mon, game-day) to the rest of the week.

**Phase 3 — Investment and ambient depth (Sprints 9-12, eight weeks).** Ship P2 features: `GP-05`, `HT-03`, `PP-03`, `PV-02`, `PL-03`, `ST-02`, `ST-03`. Enable post-game debrief. Deepen the cross-link graph. Goal: turn short-term cadence into a compounding investment column — each coach's instrument is visibly denser at week 12 than at week 1.

Schedule-absent users remain a first-class state through all three phases. Every feature listed degrades cleanly when signals are missing. The Morning Practice Read is the universal fallback.

### 7.2 Success metrics

Current baseline figures are from the most recent three weeks of landing and play-viewer analytics (confidence: MEDIUM — sample is small, coach segment under 200 weekly actives). Post-Phase-1 targets assume the P0 shipping list lands on schedule.

| Metric | Definition | Baseline (3-wk trailing) | Phase-1 target | Phase-3 target |
|---|---|---|---|---|
| Coach D7 retention | Share of new coach signups active day 7 | 31% | 48% | 62% |
| Coach D30 retention | Share active day 30 | 14% | 28% | 42% |
| Sessions per coach per week | Distinct opens, peak weeks | 2.1 | 3.5 | 4.8 |
| Primary-surface open rate | Coach opens where Game Plan Generator is first surface | — (not yet shipped) | 70% | 85% |
| Practice streak penetration | Coaches with three or more consecutive practice-day opens | — | 35% | 55% |
| Player D7 | Share active day 7 | 38% | 52% | 65% |
| Player drill-completion rate | Drills marked complete per flagged drill | 42% | 58% | 70% |
| Student wiki session length | Median minutes per wiki session | 3.4 | 4.2 | 5.5 |
| Email open rate (Coaching Read) | Across three editions | — | 38% | 45% |
| Citation inspection rate | Share of answers where the coach clicks to read the cited page | — | 22% | 35% |

Citation inspection rate is the metric most specific to Motion. No comparable product has a good number here. It measures whether the "every answer traces back to a page" promise is real to users or rhetorical.

### 7.3 What not to measure

Motion should not track streak-break recovery, re-engagement after lapse via discount, or notification click-through in isolation. These metrics encourage the arcade register the product has already rejected twice. Streak-break is a non-metric: the streak is a count, not a currency.

---

## Closing

The retention unit for a coaching instrument is the ritualised open. Practice morning. Game-day T-4. Halftime. Sunday evening film. The instrument that is on the bench before the whistle does not need to beg for attention.

Motion has the intelligence density. Seven books, 2,440 pages, compiled into a cited wiki. The architecture — eight signals, five intents, 14 atoms, seven components — is the right shape for a product whose promise is that the next right move is already on the screen. The gap is the prompt layer, the ritualisation layer, and the investment column. All three are buildable in twelve weeks.

> The coach who opens Motion before the bus leaves never browses. They read.
