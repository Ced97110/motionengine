---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [analytics, offense, efficiency, possession-usage, player-evaluation, optimization, individual-offense]
source_count: 1
last_updated: 2026-04-11
---

# Offensive Skill Curves

## Summary
An offensive skill curve is a plot of a player's *possession usage rate* (what percentage of team possessions he uses, on the Y-axis) against his *offensive efficiency rating* (points per 100 possessions, on the X-axis). The curve shows how a player's efficiency changes as his role in the offense expands or contracts. [S16, pp.232-241]

The fundamental insight: **players who use more possessions do so at lower efficiency; players who use fewer possessions are forced to take smarter shots and become more efficient**. This trade-off has massive implications for how coaches allocate offensive roles and how teams should respond when a star is missing.

The concept was developed by Dean Oliver after years of NBA data analysis. Though the curves are difficult to construct perfectly (players rarely voluntarily reduce their role), they provide a scientific framework for questions coaches answer intuitively every day.

## When to Use
- Evaluating whether to ask a high-volume scorer to take fewer shots
- Assessing what happens to secondary players if a star is injured
- Optimizing possession distribution across a lineup
- Understanding why role players on star-heavy teams often look more efficient than they truly are
- Identifying "true scorers" who maintain efficiency at high volume vs. "false scorers" who are only efficient in a limited role

## Key Principles
1. **The curve always declines**: As possession usage increases, efficiency decreases. The only way to improve rating is to take smarter (fewer) shots. The curve must trend downward from left to right [S16, p.233]
2. **The curve shifts with context**: Better teammates or career peak performance shifts the curve right (higher efficiency at the same usage). Worse teammates or old age/youth shifts it left [S16, p.234]
3. **"Scorers" use 32–35% of possessions**: High-volume scorers like Allen Iverson and Jerry Stackhouse used 32–35% of team possessions and had offensive ratings of 100–105 at that load — about average [S16, p.233]
4. **Elite scorers extend far right**: Michael Jordan and Cynthia Cooper could maintain high efficiency even at very high usage rates — their curves extend much farther to the right than ordinary scorers [S16, p.236]
5. **Role players benefit from star usage**: When a star uses 35% of possessions, each of the other four players uses ~16% on average — well within their comfort zone, producing much higher efficiency than if asked to do more [S16, p.237]
6. **The verification test**: Shaq used 31% of Lakers possessions in 2002, projecting to a 115–118 rating on his skill curve. His actual rating was ~116. Kobe's 30% usage projected to ~113; actual was 112. The curves accurately reproduce reality [S16, p.238]

## Player Examples

### Allen Iverson (age 26)
- Usage: 32–35% of team possessions
- Rating at 33% usage: ~100–105 (average NBA)
- Rating if dropped to 20% usage: ~112
- Curve interpretation: A "scorer" type — high volume, average efficiency at current load. Could be more efficient if used less, but that never happened [S16, pp.232-233]

### Jerry Stackhouse (2001-02)
- Very similar curve shape to Iverson
- Usage: 31–34% of possessions
- Rating at 33%: ~100–105
- Rating if dropped to 20%: ~108
- Note: Even when Stackhouse "tried to be unselfish" in 2002, his usage only dropped from 34% to 32% [S16, p.236]

### Michael Jordan (1996-97)
- Curve extends much farther right than Iverson/Stackhouse
- Could maintain efficiency at 35–40% usage where ordinary scorers collapse
- Very similar curve shape to Cynthia Cooper (WNBA) — both were elite ball-dominant scorers [S16, p.236]

### Cynthia Cooper (Houston Comets, 1998-99)
- WNBA offensive efficiency curve essentially matched Jordan's shape
- Described as the "Michael Jordan of the WNBA" — the curves supported this [S16, p.236]

### Eric Snow (76ers)
- Low usage role player who benefited from Iverson's ball dominance
- At 16% usage: rating improved several points above what he'd post at 20%+
- If forced to use 20%+ of possessions, his efficiency would drop substantially [S16, p.237]

### Shaq O'Neal and Kobe Bryant (2002 Lakers)
- Both used ~30% of possessions at ratings of 116–117 — rare elite level
- Their dominance allowed Fisher (16%) and Horry (14%) to post high efficiency ratings
- Team offensive rating: ~114 — a very good offense [S16, p.238]

## Optimizing Team Offense

Skill curves can be used to model what happens to team offense when possession distribution changes [S16, pp.239-241]:

**Lakers baseline** (actual 2002):
- Bryant: 30%, OR=114; O'Neal: 30%, OR=117; Fisher: 16%, OR=115; Horry: 14%, OR=114; Fox: 10%, OR=108 → **Team OR: 114**

**If Kobe/Shaq dropped to 25% each (Fisher, Horry, Fox pick up slack)**:
- Fisher forced to 20%: OR drops to ~90; Horry to 17%: OR drops to ~93 → **Team OR: 107** (7-point drop — massive)

**If Fox picks up the slack instead**:
- Fisher stays at 17%: OR=113; Horry at 15%: OR=100; Fox rises to 18%: OR=102 → **Team OR: 112** (only 2-point drop)
- Fox can handle more possessions better than Fisher/Horry can

**Key lesson**: Not all role players are equally capable of absorbing extra possessions. Fox served as a better "buffer" than Fisher or Horry when stars were unavailable [S16, p.241]

## Common Mistakes
1. **Assuming all players have the same curve shape** → The fundamental difference between scorers and role players is curve depth and rightward extension
2. **Evaluating role players without considering usage context** → A role player's high efficiency rating may be entirely explained by the star's ball dominance. Move that player to a team without a ball-dominant star and his efficiency collapses
3. **Demanding more balanced offense for its own sake** → Moving possessions from an efficient high-usage player to less-capable role players almost always decreases team offensive rating [S16, p.240]
4. **Ignoring uncertainty in flat regions** → Skill curves are least reliable in regions where data is sparse (players rarely use that level of possessions). Fisher's curve in the 20%+ region has high uncertainty [S16, p.239]

## Constructing Skill Curves
Oliver took years to develop reliable methods. Key principles [S16, p.239]:
- Built from box score data and general trends observed across many games
- Curves are forced to be declining (any apparent increase at lower usage is an artifact of defensive adjustment, not true skill)
- Data is sparse for players who rarely operate outside their normal usage range
- Think of them as "sonograms" — blurry but revealing a real shape

## Related Concepts
- [[concept-individual-win-loss-records]] — The next step: translating efficiency into wins contributed
- [[concept-coaching-evaluation-metrics]] — Skill curves inform what expectations are reasonable for a given roster
- [[concept-performance-rating-system]] — Another approach to quantifying individual player contribution
- [[concept-offensive-system-design]] — How to design an offense around the skill levels of available players

## Sources
- [S16, pp.232-241] — Complete treatment of offensive skill curve theory, player examples, and optimization application
