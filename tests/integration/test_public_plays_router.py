"""Integration tests for the public plays router.

Covers the consumer surface separately from ``playlab``:

- List endpoint hides IP-blocked slugs and no-geometry pages.
- Detail endpoint returns the full play + prose + related slugs.
- IP-blocked slug returns 404 even when the file exists (indistinguishable
  from "not found" — a public endpoint must not leak the distinction).
- Slug traversal is rejected with 400.
- Authoring-only ``todos`` / ``source`` fields never leak through.
"""
# ruff: noqa: E501  # Fixture strings embed single-line JSON blobs.

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from motion.routers import public_plays as public_plays_router_module
from motion.services import wiki_importer
from motion.wiki_ops import paths as paths_module

SAMPLE_PAGE = """---
type: play
category: offense
tags: [ram-screen]
---

# Sample

## Overview
A straightforward wing entry → PnR play.

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":33},{"role":"2","x":-18,"y":22}],"ballStart":"1","actions":[{"from":"1","to":"2","type":"pass"}],"notes":"Phase 1."}
```

## Phases

### Phase 1: Entry
- 1 passes to 2.

## Key Coaching Points
- Keep spacing tight on the entry pass.
- 5 must sprint on the screen. [S4, p.75]

## Related Plays
- [[play-other]]
- [[concept-setting-screens]]

## Sources
- [S4, p.74]
"""


NO_DIAGRAM_PAGE = """---
type: play
category: offense
---

# Prose-Only

## Overview
No geometry yet.

### Phase 1: Stub
- Just text.

## Sources
- [Sx, p.1]
"""


IP_BLOCKED_PAGE = """---
type: play
category: offense
---

# Forbidden

## Overview
IP-leaking slug; must be suppressed.

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":33}],"actions":[],"notes":"Phase 1."}
```

## Phases

### Phase 1: Only
- Stub.
"""


