# Play Extraction Proof of Concept

Validates whether Claude Vision can extract accurate basketball play data from
rasterized book diagrams. This is Resolution 1 from Motion's play animation
pipeline spec.

## Quick start

```bash
cp .env.example .env
# Edit .env — add your ANTHROPIC_API_KEY
make setup
make rasterize      # PDF → JPEG at 200 DPI for 5 selected pages
# Annotate data/ground-truth.json by eye (see spec Step 7)
make run            # 20 Claude Vision calls, ~$1 on Opus 4.7
make score          # writes results/scores.json
make overlay        # writes results/overlays/*.svg
make test           # unit tests for Bézier
```

## Outputs

- `results/decision.md` — the headline verdict
- `results/scores.json` — numerical accuracy
- `results/overlays/*.svg` — visual diffs (ground truth green vs extracted orange)

## Dependencies

- Python 3.9+
- poppler-utils (`pdftoppm`) — `brew install poppler`
- `ANTHROPIC_API_KEY` env var
- Source PDF: `backend/knowledge-base/raw/2018-19-nba-playbook.pdf` (934 pp)

## Model

Uses `claude-opus-4-7`. If the verdict is VIABLE or VIABLE_WITH_CORRECTION, probe
`claude-haiku-4-5-20251001` on the best strategy before running Resolution 3
at scale (production cost delta is 10x).

## References

- `backend/spec/play-extraction-poc.md` — this task's authoritative spec
- `backend/spec/play-animation-pipeline.md` — the master spec (6 resolutions)
- `backend/spec/play-viewer.md` — target rendering engine
