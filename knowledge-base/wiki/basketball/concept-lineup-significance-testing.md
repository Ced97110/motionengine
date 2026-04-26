---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [analytics, player-evaluation, statistics, defense, lineup-analysis]
source_count: 1
last_updated: 2026-04-11
---

# Lineup Significance Testing

## Summary
Significance testing is a statistical tool for determining whether observed differences in a team's performance with and without a specific player are real effects or simply random variation. Applied to basketball, it answers: "When our record was better without Player X, was that meaningful or just a fluke?"

Dean Oliver applies this framework to the famous Derrick Coleman case (Charlotte Hornets 1999–2001), where the Hornets went 74-80 with Coleman and 54-20 without him — a difference so extreme that significance testing calculated only a 0.02% chance it was due to luck. Oliver then drills down into the Four Factors to identify *why* Coleman's presence hurt the team: defensive field goal percentage was significantly higher with him in the lineup [S16, Ch.7].

## When to Use
- Evaluating player acquisitions and roster decisions
- Investigating an unexplained win-loss split
- Identifying whether lineup changes produce real improvement
- Analyzing injury absences to gauge player impact

## Key Principles
1. **Statistical significance threshold**: If the significance test returns > 5%, treat the difference as likely due to luck. Below 5% means something real is probably occurring [S16, p.94]
2. **Sample size matters**: Small samples (8 games) can show large win-loss differences that are still statistically insignificant [S16, p.95]
3. **Isolate offense and defense separately**: A player may hurt defense without affecting offense, or vice versa — test both ratings independently [S16, p.94]
4. **Account for the replacement player**: The split reflects the player AND whoever replaced him — if the replacement is clearly better, the split is unsurprising [S16, p.94]
5. **Then drill into the Four Factors**: Identify which of the four factors (FG%, OREB, TOV, FTA) explains the offensive/defensive rating change [S16, pp.96-97]
6. **Individual defense is poorly documented** — lineup splits are one of the best available tools for tracking defensive contributions [S16, p.97]

## The Coleman Case Study (1999–2001)

| Season | With Coleman | Without Coleman | Primary Replacements |
|--------|-------------|-----------------|----------------------|
| 1999 | 15-22 | 11-2* | Brown, Miller, Reid, Shackleford |
| 2000 | 44-34 | 6-2 | Brown, Miller, Robinson, Fuller |
| 2001 | 15-24 | 37-16* | Magloire + increased starter mins |
| **Total** | **74-80** | **54-20*** | — |

*Statistically significant at 5% level*

**Charlotte's Four Factors with/without Coleman:**
- Defensive FG% (2PT): 0.457 with DC vs. 0.440 without (*sig: 0.02*)
- Defensive FG% (3PT): 0.367 with DC vs. 0.337 without (sig: 0.09)
- Opponent OREB%: 0.274 with DC vs. 0.261 without (sig: 0.10)
- Defensive TOV rate: no meaningful difference
- Opponent FTA rate: no meaningful difference

*Conclusion: Coleman's negative impact was almost entirely on defensive FG% — opponents shot significantly better inside the arc when he played* [S16, pp.97]

## Other Case Studies

### Michael Jordan, Washington 2002
- With: 30-30 | Without: 7-15 (sig: 7%)
- Key effect: **Defense** — Wizards allowed 102.6 pts/100 with Jordan, 106.9 without (sig: 5%)
- Most significant mechanism: Jordan reduced opponent FTA (team fouled 20.6x/game with him vs. 23.9 without) [S16, p.98]

### Steve Francis, Houston 2002
- With: 26-31 | Without: 2-21
- Key effect: **Offense** — offensive rating 102.6 with Francis, 98.7 without
- Straightforward: Francis was a known shot-creator; his replacements (Torres, T. Brown, Norris) were not [S16, p.98]

### Ron Artest, Chicago-Indiana 2002
- Chicago: defensive rating 102.0 with / 107.7 without (significant)
- Indiana: only 102.6 to 100.9 with Artest (insignificant)
- Lesson: Mixed evidence — strong Chicago results partly confounded by replacement quality [S16, pp.98-99]

### Dikembe Mutombo, Atlanta-Philadelphia 2001
- Atlanta: defensive rating 100.5 with Mutombo vs. 110.0 without (highly significant)
- Tradeoff: Offense was significantly worse with Mutombo, but only by 3 pts vs. 10 pts gained defensively [S16, p.99]

### Shaquille O'Neal, Los Angeles 2000–2002
- With: .768 win% | Without: 13-13
- Key effect: **Offense** — 109.1 → 103.9 without him; defense nearly unchanged [S16, p.100]

### Allen Iverson, Philadelphia 2000–2002
- With: 62% win% | Without: 48%
- Key effect: **Offense** — 103.7 → 98.2 without Iverson; defense barely changed (101.0 → 100.4)
- Most significant factors with Iverson: more FTA and more 3PT makes [S16, p.100]

## The Technical Method
Test used: **Two-sample unequal variance student t-test** (one-tailed or two-tailed depending on situation)
- Excel: `TTEST(Array1, Array2, Tails, Type)` with `Tails=1 or 2`, `Type=3`
- Apply to: offensive rating, defensive rating, and each of the Four Factors separately [S16, p.100]

## Common Mistakes
1. **Declaring significance from small samples** → 6-2 in 8 games sounds impressive but is not statistically significant at 5% [S16, p.95]
2. **Attributing split entirely to the absent player** → The split always reflects the absent player AND the replacement
3. **Stopping at wins/losses** → The useful finding comes from decomposing into offensive/defensive ratings, then into Four Factors
4. **Ignoring schedule effects** → The Bowen/Spurs case showed part of the apparent effect was due to opponent quality during his absence [S16, p.99]

## Related Concepts
- [[concept-four-factors]] — the framework used to explain WHY lineup splits occur
- [[concept-player-rating-systems-comparison]] — alternative approaches to player evaluation
- [[concept-rebounding-myths-roles]] — how rebounding fits into the analytical framework

## Sources
- [S16, pp.93-100] — Chapter 7: "The Significance of Derrick Coleman's Insignificance" — complete case studies with data tables
