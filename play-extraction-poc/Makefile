.PHONY: setup rasterize run score overlay test clean verdict

setup:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt
	@echo ""
	@echo "Activate the venv with: source .venv/bin/activate"

rasterize:
	. .venv/bin/activate && python -m src.rasterize

run:
	. .venv/bin/activate && python -m src.extract

score:
	. .venv/bin/activate && python -m src.score

overlay:
	. .venv/bin/activate && python -m src.overlay

verdict: score overlay
	@echo ""
	@echo "Write results/decision.md manually using the template in the spec, or regenerate with: python -m src.decision"

test:
	. .venv/bin/activate && pytest tests/ -v

clean:
	rm -rf results/extractions/* results/overlays/* data/ground-truth-overlays/*
	rm -f results/scores.json results/decision.md
