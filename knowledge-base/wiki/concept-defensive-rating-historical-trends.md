---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [defense, analytics, NBA, statistics, team-evaluation]
source_count: 1
last_updated: 2026-04-11
---

# Defensive Rating — NBA Historical Analysis

## Summary
Defensive rating measures a team's defensive efficiency as **points allowed per 100 possessions**. Lower is better. Oliver compiled the top 25 NBA defenses since 1974, finding that the Pat Riley New York Knicks teams of 1993 and 1994 were the greatest defensive teams in NBA history by a wide margin — their gap over the #2 defense was as large as the gap between the #1 and #18 offense [S16, p.46].

Riley's Knicks defense worked by **completely taking away the interior**, exploiting hand-check rules, and fouling players who got near the basket to prevent layups. This approach influenced the entire defensive landscape of the 1990s and directly caused the rule changes that brought zone defense to the NBA in 2002 [S16, p.46].

## When to Use
- Evaluating a team's defensive quality independent of its offensive tempo
- Comparing defenses across eras using standard deviation normalization
- Identifying what makes elite defenses different (personnel vs. system vs. effort)
- Game planning: understanding how best defenses force opponents to play

## Key Principles
1. **All elite defenses allow below-average field goal percentages** — forcing bad shots is the universal trait of great defenses, regardless of shot-blocking volume [S16, p.52]
2. **Shot-blocking presence in the middle helps but is not required** — many top defenses had below-average team block rates while still dominating [S16, p.52]
3. **Straight-up man defense is the common system** — NBA defenses historically had limited structural variation; great defenses played man-to-man straight up without heavy double-teaming [S16, p.50]
4. **System may matter more for defense than offense** — top defenses had fewer All-NBA stars (16/10/4 vs. 20/11/7 for top offenses) suggesting systems and coaching drive defense more [S16, p.50]
5. **Coaching continuity strongly predicts top defenses** — multiple coaches (Riley, Jackson, Popovich, Frank Layden/Jerry Sloan) appear with multiple teams [S16, p.52]
6. **Pace of great defenses** — best defensive teams played ~0.5 possessions per game *slower* than average; best offensive teams played ~0.3 possessions per game *faster* [S16, p.50]

## Top 25 Historical Defenses (by Increment below Average)
From Table 3.8 [S16, pp.47-49]:

| Rank | Team | Season | Def Rating | Relative to League | Key Players |
|------|------|--------|------------|-------------------|-------------|
| 1 | New York Knicks | 1993 | 99.7 | -8.4 | Ewing, Oakley, Starks, Mason, Rivers |
| 2 | New York Knicks | 1994 | 98.2 | -8.1 | Ewing, Oakley, Starks, Mason |
| 3 | San Antonio Spurs | 1999 | 95.0 | -7.2 | Duncan, Robinson, A. Johnson, Elliott |
| 4 | Washington Bullets | 1975 | 92.2 | -6.4 | Wes Unseld, Elvin Hayes, Phil Chenier |
| 5 | Utah Jazz | 1989 | 101.5 | -6.3 | Mark Eaton, Stockton, Malone, Bailey |
| 6 | Phoenix Suns | 1981 | 100.5 | -6.2 | T. Robinson, Dennis Johnson, W. Davis |
| 7 | Miami Heat | 1997 | 100.6 | -6.1 | Mourning, P.J. Brown, Tim Hardaway |
| 8 | Philadelphia 76ers | 1981 | 100.6 | -6.1 | Dr. J, Dawkins, Bobby Jones, Mo Cheeks |

## Top 25 Historical Defenses (Standard Deviations below Average)
From Table 3.9 [S16, pp.49]:

| Rank | Team | Season | Def Rating | Std Dev below Avg |
|------|------|--------|------------|--------------------|
| 1 | New York Knicks | 1993 | 99.7 | -2.88 |
| 2 | Washington Bullets | 1975 | 92.2 | -2.86 |
| 3 | Utah Jazz | 1989 | 101.5 | -2.49 |
| 4 | New York Knicks | 1994 | 98.2 | -2.35 |
| 5 | Golden State Warriors | 1976 | 95.5 | -2.03 |

*Note: The Washington Bullets of 1975 rise to #2 by standard deviations because the SD of defensive ratings was very tight that season.* [S16, p.49]

## Key Defensive Coaching Patterns
From Table 3.12 [S16, p.54]:
- **Pat Riley**: NYK 1993, NYK 1994, MIA 1997
- **Gregg Popovich**: SAN 1999, SAN 1998, SAN 2000, SAN 2001
- **Phil Jackson**: CHI 1996, LAL 2000, CHI 1998
- **Frank Layden/Jerry Sloan**: UTA 1989, UTA 1988, UTA 1985, UTA 1987
- **Lenny Wilkens**: CLE 1989, ATL 1999
- **Larry Brown**: NJN 1983, DEN 1977

The recurrence of coaches across multiple teams is strong evidence that defensive *systems* are portable and coachable [S16, p.52].

## Statistical Indicators of Top Defenses
From Table 3.10 [S16, p.51], all top defenses shared:
- **Below-average floor percentage allowed** (opponents shot poorly)
- **Below-average field goal percentage allowed**
- **Below-average play percentage** (fewer possessions that scored at least 1 point)
- No consistent pattern in pace (possessions per game)

## Common Mistakes in Building/Evaluating Defenses
1. **Overvaluing shot-blockers** → many elite defenses had below-average team block rates; forcing bad shots matters more than blocking good ones [S16, p.52]
2. **Ignoring interior presence** → while not universally necessary, a shot-blocking threat in the middle was a *trait* of many great defenses [S16, p.52]
3. **Confusing effort with system** → the worst defenses often came in lockout/expansion years when players were out of shape, supporting the "defense is effort" maxim [S16, p.59]

## Height Analysis
From Table 3.13 [S16, p.55]: Top defensive teams averaged slightly *shorter* than top offensive teams, but both were close to league average (within ~0.5 inches). Height helps defense but is not determinative.

## Related Concepts
- [[concept-offensive-rating-historical-trends]] — the complementary offensive efficiency metric
- [[concept-pace-of-play]] — how possessions per game relates to defensive performance
- [[concept-roster-stability]] — why continuity predicts defensive performance
- [[concept-four-factors-basketball]] — what defensive factors matter most

## Sources
- [S16, pp.46-55] — Top 25 defenses tables (3.8, 3.9, 3.10, 3.12, 3.13), commentary on Riley Knicks, shot-blocking, coaching patterns
- [S16, p.50] — Stars vs. systems analysis
- [S16, p.52] — Shot-blocking and straight-up man defense discussion
