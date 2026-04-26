---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [offense, analytics, NBA, statistics, team-evaluation]
source_count: 1
last_updated: 2026-04-11
---

# Offensive Rating — NBA Historical Analysis

## Summary
Offensive rating measures a team's scoring efficiency as **points scored per 100 possessions**. Because it controls for pace (possessions per game), it is a more accurate measure of offensive quality than raw points per game. Dean Oliver compiled the top 25 NBA offenses since 1974 and analyzed what separated elite offenses from average ones [S16, pp.43-46].

The raw offensive rating list (Table 3.2/3.6 in the source) is dominated by 1990s and 2000s teams, partly because the standard deviation of offensive ratings was higher in that era — meaning teams diverged more from the mean. To correct for this era effect, Oliver normalized ratings by dividing each team's increment above average by the season's standard deviation of all team offensive ratings, producing a "standard deviations above average" metric [S16, p.44].

## When to Use
- Evaluating whether a team's offense is elite, average, or poor relative to its era
- Comparing teams across different decades when pace and league scoring averages differ
- Identifying whether an offense is built for efficiency or volume
- Scouting reports: identifying opponents above/below league average offensive efficiency

## Key Principles
1. **Points per 100 possessions, not per game** — removes pace bias; a fast team can score 115 points per game but be below average efficiency [S16, p.44]
2. **Standard deviation normalization for cross-era comparisons** — dividing increment above average by the season's SD corrects for talent dilution and era differences [S16, p.44]
3. **Height helps offense** — the top 25 offenses were on average slightly taller than the league average, but by less than 1 inch [S16, p.43, Table 3.6]
4. **Stars matter for offense** — the top 25 offenses had more All-NBA players (20 First Team, 11 Second Team, 7 Third Team) than the top 25 defenses, suggesting individual talent drives offense more than systems [S16, p.50]
5. **Roster stability matters** — the worst offenses historically had roster stability under 75%, meaning 2–3 of 5 floor positions completely turned over year-to-year [S16, p.59]

## Top 25 Historical Offenses (Standard Deviations above Average)
From Table 3.7 [S16, pp.45]:

| Rank | Team | Season | Off Rating | Std Dev above Avg | Key Players |
|------|------|--------|------------|-------------------|--------------|
| 1 | Denver Nuggets | 1982 | 114.3 | +2.65 | Alex English, Dan Issel, Kiki Vandeweghe |
| 2 | Chicago Bulls | 1997 | 114.4 | +2.32 | Jordan, Pippen, Kukoc, Rodman |
| 3 | Dallas Mavericks | 2002 | 112.2 | +2.25 | Dirk Nowitzki, Steve Nash, Michael Finley |
| 4 | Utah Jazz | 1997 | 113.6 | +2.11 | Karl Malone, John Stockton, Jeff Hornacek |
| 5 | Chicago Bulls | 1992 | 115.5 | +2.00 | Jordan, Pippen, Horace Grant, B.J. Armstrong |
| 6 | Philadelphia 76ers | 1978 | 106.3 | +1.98 | Julius Erving, George McGinnis, Doug Collins |
| 7 | Chicago Bulls | 1996 | 115.2 | +1.98 | Jordan, Pippen, Kukoc, Rodman |
| 8 | Los Angeles Lakers | 1987 | 115.6 | +1.95 | Magic Johnson, James Worthy, Kareem |

*The 1982 Denver Nuggets rank #1 by standard deviations because the SD of offensive ratings was only 2.83 that season, making their +7.5 increment even more remarkable.* [S16, p.44]

## Coaching Patterns
Multiple coaches appear with different teams, suggesting defensive systems are portable:
- Phil Jackson: Chicago Bulls (multiple years) + LA Lakers
- Pat Riley: NY Knicks (defense) + Miami Heat
For offense, star players appear to be the primary driver [S16, p.52]

## Era Effects
Standard deviations of offensive (and defensive) ratings were **relatively higher in the 1990s**, meaning teams diverged more from average. This may reflect talent dilution from expansion, or strategic evolution [S16, p.44, Figure 3.2]. The standard deviation was ~2.2 in 1978 vs. ~3.9 in 1998.

## Common Mistakes in Interpreting Offensive Ratings
1. **Using points per game instead of per possession** → always convert to per-100-possession rates when comparing across eras or pace styles
2. **Ignoring era context** → a +5.0 increment in 1978 may equal a +7.5 increment in 1998 in terms of true dominance
3. **Confusing pace with efficiency** → fast teams score more per game but aren't necessarily more efficient [S16, p.52]

## Related Concepts
- [[concept-defensive-rating-historical-trends]] — the complementary defensive efficiency metric
- [[concept-pace-of-play]] — how possessions per game relates to efficiency
- [[concept-roster-stability]] — why continuity predicts offensive performance
- [[concept-four-factors-basketball]] — the four key drivers of offensive efficiency

## Sources
- [S16, pp.43-46] — Top 25 offenses raw and standard-deviation normalized rankings, Tables 3.6 and 3.7
- [S16, p.44, Figure 3.2] — Standard deviation of team offensive and defensive ratings over time
- [S16, p.50] — Stars vs. systems analysis comparing All-NBA representation on top offenses vs. defenses
