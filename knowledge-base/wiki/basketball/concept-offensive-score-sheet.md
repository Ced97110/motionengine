---
type: concept
level: advanced
positions: [PG, SG, SF, PF, C]
tags: [analytics, statistics, game-film, scouting, possessions]
source_count: 1
last_updated: 2026-04-11
---

# Offensive Score Sheet (Oliver's Game Recording Method)

## Summary
In 1987, Dean Oliver developed a nontraditional method for recording what happens in a basketball game. Rather than tracking traditional box-score events (shots, rebounds, fouls) in isolation, Oliver's **Offensive Score Sheet** records the game in sequential possession units — who had the ball, what happened with it, and how the possession ended.

This scoring method is the empirical foundation for the entire *Basketball on Paper* framework. It allows the analyst to count possessions directly, trace the flow of a game, and see how individual actions connect to team outcomes. Oliver notes that using it in a coaching program is "certainly not necessary," but the logic it reveals — how shooting, rebounding, passing, and defense connect — is the conceptual backbone of the book [S16, p.2].

## When to Use
- Advanced game charting to build a possession-by-possession dataset
- Identifying which possessions a player is involved in (usage rate)
- Tracking fast-break vs. half-court possession splits
- Measuring true pace (possessions per game)
- Building the data foundation for individual ORtg/DRtg calculations

## Key Principles
1. **Possessions are the unit of record.** Each row on the score sheet represents one offensive possession, not one play or one event.
2. **Record the outcome, not just the action.** Did the possession end in a made shot? A turnover? A free throw trip? An offensive rebound (which extends rather than ends the possession)?
3. **Both teams' possessions are tracked alternately.** The sheet captures pace naturally — how many possessions each team used in a given time period.
4. **Identify the ball-handler and decision-maker.** This allows play% (usage rate) to be calculated per player.
5. **Connects to box-score statistics.** The score sheet data can be used to verify and interpret traditional box-score numbers — not replace them.

## Common Mistakes
1. **Treating an offensive rebound as a new possession** → An OREB extends the current possession; the possession counter does not advance until the ball is turned over, a shot attempt is not rebounded offensively, or free throws end the sequence.
2. **Not recording failed possessions** → A possession that ends in a turnover or missed shot must be recorded just as carefully as one that results in a basket. All possessions matter for efficiency calculations.
3. **Conflating possession with play** → A single possession can involve multiple passes, screens, and dribble moves before ending. The score sheet records the possession outcome, not each individual action within it.

## Related Concepts
- [[concept-basketball-statistical-framework]] — the system this score sheet feeds
- [[concept-points-per-possession]] — the primary metric calculated from possession data
- [[concept-individual-offensive-rating]] — requires accurate possession counts per player
- [[concept-scouting-philosophy]] — related scouting recording systems [S14]

## Sources
- [S16, p.2] — description of the score sheet and its role in the book
- [S16, Ch.2] — full chapter on offensive score sheets and watching games
