---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [analytics, game-analysis, statistics, offense, defense, scouting]
source_count: 1
last_updated: 2026-04-11
---

# Possession Score Sheet (Oliver Shorthand System)

## Summary
Dean Oliver's possession score sheet is a pen-and-paper shorthand system for tracking every action in a basketball game at the possession level. By recording each pass, dribble, shot attempt, rebound, turnover, and foul in sequence using player uniform numbers and compact symbols, the system creates a complete play-by-play transcript that reveals the ebb and flow of the game — which players touch the ball, how possessions end, where shots come from, and how ball movement creates or prevents scoring [S16, pp.8-22].

The system was used by Oliver to hand-score games in real time and forms the data foundation for his player evaluation metrics (individual points produced, individual defensive stops, team efficiency). It is illustrated in detail through a full possession-by-possession reconstruction of Game 4 of the 1997 NBA Finals (Chicago Bulls vs. Utah Jazz) [S16, pp.8-22].

## When to Use
- When conducting detailed scouting analysis of a specific opponent
- When evaluating which lineups, plays, or player combinations are most productive
- When studying ball movement and shot-creation patterns
- When building a database of individual player production and efficiency
- As an advanced coaching tool for post-game video review

## Key Principles

### Possession Structure
1. Each possession is recorded on one line, beginning with the score at the *end* of the possession, followed by the team abbreviation, followed by the action sequence [S16, p.9].
2. Player actions are recorded using uniform numbers; the scoring team's score is listed on the left [S16, p.9].

### Core Notation Symbols
The following symbols are used throughout the system [S16, pp.9-22]:

| Symbol | Meaning |
|--------|--------|
| `[number]` | Player touch/pass (e.g., `12` = player #12 has the ball) |
| `D` (superscript) | Dribble used to gain significant ground |
| `D/` (superscript) | Dribble crossing half-court |
| `/` | Pass crossing half-court (less common than dribble crossings) |
| `—` (subscript) | Missed field goal attempt; location subscript follows |
| `+` | Made field goal (unassisted) |
| `++` | Made field goal (assisted) |
| `R` (superscript) | Rebound |
| `RD` (superscript) | Rebound followed immediately by dribble |
| `F` + number + `(n)` | Foul committed; number = fouler; (n) = foul count |
| `X` | Missed free throw |
| `*` | Made free throw |
| `BP TO` | Turnover via bad pass |
| `LB TO` | Turnover via lost ball |
| `TRVL TO` | Turnover via travel |
| `OB TO` | Turnover — ball out of bounds |
| `STL` (superscript) | Steal |
| `BK` + number | Block (by player #) |
| `KOB` (superscript) | Ball knocked out of bounds |
| `ROB` (superscript) | Rebound that went out of bounds |
| `OB` (superscript) | Inbounds play; number indicates the inbounder |
| `OF` | Offensive foul |
| Underline `__` | Player posting up |
| `TIME X:XX` | Timeout called at specified game clock |
| `(TFOUL [number] [shooter]: result)` | Technical foul; who shot the free throws and result |
| `(DOUBLE TFOUL [n1],[n2])` | Double technical foul |
| `(ILL D WARN)` | Illegal defense warning |
| `KICK` | Kicked ball violation |
| `BK9 24-S CK TO` | Shot-clock violation following a block |
| `END 1Q / 2Q / 3Q` | End of quarter marker |

### Shot Location Map
Shot locations are encoded as subscripts following shot result symbols (— or +/++) using a nine-region court map [S16, p.10]:

```
         Z (above arc, straight)
      C (mid-range center)
  R | D | L    B (mid-range right block area)
   2 (paint)   Y (right wing extended)
      1 (baseline mid)    
         A (baseline center)
            X (corner baseline)
```

- **Within 3PT line**: regions 1, 2, A, B, C (mid-range zones)
- **Beyond 3PT line**: X, Y, Z (three-point zones)
- **At the rim**: L (left layup), R (right layup), D (dunk)
- Locations are approximate, not precise coordinates [S16, p.10]

### Assist Definition
A working definition used in the system: "Did the scorer have to do anything *unexpected* to score the basket?" If yes — no assist. If no — give the passer an assist. The official definition ("pass that leads directly to a score") is deliberately vague and inconsistently applied [S16, p.12].

### Posting Up
An underline beneath a player number indicates that player is in the post at some point during their ball possession. This is not a precise time-stamp — it signals they were in the post at some point. Players can enter and exit the post without additional notation [S16, p.13].

### Dribbling Notation
The superscript D is reserved for dribbles that gain significant ground, not just balance dribbles or stationary dribbles. The intent is to capture player movement on the court [S16, p.10].

## Common Mistakes
1. **Expecting perfect completeness** → The system cannot capture every detail (e.g., specific screen actions, exact defensive assignments). It captures the most important elements of possession flow [S16, p.13].
2. **Confusing dribble crossings with pass crossings** → Ball crossing half-court on the dribble (D/ superscript) is far more common than crossing on a pass (/ alone) [S16, p.11].
3. **Missing the inbounder notation** → The inbounder's number with OB superscript is most critical when the inbounder passes to a scorer (to credit the assist correctly) [S16, p.13].
4. **Speed of the game** → Real-time game scoring requires practice; handwriting becomes sloppy at game speed. Electronic shot charts exist but are incompatible with the full shorthand system [S16, p.11].

## Application Example: 1997 NBA Finals Game 4
The system is illustrated in full detail through Game 4 (Bulls vs. Jazz, Utah leads series 1-2 before the game). Key observations enabled by the system [S16, pp.8-22]:
- **Karl Malone** touched the ball on virtually every Utah possession; his misses and makes are precisely tracked
- **Michael Jordan** touched the ball on every Bulls possession in the fourth quarter; scored 6 field goals in Q4
- **Dennis Rodman's impact** on team scoring pace is visible: when he was out, both teams scored more easily
- **John Stockton's gutsiest pass** — full-court pass to Malone for layup and 74-73 lead with 44.5 seconds left — is captured in the sequence: `74 UTA 12RD / 32++ TIME CHI 0:44.5`
- **Jordan's steal by Stockton** in the final minute is captured as: `70 UTA 12STLD/F23 *X`

## Related Concepts
- [[concept-basketball-analytics-philosophy]] — The analytical philosophy that motivates this tracking system
- [[concept-performance-rating-system]] — A related system (from S13) for converting box-score data into weighted player production scores
- [[concept-scouting-philosophy]] — Pro scouting systems that also track possession-level opponent tendencies
- [[concept-basketball-performance-indicators-winning]] — Evidence-based KPIs that this kind of possession tracking can help identify

## Sources
- [S16, pp.8-22] — Complete system introduction and illustrated application through the 1997 NBA Finals Game 4
