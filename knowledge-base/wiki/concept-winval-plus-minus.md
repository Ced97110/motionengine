---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [analytics, player-evaluation, statistics, lineup-analysis, plus-minus]
source_count: 1
last_updated: 2026-04-11
---

# Winston/Sagarin WINVAL Plus/Minus Method

## Summary
The WINVAL system, developed by Wayne Winston and Jeff Sagarin using NBA play-by-play data, measures the point differential (and points scored/allowed) per unit time for every lineup combination on the floor. By aggregating these lineup segments across a full season and adjusting for home-court advantage and quality of competition, the system attempts to produce individual player ratings that reflect both offensive and defensive contribution [S16, pp.185-186].

The method is conceptually intuitive — it directly measures what happens when a specific player is on the floor — but suffers from two significant limitations: (1) basketball teams don't compete to win every short segment of a game equally, and (2) most lineup combinations play too few minutes together to produce statistically reliable estimates.

## When to Use
- Evaluating player impact over a full season when ample lineup data is available
- Identifying lineup combinations that produce unusual net point differentials
- As one input among many in roster construction, never as the sole decision criterion
- Most reliable for players who play heavy minutes in consistent roles

## Key Principles
1. **Core calculation**: For each lineup segment, record points scored and points allowed. Convert to a per-48-minute rate. This gives a raw net rating for each lineup [S16, p.186].
2. **Adjustments**: Correct for home/away (NBA home advantage ≈ 4 points per 48 minutes, or ~1 point per quarter) and quality of the opposing lineup [S16, p.186].
3. **Offensive/defensive split**: The system separately tracks how many points are scored and allowed, not just the net margin, enabling separate offensive and defensive player ratings [S16, p.186].
4. **Statistical fitting**: Because players share lineup time across many different combinations, a statistical method is applied to simultaneously estimate each player's individual contribution given all the lineup data [S16, p.191 endnote].
5. **Team-win probability**: One output of the system is the estimated win probability for a team consisting of that player plus four league-average players. This is intuitive but can produce extreme estimates [S16, p.188].

## Player Responsibilities
Not position-specific — the method applies equally to all positions.

## Variations
### Offensive/Defensive Split Ratings
By looking at points scored (not just net margin) during a player's lineup time, the system estimates both offensive contribution (how much the team scores with the player on the floor) and defensive contribution (how much the opponent scores). These can diverge — a player can look like a better offensive player and a worse defensive player simultaneously [S16, p.186].

### Win Probability Output
The most intuitive but most extreme output: the estimated winning percentage for a team of one player plus four average teammates. Tim Duncan was rated at 89% (≈73 wins) for 2002, which the author argues is implausibly high given that the 1996 Bulls only won 72 games [S16, p.188].

## Common Mistakes
1. **Treating 60-70 minute lineup samples as reliable** → A lineup that plays together for only 60-70 minutes (~1.5 games) can easily show ±14-18 point per-48-minute swings due to random variance alone. The difference between the best and worst Indiana lineup in 2002 may have been pure luck [S16, p.187].
2. **Ignoring garbage time and tanking** → Basketball teams compete to win the 48-minute game, not every 8-minute segment. When teams are up by 20, they relax — but the data treats that segment the same as a close fourth quarter. This inflates or deflates ratings based on when a player happens to be on the floor [S16, pp.186-187].
3. **Accepting extreme individual impact estimates without sanity checks** → A player rating of 89% win probability implies his actual teammates were dramatically below average AND that he would exceed the greatest team record in NBA history. Check extreme outputs against historical context [S16, p.188].

## Related Concepts
- [[concept-player-rating-limitations]] — The broader framework for understanding why any player rating has fundamental limits
- [[concept-box-score-analysis]] — The foundation for reading individual performance from game data
- [[concept-individual-defensive-ratings]] — A complementary approach to measuring defensive impact

## Sources
- [S16, pp.185-188] — Chapter 15, Box 1: "What the Winston/Sagarin Method Does"
