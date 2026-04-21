---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [analytics, player-evaluation, statistics, offense, defense, ratings]
source_count: 1
last_updated: 2026-04-11
---

# Individual Net Points

## Summary
Individual net points attempt to answer the game-level question: "How many net points did each player contribute in this game?" While individual win-loss records work well over a full season, game-by-game analysis often calls for a point-differential metric that can be distributed among teammates. Two methods are presented and averaged together, because neither alone captures the full picture [S16, pp.257-259].

The fundamental conceptual challenge is that **no player is a team** — points produced and points allowed are team events, not individual ones. The methods below make reasonable approximations but will never perfectly sum to the team's actual margin of victory [S16, p.260].

## When to Use
- Analyzing individual contributions within a specific game
- Tracking trends of individual vs. team performance across a season
- Identifying which players are positively or negatively driving team point differential
- Comparing star performers within a game where multiple players "go off"

## Key Principles
1. **Two versions capture different things and should be averaged.** The efficiency version penalizes high-volume scorers who are inefficient; the volume version rewards high scorers who stay on the court. Averaging balances both perspectives [S16, p.259].
2. **The sum across all teammates approximates but does not equal the team margin.** A small residual error is expected because individual stats are imperfect proxies for team events [S16, p.260].
3. **Defensive rating is the hardest component.** There is no perfect way to measure individual defensive points allowed; the approximation uses expected possessions faced based on minutes played [S16, p.258].
4. **"Points produced" includes all offensive contributions** — not just scoring, but the statistical value of all offensive actions (assists, offensive rebounds contributing to scores, etc.) [S16, p.258].

## Method 1: Efficiency-Based Net Points

### Formula
```
Net Points (v1) = (ORtg - DRtg) × Poss / 100
```

Where:
- **ORtg** = individual offensive rating (points produced per 100 possessions used)
- **DRtg** = individual defensive rating
- **Poss** = offensive possessions the player was involved in

### Interpretation
This version is **efficiency-based**. A player whose offensive rating is lower than their defensive rating will have a negative net points total even if they score 40 points. If a player goes 13-for-50 from the field for 40 points, this version likely gives them a negative total — their scoring volume came at such a cost in possessions that it hurt the team [S16, p.259].

## Method 2: Volume-Based Net Points

### Formula
```
Net Points (v2) = PtsProd - DRtg × (TmPoss × MIN) / (TmMIN × 100)
```

Where:
- **PtsProd** = actual points produced by the player on offense
- **DRtg** = individual defensive rating
- **TmPoss** = team possessions in the game
- **MIN** = individual minutes played
- **TmMIN** = team total minutes (5 players × game minutes)
- The fraction **TmPoss × MIN / TmMIN** estimates how many individual defensive possessions the player faced

### Interpretation
This version is **volume-based** (the "Spike Lee version"). A player who scores 40 points gets full credit for those 40 points, then has a reasonable defensive allowance subtracted based on their time on court. If they played 40 minutes out of 48, they faced roughly 1/5 of team possessions defensively (~16-18 possessions), so even a high defensive rating of 120 only means they allowed ~19-22 points — leaving a positive net contribution [S16, p.259].

## Average Net Points
```
Net Points (avg) = (Net v1 + Net v2) / 2
```

## NBA Example: 2001 Milwaukee Bucks vs. Charlotte Hornets (104-95 win)

| Player | Min | Poss | Off.Rtg | PtsProd | Def.Rtg | Net v1 | Net v2 | Net Avg |
|---|---|---|---|---|---|---|---|---|
| Robinson | 40 | 15.8 | 138 | 21.8 | 114 | 3.7 | 5.3 | 4.5 |
| Williams | 27 | 10.2 | 122 | 12.4 | 102 | 2.1 | 2.5 | 2.3 |
| Johnson | 37 | 4.7 | 105 | 4.9 | 104 | 0.0 | -8.9 | -4.4 |
| Allen | 46 | 21.6 | 119 | 25.7 | 113 | 1.2 | 6.9 | 4.0 |
| Cassell | 36 | 18.1 | 126 | 22.7 | 115 | 2.0 | 7.9 | 4.9 |
| Thomas | 29 | 9.0 | 99 | 8.9 | 110 | -1.0 | -2.6 | -1.8 |
| Hunter | 14 | 5.3 | 70 | 3.7 | 109 | -2.1 | -1.8 | -2.0 |
| Caffey | 11 | 1.8 | 115 | 2.0 | 99 | 0.3 | -1.9 | -0.8 |
| **Totals** | 240 | 86.4 | 118.2 | 102 | 109.9 | 6.2 | 7.4 | 6.8 |

Note: Team won by 9 actual points; both methods sum to ~+7, not +9. The ~2-point gap is the expected conceptual error [S16, p.260].

Key insight: Ray Allen and Sam Cassell had the highest scoring (the "Spike Lee view"), but Glenn Robinson was most efficient and contributed about the same average net points as Allen [S16, p.260].

## Common Mistakes
1. **Using only the volume method ("he scored 40 points!")** → Ignores efficiency; an inefficient 40-point game can be net negative for the team.
2. **Using only the efficiency method** → Ignores volume; a player who never shoots but has a great efficiency on limited touches appears to contribute more than they do.
3. **Expecting the sum to equal the team's actual point differential exactly** → A small residual is inherent to the method.
4. **Conflating net points with overall player value** → Net points is a game-level tool; bell curve win-loss records are better for season-level evaluation.

## Related Concepts
- [[concept-individual-win-loss-records]] — season-level framework that complements game-level net points
- [[concept-performance-rating-system]] — related player evaluation and weighting framework
- [[concept-basketball-performance-indicators-winning]] — team-level performance indicators

## Sources
- [S16, pp.257-260] — individual net points framework, two formulas, Milwaukee Bucks example
