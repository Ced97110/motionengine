---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [analytics, statistics, offensive-rating, defensive-rating, garbage-time, historical-analysis]
source_count: 1
last_updated: 2026-04-11
---

# Uncorrelated Ratings

## Summary
When good teams build large leads, they substitute bench players and play conservatively — "garbage time." This causes the leading team's offensive and defensive statistics to look *worse* than they really are (more bad shots, letting opponents score) while the losing team's statistics look *better*. The covariance term in the [[concept-basketball-bell-curve-model]] formula captures this effect: a positive correlation between PPG and DPPG indicates a team plays up/down to opponents.

**Uncorrelated ratings** mathematically remove that covariance while preserving the team's win total, revealing what a team's offensive and defensive ratings *would* have been if they competed at full intensity every minute of every game. They are a better predictor of playoff performance than standard ratings because teams apply themselves fully in the playoffs [S16, pp.138-142].

## When to Use
- Comparing historical teams on equal footing
- Predicting playoff success from regular-season data
- Identifying "slack-off" teams vs. "no-quit" teams
- Evaluating whether a great regular-season team will underperform in the playoffs

## Key Principles
1. **Good teams have more garbage time.** Better teams build bigger leads more often, creating more minutes where they coast — so uncorrelated ratings help good teams more than bad ones [S16, p.139].
2. **Uncorrelated ratings reward intensity.** Teams that compete hard every minute (no give-up possessions) already have low correlation; their standard and uncorrelated ratings are nearly the same.
3. **The adjustment is usually modest.** Shuffling happens in the middle of historical rankings; the top and bottom are relatively stable. The top 25 offenses and defenses retain mostly the same members [S16, pp.139-140].
4. **Playoffs as the true test.** Because teams apply full effort in postseason, uncorrelated ratings predict playoff series winners better than standard ratings (63% vs. 62% for offense; 59% vs. 57% for defense) [S16, p.142].

## Historical Impact — Top Offenses
Using uncorrelated ratings changes the top-5 offensive ranking significantly [S16, Table 12.2, p.139]:

| Team | Season | Standard ORtg Rank | Uncorrelated Rank |
|---|---|---|---|
| Chicago Bulls | 1997 | 2 | **1** |
| Utah Jazz | 1998 | 3 | **2** |
| Chicago Bulls | 1996 | 4 | **3** |
| Utah Jazz | 1997 | 9 | **4** |
| Chicago Bulls | 1992 | 6 | **5** |
| Dallas Mavericks | 2002 | 1 | 6 |

Notable entrant: **1986 Boston Celtics** (67–15) — didn't appear on standard top-25 offense list but **jumps to #24 offense and #10 defense** after uncorrelated adjustment [S16, p.140].

## Historical Impact — Top Defenses
Major changes in top-25 defenses [S16, Table 12.3, p.140]:
- **Riley's Knicks (1993, 1994)** remain #1 and #2 — they clearly exploited defensive rules to a systematic advantage
- New entrants: 1997 Bulls (#9), 1982 Milwaukee Bucks with Don Nelson (#15), 1991 San Antonio Spurs (#21), 1994 Sonics (#22), 2002 Spurs (#23)
- 1983 Philadelphia 76ers (three First-Team All-Defense players) moves from **84th → 35th** all-time

## Does Defense Win Championships? — Data
Using both standard and uncorrelated ratings to test the claim across 387 NBA playoff series since 1974 [S16, pp.142]:

| Measure | Better Defensive Team Wins | Better Offensive Team Wins |
|---|---|---|
| Standard ratings | 57% | **62%** |
| Uncorrelated ratings | 59% | **63%** |

**Conclusion:** Offense is a *better* predictor of playoff series wins than defense by ~4–6 percentage points under both measurement approaches. "Defense wins championships" is not supported by the data — offense matters more [S16, pp.141-142].

## Common Mistakes
1. **Taking standard regular-season ratings at face value for playoff prediction** → correction: use uncorrelated ratings; they better capture how hard teams actually play when everything is on the line
2. **Assuming defense wins championships** based on anecdote → correction: of 387 playoff series, the better offensive team won 62%; better defensive team won only 57%
3. **Overcorrecting** — uncorrelated ratings tell a similar story to standard ratings for most teams; don't over-rely on the adjustment for teams near the middle of the distribution

## Related Concepts
- [[concept-basketball-bell-curve-model]] — the source model from which uncorrelated ratings are derived
- [[concept-basketball-performance-indicators-winning]] — evidence-based indicators of winning
- [[concept-offensive-system-design]] — building offense as the primary competitive advantage

## Sources
- [S16, pp.138-142] — derivation of uncorrelated ratings, historical offense/defense tables, defense-wins-championships playoff study
