---
type: training
last_updated: auto
---
# Game Report Few-Shot Examples

100 curated NBA game reports used as few-shot context when generating post-game and halftime reports.

## Usage

The report generation function (`lib/game_report.py`) selects the 3 most relevant examples based on game margin similarity and includes them in the Claude API prompt.
