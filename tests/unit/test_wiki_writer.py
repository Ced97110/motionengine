"""Unit tests for :mod:`motion.services.wiki_writer`.

Covers:
- Block emission: one block per phase; key order; optional-field elision.
- Position snapshotting: screen actions don't relocate the screener.
- Markdown surgery: fences replaced in place; non-diagram text byte-preserved.
- Warning paths: extra blocks from V7Play appended; extra fences in md flagged.
"""
# ruff: noqa: E501

from __future__ import annotations

import json

from motion.services.wiki_writer import (
    render_updated_markdown,
    v7_play_to_diagram_blocks,
)


def _make_play(**overrides: object) -> dict[str, object]:
    base: dict[str, object] = {
        "name": "Schema V2",
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
        "phases": [],
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------------------------
# v7_play_to_diagram_blocks
# ---------------------------------------------------------------------------


def test_emits_phase_notes_prefers_phase_text() -> None:
    play = _make_play(
        phases=[
            {"label": "Entry", "text": "prose for phase 1", "actions": [], "defenseActions": []},
            {"label": "Action", "text": "", "actions": [], "defenseActions": []},
        ]
    )
    blocks, _ = v7_play_to_diagram_blocks(play)
    # Phase with text → emits the text so no-section round-trip works.
    assert blocks[0]["notes"] == "prose for phase 1"
    # Empty text → fallback "Phase N." stays readable.
    assert blocks[1]["notes"] == "Phase 2."


def test_ballstart_only_on_first_block() -> None:
    play = _make_play(
        phases=[
            {"label": "A", "text": "", "actions": [], "defenseActions": []},
            {"label": "B", "text": "", "actions": [], "defenseActions": []},
        ]
    )
    blocks, _ = v7_play_to_diagram_blocks(play)
    assert blocks[0]["ballStart"] == "1"
    assert "ballStart" not in blocks[1]


def test_players_snapshot_advances_through_phases() -> None:
    """Position in block N reflects state after phases 0..N-1 ran."""
    play = _make_play(
        phases=[
            {
                "label": "P1",
                "text": "",
                "actions": [
                    # 2 cuts from [-18, 22] to [18, 22]
                    {"marker": "arrow", "path": "",
                     "move": {"id": "2", "to": [18, 22]}},
                ],
                "defenseActions": [],
            },
            {"label": "P2", "text": "", "actions": [], "defenseActions": []},
        ]
    )
    blocks, _ = v7_play_to_diagram_blocks(play)
    # Block 0 snapshot = initial formation.
    p2_in_block0 = next(p for p in blocks[0]["players"] if p["role"] == "2")
    assert (p2_in_block0["x"], p2_in_block0["y"]) == (-18.0, 22.0)
    # Block 1 snapshot = after phase 1's cut moved 2 to [18, 22].
    p2_in_block1 = next(p for p in blocks[1]["players"] if p["role"] == "2")
    assert (p2_in_block1["x"], p2_in_block1["y"]) == (18.0, 22.0)


def test_screens_do_not_relocate_screener() -> None:
    """Shared rule with frontend computePositionsAt + importer _advance_positions."""
    play = _make_play(
        phases=[
            {
                "label": "P1",
                "text": "",
                "actions": [
                    {"marker": "screen", "path": "",
                     "move": {"id": "4", "to": [-16, 22]}},
                ],
                "defenseActions": [],
            },
            {"label": "P2", "text": "", "actions": [], "defenseActions": []},
        ]
    )
    blocks, _ = v7_play_to_diagram_blocks(play)
    # 4 stays at starting [-8, 29], not at the screen-glyph coord [-16, 22].
    p4_in_block1 = next(p for p in blocks[1]["players"] if p["role"] == "4")
    assert (p4_in_block1["x"], p4_in_block1["y"]) == (-8.0, 29.0)


def test_action_emission_preserves_schema_v2_fields() -> None:
    play = _make_play(
        phases=[
            {
                "label": "P1",
                "text": "",
                "actions": [
                    {
                        "marker": "screen",
                        "path": "M 8 29 C 2 26 -6 24 -16 22",
                        "move": {"id": "4", "to": [-14, 22]},
                        "durationMs": 2200,
                        "gapAfterMs": 250,
                    },
                    {
                        "marker": "arrow",
                        "dashed": True,
                        "path": "M 0 33 C 2 28 -4 24 -16 22",
                        "ball": {"from": "1", "to": "2"},
                    },
                ],
                "defenseActions": [],
            },
        ]
    )
    blocks, _ = v7_play_to_diagram_blocks(play)
    screen_action, pass_action = blocks[0]["actions"]

    # Key order matters for stable diffs.
    assert list(screen_action.keys()) == [
        "type", "from", "to", "path", "durationMs", "gapAfterMs",
    ]
    assert screen_action["type"] == "screen"
    assert screen_action["from"] == "4"
    assert screen_action["to"] == [-14.0, 22.0]
    assert screen_action["path"] == "M 8 29 C 2 26 -6 24 -16 22"
    assert screen_action["durationMs"] == 2200
    assert screen_action["gapAfterMs"] == 250

    assert pass_action == {
        "type": "pass",
        "from": "1",
        "to": "2",
        "path": "M 0 33 C 2 28 -4 24 -16 22",
    }


def test_action_without_from_is_skipped() -> None:
    play = _make_play(
        phases=[
            {
                "label": "P1",
                "text": "",
                "actions": [{"marker": "arrow", "path": ""}],  # no move, no ball
                "defenseActions": [],
            },
        ]
    )
    blocks, warnings = v7_play_to_diagram_blocks(play)
    assert blocks[0]["actions"] == []
    # Auditable: the human running save-to-wiki should see the drop.
    assert warnings
    assert "Phase 1 action 0" in warnings[0]
    assert "no recoverable `from`" in warnings[0]


# ---------------------------------------------------------------------------
# render_updated_markdown
# ---------------------------------------------------------------------------


_EXISTING_MD = """---
type: play
---

# Sample

## Overview
Narrative prose.

```json name=diagram-positions
{"players":[],"actions":[],"notes":"Phase 1."}
```

## Phases

### Phase 1: Only
- Stuff happens.

## Sources
- [Sx, p.1]
"""


def test_replace_single_fence_preserves_non_fence_bytes() -> None:
    new_block = {
        "players": [{"role": "1", "x": 0, "y": 33}],
        "actions": [],
        "notes": "Phase 1.",
    }
    new_md, warnings = render_updated_markdown(_EXISTING_MD, [new_block])
    assert warnings == []

    # All text outside the fence is byte-identical.
    assert new_md.startswith("---\ntype: play\n---\n\n# Sample\n\n## Overview\nNarrative prose.\n\n")
    assert new_md.endswith("## Sources\n- [Sx, p.1]\n")

    # The fence contents are now the new block.
    between_fence = new_md.split("```json name=diagram-positions\n", 1)[1].split("\n```", 1)[0]
    assert json.loads(between_fence) == new_block


def test_append_extra_blocks_produces_warning() -> None:
    b1 = {"players": [], "actions": [], "notes": "Phase 1."}
    b2 = {"players": [], "actions": [], "notes": "Phase 2."}
    b3 = {"players": [], "actions": [], "notes": "Phase 3."}

    new_md, warnings = render_updated_markdown(_EXISTING_MD, [b1, b2, b3])

    # Two new blocks appended at the tail.
    assert '"notes": "Phase 2."' in new_md
    assert '"notes": "Phase 3."' in new_md
    assert warnings, "expected warning about appended blocks"
    assert "Appended 2" in warnings[0]


def test_extra_fences_in_md_flagged() -> None:
    md_with_two_fences = _EXISTING_MD.replace(
        "```json name=diagram-positions\n" '{"players":[],"actions":[],"notes":"Phase 1."}\n```',
        (
            "```json name=diagram-positions\n"
            '{"players":[],"actions":[],"notes":"Phase 1."}\n```\n\n'
            "```json name=diagram-positions\n"
            '{"players":[],"actions":[],"notes":"Phase 2."}\n```'
        ),
    )
    new_md, warnings = render_updated_markdown(
        md_with_two_fences,
        [{"players": [], "actions": [], "notes": "Phase 1."}],
    )
    # First fence updated, second left alone.
    assert warnings
    assert "not overwritten" in warnings[0]
    # The second fence's Phase 2 body is still present.
    assert '"notes":"Phase 2."' in new_md


def test_no_existing_fences_appends_all_blocks() -> None:
    md_no_fence = "---\ntype: play\n---\n\n# X\n\nProse.\n"
    blocks = [
        {"players": [], "actions": [], "notes": "Phase 1."},
        {"players": [], "actions": [], "notes": "Phase 2."},
    ]
    new_md, warnings = render_updated_markdown(md_no_fence, blocks)
    assert "Phase 1." in new_md and "Phase 2." in new_md
    assert warnings and "Appended 2" in warnings[0]
