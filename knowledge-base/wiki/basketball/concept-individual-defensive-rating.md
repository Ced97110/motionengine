---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [analytics, statistics, defense, player-evaluation, possession-based]
source_count: 1
last_updated: 2026-04-11
---

# Individual Defensive Rating

## Summary
The individual defensive rating measures how many points a player allows per 100 defensive possessions. It is the most approximate of Dean Oliver's individual metrics because basketball's official statistics do not record how many points any individual player allows — defense is inherently a team activity [S16, p.361].

The formula is built on **individual defensive stops** (the positive contributions a player makes defensively), which are estimated from steals, blocks, defensive rebounds, and team-level data about forced misses and forced turnovers. The rating then places each player's stop rate against a team defensive rating baseline, with a 20% influence weight reflecting the player's share of team possessions [S16, p.362].

## When to Use
- Comparing defensive contributions across players with different roles (shot-blocker vs. perimeter disruptor vs. defensive rebounder)
- Identifying true defensive impact beyond what raw blocks/steals show
- Understanding the limitation: individual defensive ratings are the least reliable stat in this system and should be used cautiously

## Key Principles

### 1. Individual Defensive Stops
A stop occurs when a player contributes to ending a possession without the offense scoring [S16, p.359]:
- Forcing a missed shot that the team rebounds
- Getting a defensive rebound
- Forcing a turnover (steal or non-steal)
- Fouling a player who misses both free throws (second rebounded by defense)

### 2. Stops₁ — The Approximate Part (Recorded Stats)
```
Stops₁ = STL + BLK × FMwt × (1 − 1.07 × DOR%) + DREB × (1 − FMwt)
```
Where FMwt = the relative difficulty of forcing a miss vs. getting a defensive rebound:
```
FMwt = DFG% × (1 − DOR%) ÷ [DFG% × (1 − DOR%) + (1 − DFG%) × DOR%]
```

**Why blocks get more weight than DREBs**: Forcing a missed shot (~55% difficulty in NBA) is harder than getting a defensive rebound (~70% success rate), so blocks receive higher weight than DREBs [S16, p.360].

### 3. Stops₂ — The Very Approximate Part (Team-Based Estimates)
Captures forced misses and forced turnovers not in the box score, but assumes all teammates are equally good per minute at forcing them [S16, p.360]:
```
Stops₂ = [(TMDFGA − TMDFGM − TMBLK)/TMMIN × FMwt × (1 − 1.07×DOR%) 
         + (TMDTO − TMSTL)/TMMIN] × MIN 
         + PF/TMPF × 0.4 × TMDFTA × (1 − TMDFT%)²
```
The last term estimates opponent free throw scoring attributable to a player's fouls.

### 4. Total Stops
```
Stops = Stops₁ + Stops₂
```

With **Project Defensive Score Sheet** data (tracking actual forced misses and turnovers), the formula simplifies to [S16, p.361]:
```
Stops = FTO + STL + FFTA/10 + (FM + BLK) × FMwt × (1 − DOR%) + DREB × (1 − FMwt)
```

### 5. Stop Percentage
```
Stop% = Stops × TMMIN ÷ (TMPOSS × MIN)
```
Example: 8 stops in 40 minutes of a 48-min game (TMMIN=240) with 90 team possessions → Stop% = 8×240÷(90×40) = 0.53 [S16, p.361]

### 6. Individual Defensive Rating Formula
A player's defense impacts each possession to a limited degree (base = team defensive rating), modified by how much better or worse they are at getting stops [S16, p.362]:
```
DRtg = TMDRtg + %TMDPoss × [100 × DPtsPerScPoss × (1 − Stop%) − TMDRtg]
```

In the default estimation (each player faces 20% of team possessions):
```
DRtg = TMDRtg + 0.2 × [100 × DPtsPerScPoss × (1 − Stop%) − TMDRtg]
```

### 7. The Core Limitation
No statistic records how many points a player allows. The formula assumes each score allowed is a **team score**, distributed approximately equally among teammates. This is rationalized by the reality that most defensive breakdowns involve multiple players [S16, p.361]:
> "Each score that a team allows is in many ways a *team* score."

## Common Mistakes
1. **Over-trusting individual defensive ratings** → They are the most approximate stat in Oliver's system; treat with appropriate skepticism
2. **Ignoring team context** → A player on a great defensive team will look better defensively than the same player on a poor team
3. **Equating steals with good defense** → Steals are only one component of Stops₁; forced misses and defensive rebounds also matter
4. **Assuming defensive stops are fully captured** → Stops₂ uses team averages and cannot differentiate between a great and poor defender at forcing bad shots
5. **Neglecting position effects** → Gary Payton forced 0.21 non-block misses/minute vs. Jerome James at 0.08/minute; using positional data improves estimates substantially [S16, p.360]

## Variations

### Position-Specific Forced Miss Rates
Using position-specific allowed field goal data rather than team averages to estimate Stops₂ dramatically improves accuracy. Point guards force more non-block misses per minute than centers (who force misses via blocks) [S16, p.360].

### Project Defensive Score Sheet
Oliver's proposed improvement: manually track forced misses (FM), forced turnovers (FTO), and free-throw outcomes (FFTA) during games. With this data, the individual stop count is far more precise [S16, pp.360-362].

## Related Concepts
- [[concept-individual-offensive-rating]] — The offensive counterpart with parallel difficulty-based credit distribution
- [[concept-floor-percentage]] — The offensive efficiency metric; no direct defensive equivalent exists
- [[concept-defensive-stops-formula]] — Detailed breakdown of the stops calculation
- [[concept-performance-rating-system]] — A simpler alternative from S13 that uses weighted box scores

## Sources
- [S16, pp.359-362] — Complete derivation of individual defensive stops and rating formula
