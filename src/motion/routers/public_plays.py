"""User-facing play endpoints.

Read-only public shape derived from the wiki. Separate from
``/api/playlab/*`` (the maintainer authoring surface) so consumer pages
can evolve independently of the lab, and so IP scrubbing + field
stripping live in one place.

Routes:

- ``GET /api/public/plays`` — list every renderable play as
  ``{slug, name, tag, phaseCount, tags, formation, defendsAgainst}``.
  IP-leaking slugs are filtered.
- ``GET /api/public/plays/{slug}`` — detail: the V7Play + narrative
  prose sections (overview, coaching points) + related slugs. The
  authoring-only ``todos`` / ``source`` fields from the importer are
  stripped so they can't leak into consumer surfaces.

Non-goals (per the approved plan):

- Search / filter.
- Tier gating.
- Write paths (use ``/api/playlab/save-to-wiki/{slug}`` for that).
"""

from __future__ import annotations

import json
import re
from typing import Any, TypedDict

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from motion.middleware.sport import current_sport
from motion.services.wiki_importer import (
    _resolve_wiki_path,
    import_wiki_play,
    list_importable_wiki_plays,
)
from motion.sports import Sport
from motion.wiki_ops.frontmatter import parse_full
from motion.wiki_ops.paths import wiki_dir

# ---------------------------------------------------------------------------
# IP blocklist
# ---------------------------------------------------------------------------
#
# Parent ``CLAUDE.md`` mandates: no NBA team / player / institution names on
# public surfaces. Some existing wiki slugs leak those (e.g.
# ``play-celtics-x-action``). The real fix is a corpus-wide slug rename
# pass; until then, hide offending slugs from this consumer-facing API.
#
# Additive list — append new fragments as they're discovered. Matching is
# case-insensitive substring on the slug ("play-" prefix is already part of
# the slug, so fragments below are the TEAM / LOCATION tokens only).
# ---------------------------------------------------------------------------

_IP_BLOCKED_FRAGMENTS: frozenset[str] = frozenset({
    "celtics",
    "lakers",
    "knicks",
    "utah-jazz",
    "san-antonio",
    "philadelphia",
    "new-jersey",
    "charlotte",
    "orlando",
    "detroit",
})


def _is_ip_safe_slug(slug: str) -> bool:
    lowered = slug.lower()
    return not any(frag in lowered for frag in _IP_BLOCKED_FRAGMENTS)


# ---------------------------------------------------------------------------
# Coaching-points extraction
# ---------------------------------------------------------------------------
#
# The importer already surfaces overview prose (``play.desc``) and related
# slugs (``play.concepts.related``). Coaching points live in ``## Key
# Coaching Points`` but the importer doesn't extract them — adding the
# parse here avoids perturbing the authoring contract.
# ---------------------------------------------------------------------------

_COACHING_SECTION_RE = re.compile(
    r"^##\s+Key\s+Coaching\s+Points\s*\n(?P<body>[\s\S]*?)(?=^##\s|\Z)",
    re.MULTILINE,
)
_SOURCE_CITATION_RE = re.compile(r"\s*\[S\d+,[^\]]*\]")


def _extract_coaching_points(body: str) -> str:
    """Pull the ``## Key Coaching Points`` section body, citations stripped.

    Returns an empty string when the section is absent. Preserves the
    bullet-list formatting as authored so the frontend can render it
    verbatim with a standard markdown renderer (or raw `<pre>`).
    """
    match = _COACHING_SECTION_RE.search(body)
    if match is None:
        return ""
    text = match.group("body").strip()
    return _SOURCE_CITATION_RE.sub("", text).strip()


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class DefendsEntry(_CamelModel):
    slug: str
    display_name: str
    shared_tags: list[str]


class PublicPlayListEntry(_CamelModel):
    slug: str
    name: str
    tag: str
    phase_count: int
    tags: list[str] = []
    formation: str | None = None
    defends_against: list[DefendsEntry] = []


class PublicPlayProse(_CamelModel):
    overview: str
    coaching_points: str


class FormationSibling(_CamelModel):
    slug: str
    name: str


class ChainTechnique(_CamelModel):
    id: str
    role: str
    criticality: str


