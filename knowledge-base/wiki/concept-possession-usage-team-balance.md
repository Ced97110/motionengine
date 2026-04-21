---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [analytics, statistics, offense, team-offense, possessions, player-evaluation, roster-construction]
source_count: 1
last_updated: 2026-04-11
---

# Possession Usage and Team Offensive Balance

## Summary
% Team Possessions (usage rate) measures what percentage of a team's offensive possessions a given player is responsible for while he is on the court. With five players on the court, an "equal share" is 20% per player. This metric, combined with [[concept-individual-offensive-rating]], reveals whether a team's possession distribution is optimized — are the most efficient players also the highest-usage players? [S16, pp.157-162]

## When to Use
- Evaluating whether a team's ball distribution is efficient
- Identifying players who are too high- or too low-usage relative to their efficiency
- Comparing a team before and after a personnel change
- Deciding how to attack a defense: force inefficient high-usage players to use *more* possessions

## Key Principles
1. **Efficient offensive structure: high-efficiency players should also be high-usage.** The 2002 Lakers had Shaq (Rating 116, 31% usage) and Kobe (Rating 112, 30%) — efficient players dominating possessions [S16, p.158].
2. **Inefficient offensive structure: high-usage players with low ratings kill team offense.** The 1999 Blazers had Rider (Rating 99, 24% usage) and Stoudamire (Rating 101, 22%) leading in possessions — below-average efficiency at the top [S16, p.158-159].
3. **Role players are often "efficient" simply because of low usage.** A player taking 12% of possessions only gets the easy shots. Their high rating doesn't mean they could sustain it with higher usage [S16, p.158].
4. **A player's optimal usage depends on teammates.** If better scorers are available, the right play is to distribute to them. Optimal play adapts to the roster, not personal statistics [S16, p.147].
5. **The defensive implication: force inefficient high-usage players to use MORE possessions.** If Rick Fox has a below-average rating at 16% usage, defenses should try to force him to handle the ball more [S16, p.157].

## Case Studies

### 2002 Los Angeles Lakers — Efficient Distribution
- Shaq + Kobe = 61% of possessions at combined ~Rating 114
- Remaining 3 spots average only ~13% each
- High-efficiency players match high-usage roles → team offense = 109.4 [S16, p.157-158]

### 1999 vs. 2000 Portland Trail Blazers — Personnel Change Impact
**1999:** Top-2 (Rider + Stoudamire) combined rating = ~100; team offense = 104.7  
**2000:** Smith (Rating 120) replaced Rider; Wallace (Rating 108) led; top-2 combined = 114; team offense = 107.9  
Replacing one inefficient high-usage player with an efficient one produced a +3.2 point swing in team offense [S16, pp.158-159]

### Michael Jordan's Impact on Bulls
- With Jordan (1993): Rating 119 at 33% usage → Team offense = 112.9
- Without Jordan (1994): Every returning Bull became less efficient; team offense = 106.0
- The ~7-point decline matches replacing Jordan (Rating ~119) with a replacement-level player (Rating ~95)
- This validates that individual offensive ratings predict team offense changes [S16, pp.160-161]

### 1995 Bulls — Kukoc as the Recovery Engine
- Kukoc improved from Rating 100 (1994) to Rating 118 (1995)
- Substituting just Kukoc's 1995 stats into the 1994 team produced nearly the exact observed 1995 team improvement (+3 pts/100 possessions)
- Demonstrates that individual ratings are predictive [S16, p.162]

### 1996 Bulls — Perfect Distribution
| Player | Rating | Usage |
|---|---|---|
| Jordan | 124 | 31% |
| Pippen | 116 | 24% |
| Kukoc | 125 | 21% |
| Harper | 116 | 15% |
| Steve Kerr | 141 | 12% |

Every significant contributor is above the league average (~104). Team offense = 115.2 on a 72-10 team [S16, p.162]

## Player Responsibilities
- **PG**: Typically moderate-to-high usage; rating determines whether that usage is justified
- **SG**: Often highest or second-highest usage; efficiency at this load is the key variable
- **SF**: Usage should match skill — a defensive specialist should have low usage
- **PF/C**: Post players often have high floor% at moderate usage; their rating is most affected by FT%

## Common Mistakes
1. **Giving high-usage players more possessions when they are inefficient** → The 1999 Blazers ran their offense through below-average offensive players
2. **Assuming low-usage efficiency scales to star usage** → Role players are efficient *because* of low usage; their rating would likely drop with higher responsibility
3. **Ignoring efficiency when valuing a star player** → Points per game is not sufficient; points produced per possession is what matters

## Related Concepts
- [[concept-individual-offensive-rating]] — the efficiency metric that should be matched to usage
- [[concept-individual-floor-percentage]] — companion scoring-consistency metric
- [[concept-difficulty-theory-credit-distribution]] — the theory that generates usage-aware credit
- [[concept-performance-rating-system]] — alternative evaluation framework [S13]

## Sources
- [S16, pp.155-162] — Chapter 14: NBA team case studies and usage analysis