@pytest.fixture
def tmp_wiki(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Throwaway wiki dir; patch every consumer to point at it."""
    wiki = tmp_path / "wiki"
    wiki.mkdir()
    monkeypatch.setattr(paths_module, "wiki_dir", lambda: wiki)
    monkeypatch.setattr(wiki_importer, "wiki_dir", lambda: wiki)
    monkeypatch.setattr(public_plays_router_module, "wiki_dir", lambda: wiki)
    return wiki


@pytest.fixture
def client(tmp_wiki: Path) -> Iterator[TestClient]:
    # `tmp_wiki` is a dependency so pytest applies the wiki-dir monkeypatches
    # before the TestClient is built; its value is unused here but the
    # ordering matters.
    del tmp_wiki
    app = FastAPI()
    app.include_router(public_plays_router_module.router)
    with TestClient(app) as test_client:
        yield test_client


def _write(wiki: Path, slug: str, body: str) -> None:
    (wiki / f"{slug}.md").write_text(body, encoding="utf-8")


# ---------------------------------------------------------------------------
# /api/public/plays — list
# ---------------------------------------------------------------------------


def test_list_returns_renderable_plays(client: TestClient, tmp_wiki: Path) -> None:
    _write(tmp_wiki, "play-sample", SAMPLE_PAGE)
    _write(tmp_wiki, "play-prose-only", NO_DIAGRAM_PAGE)

    response = client.get("/api/public/plays")
    assert response.status_code == 200, response.text
    entries = response.json()
    slugs = [e["slug"] for e in entries]
    assert "play-sample" in slugs
    # No-geometry pages suppressed from the gallery.
    assert "play-prose-only" not in slugs


def test_list_hides_ip_blocked_slugs(client: TestClient, tmp_wiki: Path) -> None:
    _write(tmp_wiki, "play-sample", SAMPLE_PAGE)
    _write(tmp_wiki, "play-celtics-x-action", IP_BLOCKED_PAGE)

    response = client.get("/api/public/plays")
    slugs = [e["slug"] for e in response.json()]
    assert "play-sample" in slugs
    assert "play-celtics-x-action" not in slugs


def test_list_entry_shape_matches_pydantic_model(client: TestClient, tmp_wiki: Path) -> None:
    _write(tmp_wiki, "play-sample", SAMPLE_PAGE)
    entries = client.get("/api/public/plays").json()
    assert entries, "fixture should produce at least one entry"
    entry = entries[0]
    # Response uses camelCase per the _CamelModel alias.
    assert set(entry.keys()) == {
        "slug",
        "name",
        "tag",
        "phaseCount",
        "tags",
        "formation",
        "defendsAgainst",
    }
    assert entry["phaseCount"] >= 1
    # Filter facets default to safe empties when front-matter omits them.
    assert isinstance(entry["tags"], list)
    assert isinstance(entry["defendsAgainst"], list)


def test_list_includes_facets_from_frontmatter(
    client: TestClient, tmp_wiki: Path
) -> None:
    """Tag list + formation + defendsAgainst surface from front-matter / sidecar."""
    page_with_facets = SAMPLE_PAGE.replace(
        "tags: [ram-screen]",
        "tags: [ram-screen, pick-and-roll, half-court]",
    ).replace(
        "category: offense",
        "category: offense\nformation: 1-4-high",
    )
    _write(tmp_wiki, "play-faceted", page_with_facets)
    # Inject a compiled play-to-defending sidecar pointing at this slug.
    compiled = tmp_wiki / "compiled"
    compiled.mkdir(exist_ok=True)
    (compiled / "play-to-defending.json").write_text(
        '{"play-faceted": ['
        '{"defending": "defending-flash-post", "shared_tags": ["pick-and-roll", "high-post", "horns"]},'
        '{"defending": "defending-drop-one", "shared_tags": ["pick-and-roll", "high-post"]},'
        '{"defending": "defending-cross-four-get", "shared_tags": ["cross-screen"]}'
        ']}',
        encoding="utf-8",
    )
    entries = client.get("/api/public/plays").json()
    entry = next(e for e in entries if e["slug"] == "play-faceted")
    assert entry["formation"] == "1-4-high"
    assert "pick-and-roll" in entry["tags"]
    # Top-2 cap: highest shared-tag count first, the third entry drops off.
    assert [d["slug"] for d in entry["defendsAgainst"]] == [
        "defending-flash-post",
        "defending-drop-one",
    ]
    # Display names mirror the FE defendingDisplayName transform.
    assert entry["defendsAgainst"][0]["displayName"] == "Flash Post"
    assert entry["defendsAgainst"][1]["displayName"] == "Drop One"


def test_facet_labels_are_ip_safe(client: TestClient, tmp_wiki: Path) -> None:
    """defendsAgainst displayNames must never leak IP-blocked fragments.

    A bug in compiled crossref data could ship a defending slug that
    embeds a team token (e.g. ``defending-celtics-flash``). The list
    endpoint must scrub those rather than rendering a chip with the
    forbidden word.
    """
    _write(tmp_wiki, "play-sample", SAMPLE_PAGE)
    compiled = tmp_wiki / "compiled"
    compiled.mkdir(exist_ok=True)
    (compiled / "play-to-defending.json").write_text(
        '{"play-sample": ['
        '{"defending": "defending-celtics-flash", "shared_tags": ["ram-screen"]}'
        ']}',
        encoding="utf-8",
    )
    entries = client.get("/api/public/plays").json()
    entry = next(e for e in entries if e["slug"] == "play-sample")
    for d in entry["defendsAgainst"]:
        lowered = d["displayName"].lower() + " " + d["slug"].lower()
        for fragment in ("celtics", "lakers", "knicks"):
            assert fragment not in lowered, (
                f"defending facet leaked IP fragment '{fragment}': {d}"
            )


# ---------------------------------------------------------------------------
# /api/public/plays/{slug} — detail
# ---------------------------------------------------------------------------


def test_detail_returns_play_prose_and_related(
    client: TestClient, tmp_wiki: Path
) -> None:
    _write(tmp_wiki, "play-sample", SAMPLE_PAGE)
    response = client.get("/api/public/plays/play-sample")
    assert response.status_code == 200, response.text
    body = response.json()

    assert body["slug"] == "play-sample"
    assert body["name"] == "Sample"
    assert body["tag"] == "offense"
    # V7Play shape.
    assert body["play"]["ballStart"] == "1"
    assert len(body["play"]["phases"]) == 1
    # Prose sections populated.
    assert "wing entry" in body["prose"]["overview"].lower()
    assert "sprint" in body["prose"]["coachingPoints"].lower()
    # Citations are stripped from coaching points.
    assert "[S4" not in body["prose"]["coachingPoints"]
    # Related wikilinks surfaced.
    assert "play-other" in body["related"]
    assert "concept-setting-screens" in body["related"]


def test_detail_strips_authoring_fields(client: TestClient, tmp_wiki: Path) -> None:
    _write(tmp_wiki, "play-sample", SAMPLE_PAGE)
    body = client.get("/api/public/plays/play-sample").json()
    # The importer's tier + TODO list must not surface on the public API.
    assert "todos" not in body
    assert "source" not in body
    # Also absent from the nested play dict.
    assert "todos" not in body["play"]
    assert "source" not in body["play"]


def test_detail_404_on_ip_blocked_slug(client: TestClient, tmp_wiki: Path) -> None:
    _write(tmp_wiki, "play-celtics-x-action", IP_BLOCKED_PAGE)
    response = client.get("/api/public/plays/play-celtics-x-action")
    assert response.status_code == 404


def test_detail_404_on_missing_slug(client: TestClient) -> None:
    response = client.get("/api/public/plays/play-does-not-exist")
    assert response.status_code == 404


def test_detail_400_on_traversal(client: TestClient) -> None:
    response = client.get("/api/public/plays/..escape")
    assert response.status_code == 400


def test_detail_404_when_page_has_no_geometry(
    client: TestClient, tmp_wiki: Path
) -> None:
    _write(tmp_wiki, "play-prose-only", NO_DIAGRAM_PAGE)
    response = client.get("/api/public/plays/play-prose-only")
    assert response.status_code == 404


def test_detail_coaching_points_fallback_is_empty(
    client: TestClient, tmp_wiki: Path
) -> None:
    """A page without a '## Key Coaching Points' section returns empty string."""
    no_kp = SAMPLE_PAGE.replace(
        "## Key Coaching Points\n- Keep spacing tight on the entry pass.\n- 5 must sprint on the screen. [S4, p.75]\n\n",
        "",
    )
    _write(tmp_wiki, "play-nopoints", no_kp)
    body = client.get("/api/public/plays/play-nopoints").json()
    assert body["prose"]["coachingPoints"] == ""
    # Overview still surfaces.
    assert body["prose"]["overview"]