class ChainAnatomy(_CamelModel):
    region: str
    criticality: str
    supports_technique: str
    for_role: str


class ChainDrill(_CamelModel):
    slug: str
    region: str
    emphasis: str


class PlayChain(_CamelModel):
    techniques: list[ChainTechnique] = []
    anatomy: list[ChainAnatomy] = []
    drills: list[ChainDrill] = []


class PublicPlayDetail(_CamelModel):
    slug: str
    name: str
    tag: str
    play: dict[str, Any]
    prose: PublicPlayProse
    related: list[str]
    formation: str | None = None
    formation_siblings: list[FormationSibling] = []
    chain: PlayChain = PlayChain()


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------


router = APIRouter(prefix="/api/public/plays", tags=["public-plays"])


@router.get("", response_model=list[PublicPlayListEntry])
async def list_plays(request: Request) -> list[PublicPlayListEntry]:
    """List every IP-safe play page with renderable geometry."""
    sport: Sport = current_sport(request)
    entries = list_importable_wiki_plays(sport=sport)
    play_to_defending = _load_compiled_index("play-to-defending.json", sport=sport)
    out: list[PublicPlayListEntry] = []
    for e in entries:
        slug = e["slug"]
        if not _is_ip_safe_slug(slug):
            continue
        # Suppress pages with no diagram blocks — detail endpoint would
        # 404 on them, so hiding from the list gives a cleaner gallery.
        if not e.get("hasDiagram"):
            continue
        facets = _read_facets_from_file(slug, sport=sport)
        out.append(
            PublicPlayListEntry(
                slug=slug,
                name=e["name"],
                tag=facets["tag"],
                phase_count=e["phaseCount"],
                tags=facets["tags"],
                formation=facets["formation"],
                defends_against=_top_defending(slug, play_to_defending),
            )
        )
    return out


