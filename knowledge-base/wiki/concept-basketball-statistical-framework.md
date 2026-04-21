---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [analytics, statistics, offense, defense, team-evaluation, player-evaluation, possessions]
source_count: 1
last_updated: 2026-04-11
---

# Basketball Statistical Framework (Oliver's Possession-Based System)

## Summary
Dean Oliver's *Basketball on Paper* (2004) establishes a complete possession-based statistical framework for evaluating basketball performance. The framework's central insight is that **a possession is the fundamental unit of basketball** — every offensive sequence ends in a made or missed shot, a turnover, or free throws, and the goal of offense is to score as many points as possible per possession while defense aims to allow as few as possible.

The framework was originally developed in 1987 and refined through work with the Seattle Supersonics and Charlotte Sting. It ties together all traditional box-score statistics — field goals, free throws, rebounds, assists, turnovers, steals, blocks — into a single coherent system that can evaluate teams and individual players on the same scale: **points per 100 possessions**.

This was the first systematic application of sabermetric thinking (pioneered by Bill James for baseball) to basketball [S16, p.1].

## When to Use
- Building a player evaluation system from box-score data
- Comparing players across eras, leagues, or pace environments
- Identifying which team statistics most predict winning
- Making lineup decisions with statistical support
- Scouting opponents through efficiency tendencies

## Key Principles
1. **Possessions as denominator.** All efficiency calculations divide by possessions, not minutes or games. Possession estimate: `FGA − OREB + TOV + (0.44 × FTA)` [S16, Appendix 1].
2. **Points per 100 possessions (ORtg/DRtg).** The single number that best describes offensive or defensive quality, independent of pace.
3. **Four Factors of winning.** Oliver identified four team statistics most predictive of ORtg/DRtg: (1) shooting efficiency (EffFG%), (2) turnover rate (TOV%), (3) offensive rebounding rate (OR%), and (4) free throw rate (FT/FGA). See [[concept-four-factors-winning]].
4. **Floor percentage.** The fraction of an individual's possessions that end in a score. `Floor% = Scoring Possessions / Possessions`. Combined with efficiency per scoring possession, this produces individual ORtg.
5. **Individual ratings from team context.** Individual ORtg is not measured directly — it is calculated by allocating team scoring credit based on each player's share of possessions used and their efficiency contribution.
6. **Defensive ratings require estimation.** Box scores do not directly capture defensive responsibility. Oliver developed approximation formulas using opponent FG%, blocks, steals, and defensive rebounds [S16, Appendix 3].
7. **Teamwork and credit distribution.** Assists, screens, and spacing create value not fully captured by traditional stats. Chapters 5, 10, and 13 address distributing credit in team contexts.

## Core Abbreviations / Vocabulary
Oliver's notation system, used throughout the book:
- **ORtg**: Individual or team offensive rating (pts produced per 100 possessions)
- **DRtg**: Individual or team defensive rating (pts allowed per 100 possessions)
- **Floor%**: Scoring possessions divided by possessions
- **EffFG%**: Effective field goal percentage = (FGM + 0.5 × FG3M) / FGA
- **OR%**: Team offensive rebounding percentage
- **TOV%**: Turnovers per possession
- **Play%**: Plays (possessions used) as share of team plays
- **Stop%**: Stops (defensive possessions successfully ended) per individual defensive possession
- **PtsPerScPoss**: Points produced per scoring possession (efficiency on made plays)

(For the full 60+ abbreviation list, see [S16, pp.xi-xvi])

## Player Responsibilities
The framework applies to all five positions equally — it does not privilege scorers over defenders or big men over guards. A player who never scores but consistently produces stops and grabs defensive rebounds will show a favorable DRtg and contribute positively to team efficiency differential.

## Variations
### Team-Level Application
At the team level, ORtg and DRtg can be calculated directly and exactly from box scores. Their differential predicts winning percentage with high accuracy [S16, Ch.4].

### Individual Application
Individual ORtg requires the full formula in Appendix 1, which accounts for a player's FGA, FTA, OREB, AST, and TOV in the context of team efficiency [S16, Ch.14].

### Historical Application
Appendix 2 provides individual offensive ratings for the greatest offenses in NBA history, enabling cross-era comparisons [S16, Appendix 2].

## Common Mistakes
1. **Treating ORtg as raw scoring ability** → ORtg credits playmaking, offensive rebounding, and drawing fouls, not just shooting.
2. **Ignoring sample size** → Individual ratings over small minute samples are noisy; 500+ possessions are needed for meaningful estimates.
3. **Using PPG instead of ORtg** → Points per game conflates volume with efficiency and is biased by pace.
4. **Neglecting DRtg** → The best analytical player evaluation systems are bidirectional; offense-only metrics systematically overrate volume scorers.

## Related Concepts
- [[concept-points-per-possession]] — the core metric of the framework
- [[concept-individual-offensive-rating]] — individual ORtg calculation
- [[concept-individual-defensive-rating]] — individual DRtg estimation
- [[concept-floor-percentage]] — the intermediate metric linking usage to efficiency
- [[concept-four-factors-winning]] — the four controllable drivers of team efficiency
- [[concept-performance-rating-system]] — an alternative weighted scoring system [S13]

## Sources
- [S16, pp.1-7] — framework overview, intended audiences, philosophical foundation
- [S16, pp.xi-xvi] — complete abbreviation/notation system
- [S16, Ch.2] — offensive score sheets as the original data collection method
- [S16, Ch.14] — full individual offensive rating formulas
- [S16, Appendix 1] — calculation details
