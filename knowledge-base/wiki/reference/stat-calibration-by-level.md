---
type: reference
last_updated: auto
---
# Stat Calibration by Competition Level

This table defines expected statistical ranges at each competition level.
Used by the AI to calibrate game analysis -- what is "notable" at U14 differs from U18.

| Level | PPG | FG% | TOV/game | Notable scorer | AST | REB |
|-------|-----|-----|----------|---------------|-----|-----|
| nba | 105.2 | 45.7% | 13.6 | 37+ pts | 23.0 | 43.8 |
| college | 68.4 | 42.5% | 15.0 | 24+ pts | 13.8 | 37.2 |
| u18_natl | 57.9 | 39.8% | 17.7 | 20+ pts | 11.5 | 35.0 |
| u18_club | 52.6 | 37.5% | 20.4 | 18+ pts | 10.3 | 32.8 |
| u16_natl | 47.3 | 36.6% | 21.8 | 17+ pts | 9.2 | 30.7 |
| u16_club | 42.1 | 34.3% | 24.5 | 15+ pts | 8.0 | 28.5 |
| u14_natl | 40.0 | 32.9% | 25.8 | 14+ pts | 6.9 | 26.3 |
| u14_club | 36.8 | 31.1% | 27.2 | 13+ pts | 5.8 | 24.1 |
| u12 | 29.5 | 27.4% | 31.3 | 10+ pts | 4.6 | 21.9 |
| u10 | 21.0 | 22.9% | 38.1 | 7+ pts | 3.4 | 19.7 |
| rec | 31.6 | 25.1% | 34.0 | 11+ pts | 3.4 | 21.9 |

Source: Computed from SportsSettBasketball dataset (6,150 NBA games) with level ratios estimated from coaching knowledge.