@router.get("/{slug}", response_model=PublicPlayDetail)
async def play_detail(slug: str, request: Request) -> PublicPlayDetail:
    """Return a renderable V7Play + narrative prose for ``slug``."""
    sport: Sport = current_sport(request)
    try:
        root = wiki_dir(sport=sport)
        path = _resolve_wiki_path(slug, root)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not _is_ip_safe_slug(slug):
        # Treat blocked slugs as "not found" — the client should never see
        # the distinction between "doesn't exist" and "suppressed for IP"
        # on a public endpoint.
        raise HTTPException(status_code=404, detail=f"play not found: {slug}")
    if not path.is_file():
        raise HTTPException(status_code=404, detail=f"play not found: {slug}")

    result = import_wiki_play(slug, sport=sport)
    if result.play is None:
        raise HTTPException(
            status_code=404,
            detail=f"{slug} has no renderable geometry",
        )

    # Strip authoring-only fields before emitting to the consumer surface.
    # `todos` / `source` tier are maintainer signals and leaking them would
    # confuse non-author viewers.
    play_payload = dict(result.play)

    raw_md = path.read_text(encoding="utf-8")
    fm, body = parse_full(raw_md)
    coaching_points = _extract_coaching_points(body)
    overview = play_payload.get("desc") or ""
    related_raw = play_payload.get("concepts", {}).get("related", [])
    related = [r for r in related_raw if isinstance(r, str) and r]

    formation = _formation_from_fm(fm)
    siblings = _formation_siblings(slug, formation, sport=sport)
    chain = _play_chain(slug, sport=sport)

    return PublicPlayDetail(
        slug=slug,
        name=str(play_payload.get("name") or slug),
        tag=str(play_payload.get("tag") or ""),
        play=play_payload,
        prose=PublicPlayProse(
            overview=overview,
            coaching_points=coaching_points,
        ),
        related=related,
        formation=formation,
        formation_siblings=siblings,
        chain=chain,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Formation siblings (UX signal)
# ---------------------------------------------------------------------------
#
# Compiled sidecar ``wiki/compiled/formation-graph.json`` maps formation →
# [slug...]. Reading it per-request keeps siblings fresh when the wiki is
# recompiled between process restarts; the file is a few KB and the parse
# is trivial. Siblings are filtered against the IP blocklist and the
# renderable-geometry set so chips never deep-link to 404s.
# ---------------------------------------------------------------------------


def _formation_from_fm(fm: dict[str, Any]) -> str | None:
    val = fm.get("formation")
    if isinstance(val, str):
        stripped = val.strip()
        if stripped:
            return stripped
    return None


def _load_formation_graph(*, sport: Sport) -> dict[str, list[str]]:
    path = wiki_dir(sport=sport) / "compiled" / "formation-graph.json"
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    if not isinstance(data, dict):
        return {}
    out: dict[str, list[str]] = {}
    for k, v in data.items():
        if isinstance(k, str) and isinstance(v, list):
            out[k] = [s for s in v if isinstance(s, str)]
    return out


def _formation_siblings(
    this_slug: str, formation: str | None, *, sport: Sport
) -> list[FormationSibling]:
    if not formation:
        return []
    graph = _load_formation_graph(sport=sport)
    candidate_slugs = graph.get(formation, [])
    if not candidate_slugs:
        return []
    # Use the importable-plays list as the source of `name` and as the
    # renderability filter — any sibling missing from this set either isn't
    # a ``type: play`` page or has no diagram geometry, so its detail page
    # would 404. Chips should never deep-link into a dead end.
    renderable = {
        p["slug"]: p["name"]
        for p in list_importable_wiki_plays(sport=sport)
        if p.get("hasDiagram")
    }
    out: list[FormationSibling] = []
    for sib_slug in candidate_slugs:
        if sib_slug == this_slug:
            continue
        if not _is_ip_safe_slug(sib_slug):
            continue
        name = renderable.get(sib_slug)
        if name is None:
            continue
        out.append(FormationSibling(slug=sib_slug, name=name))
    return out


# ---------------------------------------------------------------------------
# Cross-reference chain (the moat surface)
# ---------------------------------------------------------------------------
#
# Reads three compiled sidecars per request:
#   - play-to-technique.json   — what techniques each role needs
#   - play-to-anatomy.json     — what body regions each role loads
#   - anatomy-to-drill.json    — drills that train each region
#
# Drill suggestions come from joining the anatomy list against the
# anatomy-to-drill index (deduped by drill slug, keeps highest emphasis).
# Technique→drill exists in the corpus but is sparse (3 edges as of
# 2026-04-23) so we don't surface it yet — anatomy→drill is the load-bearing
# path.
# ---------------------------------------------------------------------------


def _load_compiled_index(name: str, *, sport: Sport) -> dict[str, Any]:
    path = wiki_dir(sport=sport) / "compiled" / name
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _play_chain(slug: str, *, sport: Sport) -> PlayChain:
    techniques_idx = _load_compiled_index("play-to-technique.json", sport=sport)
    anatomy_idx = _load_compiled_index("play-to-anatomy.json", sport=sport)
    drills_idx = _load_compiled_index("anatomy-to-drill.json", sport=sport)

    techniques: list[ChainTechnique] = []
    for entry in techniques_idx.get(slug, []):
        if not isinstance(entry, dict):
            continue
        try:
            techniques.append(
                ChainTechnique(
                    id=str(entry["id"]),
                    role=str(entry["role"]),
                    criticality=str(entry["criticality"]),
                )
            )
        except KeyError:
            continue

    anatomy: list[ChainAnatomy] = []
    seen_drills: dict[str, ChainDrill] = {}
    for entry in anatomy_idx.get(slug, []):
        if not isinstance(entry, dict):
            continue
        try:
            region = str(entry["region"])
            anatomy.append(
                ChainAnatomy(
                    region=region,
                    criticality=str(entry["criticality"]),
                    supports_technique=str(entry["supports_technique"]),
                    for_role=str(entry["for_role"]),
                )
            )
        except KeyError:
            continue
        # Suggest drills for this region. Keep first-seen entry per drill
        # slug so a drill listed under multiple regions doesn't appear twice.
        for drill_entry in drills_idx.get(region, []):
            if not isinstance(drill_entry, dict):
                continue
            drill_slug = drill_entry.get("drill")
            if not isinstance(drill_slug, str) or drill_slug in seen_drills:
                continue
            seen_drills[drill_slug] = ChainDrill(
                slug=drill_slug,
                region=region,
                emphasis=str(drill_entry.get("emphasis", "primary")),
            )

    return PlayChain(
        techniques=techniques,
        anatomy=anatomy,
        drills=list(seen_drills.values()),
    )


class _Facets(TypedDict):
    tag: str
    tags: list[str]
    formation: str | None


def _read_facets_from_file(slug: str, *, sport: Sport) -> _Facets:
    """Read ``tag``, ``tags``, and ``formation`` from front-matter in one pass.

    ``tag`` mirrors the historical single-string surface (category, falling
    back to the first ``tags`` entry). ``tags`` is the full list. ``formation``
    is the raw front-matter value or ``None``. Unreadable pages return safe
    empties rather than surfacing an error at list time.
    """
    root = wiki_dir(sport=sport)
    path = root / f"{slug}.md"
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError:
        return {"tag": "", "tags": [], "formation": None}
    fm, _ = parse_full(raw)
    raw_tags_field = fm.get("tags")
    tags: list[str] = []
    if isinstance(raw_tags_field, list):
        tags = [t.strip() for t in raw_tags_field if isinstance(t, str) and t.strip()]
    category = fm.get("category")
    tag = (
        category.strip()
        if isinstance(category, str) and category.strip()
        else (tags[0] if tags else "")
    )
    formation_raw = fm.get("formation")
    formation = (
        formation_raw.strip()
        if isinstance(formation_raw, str) and formation_raw.strip()
        else None
    )
    return {"tag": tag, "tags": tags, "formation": formation}


# ---------------------------------------------------------------------------
# Defending-edges enrichment
# ---------------------------------------------------------------------------
#
# ``play-to-defending.json`` (compiled by ``crossref.py``) maps each play
# slug to the defending pages that share at least one non-generic tag. The
# raw list can be 5+ entries for plays with broad action tags
# (e.g. ``cross-screen``); for the gallery facet we cap at the **top 2**
# matches sorted by shared-tag count, descending. Cap = 2 keeps the chip
# distribution tight (no defense ends up linked to 28 plays at once) and
# matches the M4 brief logic of "TOP match" referenced in the play-brief
# prompt.
# ---------------------------------------------------------------------------


def _defending_display_name(slug: str) -> str:
    """Mirror ``defendingDisplayName`` in ``frontend/src/lib/knowledge/display-names.ts``.

    ``defending-flash-post`` → ``Flash post``. Server-side derivation keeps
    the API self-describing so the FE doesn't import a slug-mapping table
    just to render a chip.
    """
    stripped = slug.removeprefix("defending-").replace("-", " ")
    if not stripped:
        return stripped
    # Title-case every word (matches the FE ``\b\w`` regex behaviour).
    return " ".join(word[:1].upper() + word[1:] for word in stripped.split())


def _top_defending(
    slug: str, play_to_defending: dict[str, Any]
) -> list[DefendsEntry]:
    raw = play_to_defending.get(slug, [])
    if not isinstance(raw, list):
        return []
    candidates: list[tuple[int, str, list[str]]] = []
    for entry in raw:
        if not isinstance(entry, dict):
            continue
        defending_slug = entry.get("defending") or entry.get("defending_slug")
        shared = entry.get("shared_tags")
        if not isinstance(defending_slug, str) or not defending_slug:
            continue
        if not isinstance(shared, list):
            continue
        # Defending slugs go through the same IP filter as plays — a stray
        # team-named defending page in compiled data must not surface as a
        # consumer-facing chip label.
        if not _is_ip_safe_slug(defending_slug):
            continue
        shared_clean = [s for s in shared if isinstance(s, str) and s]
        candidates.append((len(shared_clean), defending_slug, shared_clean))
    # Sort by (shared-tag count desc, slug asc) for determinism.
    candidates.sort(key=lambda c: (-c[0], c[1]))
    return [
        DefendsEntry(
            slug=defending_slug,
            display_name=_defending_display_name(defending_slug),
            shared_tags=shared_clean,
        )
        for _, defending_slug, shared_clean in candidates[:2]
    ]
