"""Repo-root, wiki, raw-PDF, and frontend-src path resolution.

The Python ports run from ``backend/`` rather than ``frontend/`` (which
is where the TS originals ran), so they resolve paths relative to the
repo root rather than ``process.cwd()``. The helpers here centralize
that resolution and mirror the TS behavior of preferring
``../backend/knowledge-base/wiki`` as the canonical wiki directory.

Resolution order (wiki_dir):

1. Explicit override (``MOTION_WIKI_DIR`` environment variable or the
   ``--wiki-dir`` CLI flag where supported).
2. ``<repo_root>/backend/knowledge-base/wiki`` — sibling-dev layout.
3. ``<repo_root>/knowledge-base/wiki`` — legacy single-repo layout.

Raw PDF resolution is simpler: ``<repo_root>/backend/knowledge-base/raw``
unless ``MOTION_WIKI_RAW_DIR`` is set.
"""

from __future__ import annotations

import os
from pathlib import Path


def repo_root() -> Path:
    """Return the Motion repo root (the ``motion/`` directory).

    The package file lives at
    ``<repo>/backend/src/motion/wiki_ops/paths.py``. Four ``parent`` hops
    (``paths.py`` → ``wiki_ops`` → ``motion`` → ``src`` → ``backend``)
    land on ``backend``; one more lands on the repo root.
    """
    return Path(__file__).resolve().parents[4]


def backend_root() -> Path:
    """Return the ``backend/`` directory inside the repo."""
    return repo_root() / "backend"


def frontend_root() -> Path:
    """Return the ``frontend/`` directory inside the repo."""
    return repo_root() / "frontend"


def wiki_dir(override: str | os.PathLike[str] | None = None) -> Path:
    """Resolve the wiki directory.

    ``override`` takes precedence, followed by ``MOTION_WIKI_DIR``,
    followed by the two canonical fallbacks. Unlike
    ``frontend/src/lib/wiki-loader.ts`` this helper does not swallow
    missing directories — callers must handle the "no wiki" error case.
    """
    if override is not None:
        return Path(override).resolve()
    env = os.environ.get("MOTION_WIKI_DIR")
    if env:
        return Path(env).resolve()
    sibling = backend_root() / "knowledge-base" / "wiki"
    if sibling.is_dir():
        return sibling
    legacy = repo_root() / "knowledge-base" / "wiki"
    return legacy


def raw_pdf_dir(override: str | os.PathLike[str] | None = None) -> Path:
    """Resolve the raw PDF directory."""
    if override is not None:
        return Path(override).resolve()
    env = os.environ.get("MOTION_WIKI_RAW_DIR")
    if env:
        return Path(env).resolve()
    return backend_root() / "knowledge-base" / "raw"


def frontend_plays_dir() -> Path:
    """Return ``frontend/src/data/plays``."""
    return frontend_root() / "src" / "data" / "plays"


def frontend_review_dir() -> Path:
    """Return ``frontend/src/data/plays/_review``."""
    return frontend_plays_dir() / "_review"


def frontend_src_dir() -> Path:
    """Return ``frontend/src`` — scanned by check-nba-terms."""
    return frontend_root() / "src"
