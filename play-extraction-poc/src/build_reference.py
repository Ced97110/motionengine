"""Render data/reference-court.svg → data/reference-court.png at 1200 px wide."""
from __future__ import annotations

import os
import sys
from pathlib import Path

# Homebrew on Apple Silicon keeps libcairo under /opt/homebrew/lib and cairocffi
# does not search there by default. Prepend it so `import cairosvg` succeeds.
if sys.platform == "darwin":
    homebrew_lib = "/opt/homebrew/lib"
    existing = os.environ.get("DYLD_FALLBACK_LIBRARY_PATH", "")
    if homebrew_lib not in existing.split(":"):
        os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = (
            f"{homebrew_lib}:{existing}" if existing else homebrew_lib
        )

HERE = Path(__file__).resolve().parent.parent
SVG = HERE / "data" / "reference-court.svg"
PNG = HERE / "data" / "reference-court.png"


def main() -> None:
    if not SVG.exists():
        raise SystemExit(f"Missing {SVG}")
    try:
        import cairosvg
    except (ImportError, OSError) as e:
        raise SystemExit(
            f"Could not load cairosvg/libcairo: {e}\n"
            "Fix: `brew install cairo` (macOS) or `apt-get install libcairo2` (Debian)."
        )
    cairosvg.svg2png(url=str(SVG), write_to=str(PNG), output_width=1200)
    print(f"→ {PNG}")


if __name__ == "__main__":
    main()
