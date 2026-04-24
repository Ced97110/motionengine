"""User-facing wiki page endpoint.

Read-only minimal view of any concept / drill / exercise / defending page.
Mirrors ``public_plays.py``'s shape (IP scrub, traversal guard, fields
stripped) but for the non-play page types. Powers the click-through from
the play-detail chain panel: drill slugs → drill page, anatomy regions →
concept-anatomy page.

Non-goals (deliberate, mirror parent CLAUDE.md "wiki is a retrieval layer
not a browsable surface"):

- No listing endpoint — discovery happens via the Engine / chain panel,
  not via "browse all concepts."
- No search. No filters. No edit.
- No traversal of arbitrary paths — slug must be a single filename stem.
"""

from __future__ import annotations

import re
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from motion.routers.public_plays import _is_ip_safe_slug
from motion.wiki_ops.frontmatter import parse_full
from motion.wiki_ops.paths import wiki_dir

# Pages we expose. ``play-*`` is intentionally excluded — those have
# their own richer detail endpoint at ``/api/public/plays/{slug}``.
_ALLOWED_PREFIXES: tuple[str, ...] = (
    "concept-",
    "drill-",
    "exercise-",
    "defending-",
)

# Same citation-strip pattern used in ``public_plays``. We don't want
# `[S4, p.66]` flooding the consumer body.
_SOURCE_CITATION_RE = re.compile(r"\s*\[S\d+,?[^\]]*\]")


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class PublicWikiPage(_CamelModel):
    slug: str
    type: str
    title: str
    body: str
    tags: list[str] = []


router = APIRouter(prefix="/api/public/wiki", tags=["public-wiki"])


def _resolve_safe_path(slug: str) -> Path:
    """Block path traversal — slug must be a bare filename stem."""
    if Path(slug).name != slug or slug.startswith("."):
        raise HTTPException(status_code=400, detail="invalid slug")
    if not any(slug.startswith(p) for p in _ALLOWED_PREFIXES):
        # Don't expose play-* via this endpoint; force callers to the
        # richer ``/api/public/plays/{slug}`` surface.
        raise HTTPException(status_code=404, detail=f"page not found: {slug}")
    root = wiki_dir()
    target = (root / f"{slug}.md").resolve()
    if root.resolve() not in target.parents:
        raise HTTPException(status_code=400, detail="invalid slug")
    return target


def _extract_title(body: str, slug: str) -> str:
    """Pull the first-level heading from the body, fall back to the slug."""
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return slug


def _strip_citations(body: str) -> str:
    return _SOURCE_CITATION_RE.sub("", body)


def _extract_tags(fm: dict) -> list[str]:
    raw = fm.get("tags")
    if not isinstance(raw, list):
        return []
    return [t.strip() for t in raw if isinstance(t, str) and t.strip()]


@router.get("/{slug}", response_model=PublicWikiPage)
async def wiki_page(slug: str) -> PublicWikiPage:
    if not _is_ip_safe_slug(slug):
        # 404 not 403 so the public surface doesn't leak the distinction
        # between "blocked" and "doesn't exist."
        raise HTTPException(status_code=404, detail=f"page not found: {slug}")
    target = _resolve_safe_path(slug)
    if not target.is_file():
        raise HTTPException(status_code=404, detail=f"page not found: {slug}")

    raw = target.read_text(encoding="utf-8")
    fm, body = parse_full(raw)
    page_type = str(fm.get("type", "")) or _infer_type(slug)
    title = _extract_title(body, slug)
    return PublicWikiPage(
        slug=slug,
        type=page_type,
        title=title,
        body=_strip_citations(body),
        tags=_extract_tags(fm),
    )


def _infer_type(slug: str) -> str:
    for prefix, label in (
        ("concept-", "concept"),
        ("drill-", "drill"),
        ("exercise-", "drill"),
        ("defending-", "defending"),
    ):
        if slug.startswith(prefix):
            return label
    return "page"
