---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [analytics, statistics, defense, player-evaluation, possession-based]
source_count: 1
last_updated: 2026-04-11
---

# Defensive Stops Formula

## Summary
A defensive "stop" is when a player contributes to ending an opponent's possession without a score. Dean Oliver's formula for individual defensive stops has two parts: an **approximate part** (Stops₁) using recorded box-score statistics, and a **very approximate part** (Stops₂) using team-level data to estimate unrecorded contributions [S16, pp.359-361].

The stops calculation is the core input into the [[concept-individual-defensive-rating]]. More stops relative to possessions faced = better defensive rating. Stops are also used to calculate **stop percentage** (Stop%), the defensive equivalent of floor percentage.

## When to Use
- Evaluating individual defensive contribution beyond raw steals, blocks, and rebounds
- Understanding how shot-blocking, rebounding, and perimeter disruption are weighted against each other
- Distinguishing elite defenders from average ones within the same team context

## Key Principles

### 1. What Counts as a Stop [S16, p.359]
An individual contributes to a stop by:
1. Forcing a missed shot that is then rebounded by the defense
2. Getting a defensive rebound
3. Forcing a turnover (recorded as steal, or unrecorded)
4. Fouling a player who misses both foul shots, with the defense rebounding the second

### 2. FMwt — Forced Miss Weight
This weight determines how much credit a block deserves relative to a defensive rebound, using the same competition logic as the offensive rebound weight [S16, p.359]:
```
FMwt = DFG% × (1 − DOR%) ÷ [DFG% × (1 − DOR%) + (1 − DFG%) × DOR%]
```
In the NBA: Forcing a miss (~55% success) is harder than getting a defensive rebound (~70% success), so **blocks get more weight than defensive rebounds**. This ratio may differ at lower levels, and the formula automatically adjusts [S16, p.360].

### 3. Stops₁ — Box Score Stops [S16, p.359]
```
Stops₁ = STL + BLK × FMwt × (1 − 1.07 × DOR%) + DREB × (1 − FMwt)
```
- **STL**: Direct steal = direct stop
- **BLK × FMwt × (1 − 1.07 × DOR%)**: Blocks that lead to a stop (some blocked shots are recovered by the offense)
- **DREB × (1 − FMwt)**: Defensive rebounds, weighted by how much harder a miss was to force than to rebound

### 4. Stops₂ — Team-Estimated Stops [S16, p.360]
Captures forced misses and forced turnovers beyond steals and blocks, assuming equal distribution among teammates:
```
Stops₂ = [(TMDFGA − TMDFGM − TMBLK)/TMMIN × FMwt × (1 − 1.07 × DOR%) 
         + (TMDTO − TMSTL)/TMMIN] × MIN 
         + PF/TMPF × 0.4 × TMDFTA × (1 − TMDFT%)²
```
**Components**:
- First bracket: Team's non-block forced misses per minute × player's minutes
- Second bracket: Team's non-steal forced turnovers per minute × player's minutes
- Final term: Player's share of opponent free throws that result in stops (missed both shots)

**Critical limitation**: This assumes all players are equally good per minute at forcing bad shots and turnovers. Gary Payton forced 0.21 non-block misses/min vs. Jerome James at 0.08/min — the formula cannot capture this difference without positional adjustment [S16, p.360].

### 5. Total Stops
```
Stops = Stops₁ + Stops₂
```

### 6. Stop Percentage
```
Stop% = Stops × TMMIN ÷ (TMPOSS × MIN)
```
Interpretation: The fraction of possessions a player faces that result in a stop. A stop% of ~0.50–0.55 is typical for NBA players [S16, p.361].

### 7. Project Defensive Score Sheet Version
When a coach manually tracks forced misses (FM), forced turnovers (FTO), and free-throw results (FFTA) in a score sheet, the formula becomes more accurate [S16, p.361]:
```
Stops = FTO + STL + FFTA/10 + (FM + BLK) × FMwt × (1 − DOR%) + DREB × (1 − FMwt)
```
The FFTA/10 term estimates stops on free throw situations (approximately 1 stop per 10 free throw attempts against).

## Common Mistakes
1. **Treating all blocks as equal stops** → Many blocks are recovered by the offense; the (1 − 1.07 × DOR%) factor discounts blocks accordingly
2. **Ignoring Stops₂** → The majority of defensive value is in unrecorded forced misses and turnovers, not just steals and blocks
3. **Using Stops without team context** → Stop% normalizes for playing time and team pace; raw stops counts are misleading
4. **Not using positional adjustments** → Position-specific forced miss rates dramatically improve the Stops₂ estimate

## Related Concepts
- [[concept-individual-defensive-rating]] — Uses stop% as the primary input
- [[concept-offensive-rebound-weight]] — Parallel difficulty-weighting logic on the offensive side
- [[concept-individual-offensive-rating]] — The complete offensive counterpart system

## Sources
- [S16, pp.359-361] — Complete derivation of both parts of the stops formula
