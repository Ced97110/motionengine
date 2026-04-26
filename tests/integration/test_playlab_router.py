"""Integration tests for the playlab HTTP endpoints — focused on the
``save-to-wiki`` write-back path.

Covers:
- Preview mode returns a diff + warnings without touching the file system.
- Write mode persists new markdown to disk.
- Slug traversal is rejected with 400.
- Missing slug returns 404.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from motion.routers import playlab as playlab_router
from motion.services import wiki_importer
from motion.wiki_ops import paths as paths_module


SAMPLE_PAGE = """---
type: play
category: offense
---

# Sample

## Overview
Prose for the sample play.

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":33},{"role":"2","x":-18,"y":22},{"role":"3","x":18,"y":22},{"role":"4","x":-8,"y":29},{"role":"5","x":8,"y":29}],"actions":[{"from":"1","to":"2","type":"pass"}],"notes":"Phase 1."}
```

## Phases

### Phase 1: Entry
- 1 passes to 2.

## Sources
- [Sx, p.1]
"""


@pytest.fixture
def tmp_wiki(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Create a throwaway wiki dir and point every consumer at it.

    ``wiki_ops.paths.wiki_dir`` is the canonical resolver; ``wiki_importer``
    imports it by name so we patch both bindings to keep independent
    module namespaces consistent.
    """
    wiki = tmp_path / "wiki"
    wiki.mkdir()
    monkeypatch.setattr(paths_module, "wiki_dir", lambda *_a, **_k: wiki)
    monkeypatch.setattr(wiki_importer, "wiki_dir", lambda *_a, **_k: wiki)
    # The router imports wiki_dir at module load time — patch there too.
    monkeypatch.setattr(playlab_router, "wiki_dir", lambda *_a, **_k: wiki)
    return wiki


@pytest.fixture
def client(tmp_wiki: Path) -> Iterator[TestClient]:  # noqa: ARG001
    app = FastAPI()
    app.include_router(playlab_router.router)
    with TestClient(app) as test_client:
        yield test_client


def _sample_play() -> dict:
    return {
        "name": "Sample",
        "tag": "offense",
        "desc": "",
        "coachNote": "",
        "concepts": {"counters": [], "bestFor": "", "related": []},
        "players": {
            "1": [0, 33],
            "2": [-18, 22],
            "3": [18, 22],
            "4": [-8, 29],
            "5": [8, 29],
        },
        "roster": {},
        "defense": {},
        "ballStart": "1",
        "phases": [
            {
                "label": "Entry",
                "text": "- 1 passes to 2.",
                "actions": [
                    {
                        "marker": "arrow",
                        "dashed": True,
                        "path": "M 0 33 C 2 28 -8 24 -18 22",
                        "ball": {"from": "1", "to": "2"},
                    }
                ],
                "defenseActions": [],
            }
        ],
        "branchPoint": None,
    }


# ---------------------------------------------------------------------------
# save-to-wiki — preview mode
# ---------------------------------------------------------------------------


def test_preview_returns_diff_without_writing(
    client: TestClient, tmp_wiki: Path
) -> None:
    page = tmp_wiki / "play-sample.md"
    page.write_text(SAMPLE_PAGE, encoding="utf-8")
    original_bytes = page.read_bytes()

    response = client.post(
        "/api/playlab/save-to-wiki/play-sample",
        json={"play": _sample_play(), "mode": "preview"},
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert isinstance(body["diff"], str)
    assert body["diff"]  # non-empty — the writer's output differs from the fixture.
    assert body["warnings"] == []
    assert body.get("path") is None
    assert body.get("bytesWritten") is None

    # File was NOT touched.
    assert page.read_bytes() == original_bytes


def test_preview_import_then_save_is_semantically_idempotent(
    client: TestClient, tmp_wiki: Path
) -> None:
    """import → save (write) → import produces the same V7Play.

    This is the HTTP-level mirror of ``test_wiki_roundtrip``: the save
    endpoint may rewrite the fixture's compact JSON to pretty-printed form
    (non-empty diff), but the SEMANTIC content round-trips. That is the
    invariant we care about at the API boundary.
    """
    page = tmp_wiki / "play-sample.md"
    page.write_text(SAMPLE_PAGE, encoding="utf-8")

    first = client.get("/api/playlab/import-wiki/play-sample").json()["play"]
    client.post(
        "/api/playlab/save-to-wiki/play-sample",
        json={"play": first, "mode": "write"},
    ).raise_for_status()
    second = client.get("/api/playlab/import-wiki/play-sample").json()["play"]
    assert first == second


# ---------------------------------------------------------------------------
# save-to-wiki — write mode
# ---------------------------------------------------------------------------


def test_write_persists_new_markdown(client: TestClient, tmp_wiki: Path) -> None:
    page = tmp_wiki / "play-sample.md"
    page.write_text(SAMPLE_PAGE, encoding="utf-8")

    play = _sample_play()
    # Mutate the played path so the diff is non-trivial — writer must reflect it.
    play["phases"][0]["actions"][0]["path"] = "M 0 33 L -18 22"

    response = client.post(
        "/api/playlab/save-to-wiki/play-sample",
        json={"play": play, "mode": "write"},
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["path"].endswith("/play-sample.md")
    assert body["bytesWritten"] is None or body["bytesWritten"] >= 0
    # File reflects the new path.
    assert "M 0 33 L -18 22" in page.read_text(encoding="utf-8")
    # Non-diagram content still intact.
    assert "## Overview\nProse for the sample play." in page.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# error paths
# ---------------------------------------------------------------------------


def test_save_rejects_traversal_slug(client: TestClient) -> None:
    response = client.post(
        "/api/playlab/save-to-wiki/..escape",
        json={"play": _sample_play(), "mode": "preview"},
    )
    assert response.status_code == 400


def test_save_rejects_missing_slug(client: TestClient) -> None:
    response = client.post(
        "/api/playlab/save-to-wiki/play-does-not-exist",
        json={"play": _sample_play(), "mode": "preview"},
    )
    assert response.status_code == 404
