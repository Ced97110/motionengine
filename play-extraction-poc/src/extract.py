"""Run the 3 extraction strategies against all rasterized diagrams.

Writes one YAML file per (diagram × strategy) to results/extractions/.
On failure, writes a .error.txt file with the exception message.
"""
from __future__ import annotations

import base64
import os
from pathlib import Path

from anthropic import Anthropic

HERE = Path(__file__).resolve().parent.parent
DIAGRAMS_DIR = HERE / "data" / "diagrams"
REFERENCE_PNG = HERE / "data" / "reference-court.png"
OUT_DIR = HERE / "results" / "extractions"
PROMPTS = HERE / "src" / "prompts"

MODEL = "claude-opus-4-7"

_client = None


def client() -> Anthropic:
    global _client
    if _client is None:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise SystemExit("ANTHROPIC_API_KEY is not set. Copy .env.example to .env and fill it in.")
        _client = Anthropic()
    return _client


def load_b64(path: Path) -> str:
    return base64.standard_b64encode(path.read_bytes()).decode("utf-8")


def image_block(path: Path, media_type: str) -> dict:
    return {
        "type": "image",
        "source": {"type": "base64", "media_type": media_type, "data": load_b64(path)},
    }


def run_strategy_a(diagram: Path) -> str:
    prompt = (PROMPTS / "strategy_a_raw.txt").read_text()
    msg = client().messages.create(
        model=MODEL,
        max_tokens=2000,
        messages=[{"role": "user", "content": [
            image_block(diagram, "image/jpeg"),
            {"type": "text", "text": prompt},
        ]}],
    )
    return msg.content[0].text


def run_strategy_b(diagram: Path) -> str:
    if not REFERENCE_PNG.exists():
        raise FileNotFoundError(f"Reference court PNG missing: {REFERENCE_PNG}. Run `python -m src.build_reference`.")
    prompt = (PROMPTS / "strategy_b_calibrated.txt").read_text()
    msg = client().messages.create(
        model=MODEL,
        max_tokens=2000,
        messages=[{"role": "user", "content": [
            image_block(REFERENCE_PNG, "image/png"),
            image_block(diagram, "image/jpeg"),
            {"type": "text", "text": prompt},
        ]}],
    )
    return msg.content[0].text


def run_strategy_c(diagram: Path) -> str:
    prompt_file = (PROMPTS / "strategy_c_describe.txt").read_text()
    step1_prompt, step2_prompt = prompt_file.split("STEP 2 PROMPT:", 1)
    step1_prompt = step1_prompt.replace("STEP 1 PROMPT:", "").strip()

    step1 = client().messages.create(
        model=MODEL,
        max_tokens=1500,
        messages=[{"role": "user", "content": [
            image_block(diagram, "image/jpeg"),
            {"type": "text", "text": step1_prompt},
        ]}],
    )
    description = step1.content[0].text

    step2_full = f"{step2_prompt.strip()}\n{description}\n"
    step2 = client().messages.create(
        model=MODEL,
        max_tokens=2000,
        messages=[{"role": "user", "content": step2_full}],
    )
    return step2.content[0].text


STRATEGIES = [
    ("a", run_strategy_a),
    ("b", run_strategy_b),
    ("c", run_strategy_c),
]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    diagrams = sorted(DIAGRAMS_DIR.glob("*.jpg"))
    if not diagrams:
        raise SystemExit(f"No diagrams found in {DIAGRAMS_DIR}. Run `make rasterize` first.")

    for diagram in diagrams:
        diagram_id = diagram.stem
        print(f"\n=== {diagram_id} ===")

        for strategy_name, runner in STRATEGIES:
            print(f"  strategy {strategy_name}…", flush=True)
            try:
                output = runner(diagram)
                out_path = OUT_DIR / f"{diagram_id}_strategy_{strategy_name}.yaml"
                out_path.write_text(output)
                print(f"    → {out_path.name}")
            except Exception as e:  # noqa: BLE001 — log everything, never silence
                err_path = OUT_DIR / f"{diagram_id}_strategy_{strategy_name}.error.txt"
                err_path.write_text(f"{type(e).__name__}: {e}\n")
                print(f"    ✗ {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
