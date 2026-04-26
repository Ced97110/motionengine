"""Public drill-diagram endpoint.

Serves Tier B authored drill diagrams for the V7 viewer.

Reads from ``backend/eval/drill-diagrams-{spike,top50}/{slug}.json``. Both
folders together form the canonical drill-diagram corpus (54 court drills
as of 2026-04-26). The endpoint is read-only; new diagrams are authored by
the spike pipeline (see ``tier-b-drill-diagrams-shipped.md`` memory) and
committed to one of those folders.

Routes:

- ``GET /api/public/drills/{slug}/diagram`` — the structured DrillDiagram
  JSON for a drill, exactly as committed. The frontend's
  ``src/lib/drills/toV7Drill.ts`` adapter converts this into a V7Play the
  ``PlayViewerV7`` atom can render without LLM at request time.

Non-goals:

- Listing / search (use the wiki-pages endpoints for that).
- Authoring (offline pipeline only).
- Composing diagrams from drill MD on demand — too slow + non-deterministic.
"""

from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from motion.middleware.sport import current_sport
from motion.wiki_ops.paths import backend_root

router = APIRouter(prefix="/api/public/drills", tags=["public-drills"])


def _diagram_dirs() -> list[Path]:
    """Both top-50 and spike — concatenated lookup with top-50 first.

    The repo layout is ``<backend>/eval/drill-diagrams-{spike,top50}/``.
    Uses ``backend_root()`` directly so the path is sport-invariant and
    stable regardless of which sport wiki_dir() resolves to.
    """
    be_root = backend_root()
    return [
        be_root / "eval" / "drill-diagrams-top50",
        be_root / "eval" / "drill-diagrams-spike",
    ]


def _resolve_diagram_path(slug: str) -> Path | None:
    """Find ``{slug}.json`` across the canonical diagram dirs, else None."""
    for d in _diagram_dirs():
        candidate = d / f"{slug}.json"
        if candidate.exists():
            return candidate
    return None


@router.get("/{slug}/diagram")
def get_drill_diagram(slug: str, request: Request) -> JSONResponse:
    """Return the DrillDiagram JSON for a drill slug, or 404 if absent.

    The JSON is returned verbatim — schema is owned by the spike pipeline,
    consumer-side adapter at ``frontend/src/lib/drills/toV7Drill.ts`` does
    the V7 conversion.
    """
    # Resolve sport so requests carrying X-Motion-Sport are validated by
    # SportMiddleware (400 on invalid sport) before we look up the diagram.
    # The eval dirs are currently basketball-only; when football diagrams
    # land, sport will gate which corpus is searched.
    current_sport(request)

    # Defensive slug check — prevents path traversal via "../" or similar.
    # Drill slugs are kebab-case-only by repo convention.
    if not slug.replace("-", "").replace("_", "").isalnum():
        raise HTTPException(status_code=400, detail="invalid slug shape")

    path = _resolve_diagram_path(slug)
    if path is None:
        raise HTTPException(
            status_code=404,
            detail=f"no diagram for {slug!r} (try one of the 54 court drills "
            "under backend/eval/drill-diagrams-{spike,top50}/)",
        )

    try:
        diagram = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        # Corrupted committed JSON — should never happen given the spike
        # pipeline validates before write, but defensive.
        raise HTTPException(
            status_code=500,
            detail=f"corrupt diagram on disk: {exc}",
        ) from exc

    return JSONResponse(content=diagram)
