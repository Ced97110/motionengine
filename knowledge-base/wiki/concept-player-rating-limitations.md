---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [analytics, player-evaluation, statistics, roster-construction]
source_count: 1
last_updated: 2026-04-11
---

# Player Rating Limitations

## Summary
No overall basketball player rating system can definitively identify who the greatest player is. This is because player ratings measure *performance*, which is the cumulative output of talent plus many other factors — teammates, coaches, system, schedule strength, roles, and even psychological/motivational variables. Depending on how much of measured performance reflects true talent versus context, a rating could be highly informative or nearly meaningless [S16, pp.183-184].

This does not make player ratings useless — they are good summaries of offensive and defensive performance over time. But they cannot be used to declare "who is the greatest" because they cannot isolate pure ability from its surrounding context.

## When to Use
- When evaluating a player for roster construction, understand that their rating reflects their *current context* as much as their ability
- When comparing players across different teams, systems, or eras
- When a player's rating changes dramatically after a trade — the new context, not just the player, has changed
- When a high-rated player fails to elevate a poor team — understanding why the rating doesn't translate

## Key Principles
1. **Performance ≠ talent**: Player ratings measure what a player *did*, which is talent plus teammates, coaches, system, schedule, roles, chemistry, and motivation.
2. **The 11-factor problem**: At minimum, team performance is affected by playing talent, coaching talent, scouting, strategy, strength of schedule, position/role fit, chemistry, and salary-incentive effects — the list is potentially infinite [S16, p.183].
3. **The 70/30 problem**: Even if performance reflects 70% talent and 30% other factors, a rating cannot reliably distinguish between players like Tim Duncan, Shaquille O'Neal, Dirk Nowitzki, and Kobe Bryant at the top level [S16, p.183].
4. **Extreme ratings are suspect**: A system rating Tim Duncan's 2002 season as yielding 89% win probability (73 wins with four average teammates) is implausible because it implies his actual teammates were far below average and that he exceeded the 1996 Bulls' all-time record — an extraordinary claim [S16, p.188].
5. **Pool dependency**: Rankings based on ordinal comparison within a pool change when the pool changes. Adding or removing players from the comparison group can change who ranks "best" — a known methodological flaw [S16, pp.190-191].
6. **Weight sensitivity**: Any system that weights statistics (assists × 2, rebounds × 0.5, etc.) can be manipulated to rank any of the top 5-6 players as "The Best" simply by changing the weights [S16, p.190].

## Player Responsibilities
This is an analytical concept applicable to all positions — no position-specific breakdown applies.

## Variations
### The Holy Grail Basketball League
The theoretically ideal player rating would come from a league in which the NBA's top players are rotated among different teammates, coaches, and opponents across many games. After ~20 games, true talent would begin to separate from context. The player whose patchwork teams win the most games would be the best player. This is conceptually perfect but practically impossible [S16, p.184].

### Simulation Approach (Bob Chaikin Software)
A piece of software developed by Bob Chaikin attempted to simulate various player combinations and was used by some NBA teams, but encountered problems that prevented widespread adoption [S16, p.184].

### Winston/Sagarin WINVAL Method
A lineup-based plus/minus system using NBA play-by-play data to measure points scored/allowed per minute with each lineup, adjusted for home/away and quality of competition. Conceptually sound but suffers from small sample sizes within individual lineup combinations and the problem that teams don't compete to maximize performance in every 8-minute stretch [S16, pp.185-188]. See [[concept-winval-plus-minus]].

## Common Mistakes
1. **Treating performance ratings as talent ratings** → Remember: performance = talent + context. A player's rating will change with different teammates, coaches, or systems even if their true ability is unchanged.
2. **Using ordinal rankings from a limited player pool** → Rankings are pool-dependent; changing who is included changes who ranks first. Always ask: "Best among whom?"
3. **Accepting extreme individual impact claims** → If a rating implies a single player can make an average team win 89% of games, the rating system has likely over-fitted to small samples or ignored team quality [S16, p.188].
4. **Ignoring sample size in lineup data** → A lineup that played only 60-70 minutes together cannot produce reliable quality estimates; random variance over ~1.5 games can easily swing a net rating by 30+ points per 48 minutes [S16, p.187].

## Related Concepts
- [[concept-winval-plus-minus]] — The specific Winston/Sagarin lineup-based method and its limitations
- [[concept-box-score-analysis]] — How to extract performance information from a single game
- [[concept-individual-defensive-ratings]] — The challenge of measuring the defensive side of individual performance
- [[concept-performance-rating-system]] — Lee Rose's weighted box-score performance rating (a simpler approach with similar limitations)

## Sources
- [S16, pp.183-191] — Chapter 15: "The Holy Grail of Player Ratings"
