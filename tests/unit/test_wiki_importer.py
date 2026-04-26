"""Unit tests for :mod:`motion.services.wiki_importer`.

Covers all three outcome tiers plus the path-traversal guard.
"""
# ruff: noqa: E501  # Fixture strings embed single-line JSON blobs by design.

from __future__ import annotations

from pathlib import Path

import pytest

from motion.services import wiki_importer
from motion.services.wiki_importer import (
    _resolve_wiki_path,
    import_wiki_play,
    list_importable_wiki_plays,
)

# ---------------------------------------------------------------------------
# Wiki-dir pinning: redirect the importer at a synthetic wiki per test.
# ---------------------------------------------------------------------------


@pytest.fixture
def tmp_wiki(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Create an empty wiki dir and patch :func:`wiki_importer.wiki_dir`."""
    wiki = tmp_path / "wiki"
    wiki.mkdir()
    monkeypatch.setattr(wiki_importer, "wiki_dir", lambda *_a, **_k: wiki)
    return wiki


def _write_page(wiki: Path, slug: str, content: str) -> Path:
    path = wiki / f"{slug}.md"
    path.write_text(content, encoding="utf-8")
    return path


SINGLE_BLOCK_PAGE = """---
type: play
category: offense
formation: 5-out
tags: [quick-hitter]
---

# Black

## Overview
A quick man-to-man play from a 5-out formation. [S4, p.56]

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":33},{"role":"2","x":-18,"y":28},{"role":"3","x":18,"y":28},{"role":"4","x":-22,"y":42},{"role":"5","x":22,"y":42}],"actions":[{"from":"1","to":"2","type":"pass"},{"from":"4","to":"2","type":"screen"},{"from":"2","to":"rim","type":"dribble"},{"from":"5","to":"left_elbow","type":"cut"}],"notes":"Phase 1 and 2 combined."}
```

## Phases

### Phase 1: Wing Entry and Step-Up Screen
- 1 passes to 2.
- 4 steps up and sets a screen on 2's defender.

### Phase 2: Baseline Drive
- 2 rips through and drives baseline.

### Phase 3: Rotation and Finish
- 5 flashes into the key.
- Options: finish, kick to 3, or dump to 5.

## Related Plays
- [[play-step-up]]
- [[play-swinger]]

## Sources
- [S4, p.56]
"""


MULTI_BLOCK_PAGE = """---
type: play
category: offense
formation: 2-3 high-post
---

# High Split

## Overview
Pass-and-follow continuity from a 2-3 high-post set. [S7, p.123]

## Phases

### Phase 1: Entry
- 2 passes to 1; 5 flashes to the high-post elbow.
```json name=diagram-positions
{"players":[{"role":"1","x":-8,"y":36},{"role":"2","x":8,"y":36},{"role":"3","x":-22,"y":22},{"role":"4","x":20,"y":22},{"role":"5","x":8,"y":29}],"actions":[{"from":"2","to":"1","type":"pass"},{"from":"1","to":"5","type":"pass"}],"notes":"Phase 1 starting formation."}
```

### Phase 2: Split Options
- 1 follows the pass toward 5; 4 fakes a split and cuts backdoor.
```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":44},{"role":"2","x":-10,"y":38},{"role":"3","x":-22,"y":22},{"role":"4","x":20,"y":28},{"role":"5","x":10,"y":30}],"actions":[{"from":"5","to":"4","type":"pass"},{"from":"4","to":"rim","type":"cut"},{"from":"1","to":"5","type":"cut"}],"notes":"Phase 2 Option A."}
```

## Sources
- [S7, p.123]
"""


NO_DIAGRAM_PAGE = """---
type: play
category: offense
---

# Versus Triangle-and-Two

## Overview
Zone offense counter to the triangle-and-two defense.

## Phases

### Phase 1: Initial Ball Movement
- O1 passes to O5; O1 and O2 dive to the blocks.

## Sources
- [S13, p.255]
"""


# ---------------------------------------------------------------------------
# Core scenarios.
# ---------------------------------------------------------------------------


def test_single_block_play_imports_as_partial(
    tmp_wiki: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """One diagram block with three phase sections → ``wiki-partial``.

    The single block lands in exactly ONE phase (the one the notes reference,
    or the first phase if the block is unlabeled). Remaining phases stay
    empty so the user can author each one without first deduplicating
    identical action lists — duplicating produced confusing "same 5 actions
    in every phase" output.

    The narrative expander is stubbed to ``[]`` here so this test pins the
    pre-LLM baseline; the LLM-expansion path has its own coverage below.
    """
    monkeypatch.setattr(
        wiki_importer,
        "expand_phase_from_narrative",
        lambda *_args, **_kwargs: [],
    )
    _write_page(tmp_wiki, "play-black", SINGLE_BLOCK_PAGE)
    result = import_wiki_play("play-black")

    assert result.source == "wiki-partial"
    assert result.play is not None
    assert result.play["name"] == "Black"
    assert result.play["tag"] == "offense"
    assert "5-out formation" in result.play["desc"]
    assert result.play["concepts"]["related"] == ["play-step-up", "play-swinger"]

    players = result.play["players"]
    assert set(players.keys()) == {"1", "2", "3", "4", "5"}
    assert players["1"] == [0, 33]

    phases = result.play["phases"]
    assert len(phases) == 3
    # Exactly one phase populated; the other two empty with an explanatory TODO.
    populated = [p for p in phases if p["actions"]]
    empty = [p for p in phases if not p["actions"]]
    assert len(populated) == 1
    assert len(empty) == 2
    assert any("no diagram block aligned" in t.lower() for t in result.todos)
    # The populated phase still carries the full action conversion.
    first_actions = populated[0]["actions"]
    pass_actions = [a for a in first_actions if a.get("ball")]
    assert pass_actions and pass_actions[0]["ball"] == {"from": "1", "to": "2"}
    screens = [a for a in first_actions if a["marker"] == "screen"]
    assert screens, "expected at least one screen action"
    dribbles = [a for a in first_actions if a["marker"] == "dribble"]
    assert dribbles and dribbles[0]["move"]["id"] == "2"


def test_empty_phases_filled_by_llm_expander(
    tmp_wiki: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Empty phases call into ``expand_phase_from_narrative`` and inherit TODO.

    Stubs the expander so one unpopulated phase gets a single cut action; the
    importer must convert it via ``_convert_actions`` and tag a TODO noting
    the actions were LLM-expanded.
    """

    def fake_expander(
        phase_label: str,
        _text: str,
        player_ids: list[str],
        preceding_actions: list[dict[str, object]] | None = None,
        current_positions: dict[str, tuple[float, float]] | None = None,
    ) -> list[dict[str, str]]:
        # Empty phases get one fabricated action so we can assert end-to-end.
        assert "1" in player_ids
        assert preceding_actions is not None
        # Position context must be populated — the expander now uses this to
        # pick correct directional tokens. By the time the empty phase runs,
        # phase 1's structured actions have already advanced positions.
        assert current_positions is not None
        assert set(current_positions.keys()) >= {"1", "2", "3", "4", "5"}
        return [{"from": "2", "to": "right_wing", "type": "cut"}]

    monkeypatch.setattr(
        wiki_importer, "expand_phase_from_narrative", fake_expander
    )
    _write_page(tmp_wiki, "play-black", SINGLE_BLOCK_PAGE)
    result = import_wiki_play("play-black")

    assert result.source == "wiki-partial"
    assert result.play is not None
    phases = result.play["phases"]
    # All three phases must now carry at least one action (1 from block, 2
    # from LLM expansion).
    populated = [p for p in phases if p["actions"]]
    assert len(populated) == 3
    assert any("LLM-expanded" in t for t in result.todos)


def test_multi_block_play_imports_as_structured(tmp_wiki: Path) -> None:
    """Two phases + two phase-tagged blocks → ``wiki-structured``."""
    _write_page(tmp_wiki, "play-high-split-action", MULTI_BLOCK_PAGE)
    result = import_wiki_play("play-high-split-action")

    assert result.source == "wiki-structured"
    assert result.play is not None
    assert result.play["name"] == "High Split"

    phases = result.play["phases"]
    assert len(phases) == 2
    assert phases[0]["label"] == "Entry"
    assert phases[1]["label"] == "Split Options"

    # Phase 2 should use the block tagged "Phase 2" (5→4 pass + 4→rim cut).
    phase2_actions = phases[1]["actions"]
    rim_cut = [a for a in phase2_actions if a.get("move", {}).get("id") == "4"]
    assert rim_cut and rim_cut[0]["move"]["to"] == [0, 4]


def test_no_diagram_play_returns_none(tmp_wiki: Path) -> None:
    """``type: play`` page without any diagram blocks → ``wiki-no-diagram``."""
    _write_page(tmp_wiki, "play-versus-triangle-and-two", NO_DIAGRAM_PAGE)
    result = import_wiki_play("play-versus-triangle-and-two")

    assert result.source == "wiki-no-diagram"
    assert result.play is None
    assert any("prose extractor" in todo for todo in result.todos)


# ---------------------------------------------------------------------------
# Security — path traversal.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bad_slug",
    [
        "../escape",
        "nested/slug",
        "..",
        "./play-black",
        "",
        r"backslash\name",
    ],
)
def test_path_traversal_rejected(tmp_wiki: Path, bad_slug: str) -> None:
    """Slugs with separators or parent refs must be rejected cleanly."""
    with pytest.raises(ValueError, match=r"invalid slug|escapes wiki"):
        _resolve_wiki_path(bad_slug, tmp_wiki)


def test_import_rejects_traversal(tmp_wiki: Path) -> None:
    """The public entry point refuses to read files outside the wiki dir."""
    with pytest.raises(ValueError):
        import_wiki_play("../escape")


# ---------------------------------------------------------------------------
# Listing.
# ---------------------------------------------------------------------------


SCHEMA_V2_PAGE = """---
type: play
category: offense
---

# Schema V2

## Overview
Fixture exercising the schema v2 action fields.

```json name=diagram-positions
{"players":[{"role":"1","x":0,"y":33},{"role":"2","x":-18,"y":22},{"role":"3","x":18,"y":22},{"role":"4","x":-8,"y":29},{"role":"5","x":8,"y":29}],"ballStart":"2","actions":[{"from":"4","to":"2","type":"screen","path":"M 8 29 C 2 26 -6 24 -16 22","moveTo":[-14,22],"durationMs":2200,"gapAfterMs":250},{"from":"1","to":"2","type":"pass","ballTo":"2","path":"M 0 33 C 2 28 -4 24 -16 22"}],"notes":"Phase 1."}
```

## Phases

### Phase 1: Only
- 4 sets a screen for 2; 1 passes to 2.

## Sources
- [Sx, p.1]
"""


def test_schema_v2_fields_forwarded(tmp_wiki: Path) -> None:
    """Authored path / moveTo / timing / ballTo / ballStart must survive import."""
    _write_page(tmp_wiki, "play-schema-v2", SCHEMA_V2_PAGE)
    result = import_wiki_play("play-schema-v2")

    assert result.source == "wiki-structured"
    assert result.play is not None
    assert result.play["ballStart"] == "2"

    actions = result.play["phases"][0]["actions"]
    assert len(actions) == 2

    screen, pass_action = actions
    # Authored path preserved verbatim so downstream synthesizer leaves it alone.
    assert screen["path"] == "M 8 29 C 2 26 -6 24 -16 22"
    # moveTo wins over the role-destination lookup for "2".
    assert screen["move"]["id"] == "4"
    assert screen["move"]["to"] == [-14.0, 22.0]
    # Timing overrides forwarded.
    assert screen["durationMs"] == 2200
    assert screen["gapAfterMs"] == 250

    # Pass action uses explicit ballTo + authored path.
    assert pass_action["marker"] == "arrow"
    assert pass_action["dashed"] is True
    assert pass_action["ball"] == {"from": "1", "to": "2"}
    assert pass_action["path"] == "M 0 33 C 2 28 -4 24 -16 22"


def test_schema_v2_backward_compat_no_overrides(tmp_wiki: Path) -> None:
    """Pages without schema v2 fields emit V7 actions with no timing keys.

    Paths end up synthesized (downstream), so the right thing to pin here is
    the absence of the new optional keys (``durationMs`` / ``gapAfterMs``).
    Presence of those would signal accidental field leakage.
    """
    _write_page(tmp_wiki, "play-black", SINGLE_BLOCK_PAGE)
    result = import_wiki_play("play-black")
    phases = result.play["phases"] if result.play else []
    populated_actions = [a for p in phases for a in p["actions"]]
    assert populated_actions, "fixture should yield at least one action"
    for a in populated_actions:
        assert "durationMs" not in a, f"unexpected timing override: {a}"
        assert "gapAfterMs" not in a, f"unexpected timing override: {a}"
    # ballStart still derived from default logic (role "1" present).
    assert result.play["ballStart"] == "1"


def test_schema_v2_ballstart_falls_back_when_unknown(tmp_wiki: Path) -> None:
    """Explicit ballStart pointing at a non-existent player falls back safely."""
    bad_page = SCHEMA_V2_PAGE.replace('"ballStart":"2"', '"ballStart":"99"')
    _write_page(tmp_wiki, "play-bad-ball", bad_page)
    result = import_wiki_play("play-bad-ball")
    # 99 is not in the roster → falls back to "1".
    assert result.play["ballStart"] == "1"


def test_list_importable_plays_reports_diagram_flag(tmp_wiki: Path) -> None:
    """Listing surfaces slug/name/phaseCount/hasDiagram/blockCount per page."""
    _write_page(tmp_wiki, "play-black", SINGLE_BLOCK_PAGE)
    _write_page(tmp_wiki, "play-versus-triangle-and-two", NO_DIAGRAM_PAGE)
    # A non-play page should be ignored.
    _write_page(
        tmp_wiki,
        "concept-foo",
        "---\ntype: concept\n---\n\n# Foo\n",
    )
    entries = list_importable_wiki_plays()
    slugs = {e["slug"]: e for e in entries}
    assert set(slugs.keys()) == {"play-black", "play-versus-triangle-and-two"}
    assert slugs["play-black"]["hasDiagram"] is True
    assert slugs["play-black"]["blockCount"] == 1
    assert slugs["play-versus-triangle-and-two"]["hasDiagram"] is False
