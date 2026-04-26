"""Round-trip invariant: ``import → write → import`` produces the same V7Play.

This is the load-bearing test that makes the wiki a true source of truth.
If importer and writer ever drift, CI catches it here before a PR lands.

Strategy:

1. Iterate every ``type: play`` page in the live corpus.
2. First import produces V7Play ``v7_a`` (paths synthesized where the wiki
   block had empty/missing ``path``).
3. Writer serializes ``v7_a`` back to markdown ``md1``.
4. Second import on ``md1`` produces V7Play ``v7_b`` (paths preserved via
   the synthesizer's ``_needs_synthesis`` short-circuit).
5. Assert ``v7_a == v7_b`` — semantic identity.

The LLM narrative expander is stubbed to ``[]`` so tests are deterministic
regardless of API availability; empty phases stay empty through both
imports.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import re

from motion.services import wiki_importer
from motion.services.wiki_importer import import_wiki_play, wiki_dir
from motion.services.wiki_writer import (
    render_updated_markdown,
    v7_play_to_diagram_blocks,
)
from motion.wiki_ops.frontmatter import parse_full


_PHASE_HEADER_RE = re.compile(r"^###\s+Phase\s+(\d+)", re.MULTILINE)


def _has_duplicate_phase_numbers(md: str) -> bool:
    """Some corpus pages reuse ``### Phase 1`` for parallel options.

    The importer keys phase sections by number (``phase_by_num`` dict in
    ``_assign_blocks_to_phases``) so duplicates collide — block→phase
    binding becomes structurally ambiguous, and the round-trip isn't a
    well-defined identity. Skip these pages; a separate follow-up can
    harden the importer's binding logic.
    """
    numbers = _PHASE_HEADER_RE.findall(md)
    return len(numbers) != len(set(numbers))


@pytest.fixture
def stub_expander(monkeypatch: pytest.MonkeyPatch) -> None:
    """Replace the narrative expander with a deterministic no-op."""
    monkeypatch.setattr(
        wiki_importer,
        "expand_phase_from_narrative",
        lambda *_args, **_kwargs: [],
    )


def _enumerate_play_slugs() -> list[str]:
    """Every ``type: play`` .md page in the corpus, by slug."""
    root = wiki_dir()
    slugs: list[str] = []
    for md in sorted(root.glob("play-*.md")):
        try:
            raw = md.read_text(encoding="utf-8")
        except OSError:
            continue
        fm, _ = parse_full(raw)
        if fm.get("type") == "play":
            slugs.append(md.stem)
    return slugs


PLAY_SLUGS = _enumerate_play_slugs()


def _drop_non_renderable_actions(play: dict) -> dict:
    """Strip actions that have neither ``move`` nor ``ball``.

    These are malformed wiki entries where ``to`` couldn't resolve at import
    time. The importer tolerates them as placeholders with a TODO; the
    writer intentionally drops them (surfacing a warning). For the round-
    trip identity test we normalize both sides so the invariant tracks
    "writer/importer agree on renderable content" rather than "writer
    perfectly round-trips broken data".
    """
    out = dict(play)
    out["phases"] = [
        {
            **phase,
            "actions": [
                a for a in phase.get("actions", [])
                if isinstance(a, dict) and (a.get("move") or a.get("ball"))
            ],
        }
        for phase in play.get("phases", [])
    ]
    return out


@pytest.mark.parametrize("slug", PLAY_SLUGS)
def test_corpus_roundtrip(
    slug: str,
    stub_expander: None,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """For each play page: import → write → import = identity (after normalize)."""
    # First import: against the real corpus.
    result_a = import_wiki_play(slug)
    if result_a.play is None:
        # wiki-no-diagram pages have no blocks to round-trip — skip.
        pytest.skip(f"{slug}: no diagram blocks to round-trip")
    v7_a = result_a.play

    # Build md1 from v7_a.
    root = wiki_dir()
    md0 = (root / f"{slug}.md").read_text(encoding="utf-8")
    if _has_duplicate_phase_numbers(md0):
        pytest.skip(
            f"{slug}: duplicate `### Phase N` headers — importer binding is "
            "structurally ambiguous; follow-up to harden binding logic."
        )
    blocks, _writer_warnings = v7_play_to_diagram_blocks(v7_a)
    md1, _render_warnings = render_updated_markdown(md0, blocks)

    # Stage md1 in a temp wiki dir and re-import from it. The importer reads
    # from the patched dir so we don't need to touch the real corpus.
    tmp_wiki = tmp_path / "wiki"
    tmp_wiki.mkdir()
    (tmp_wiki / f"{slug}.md").write_text(md1, encoding="utf-8")
    monkeypatch.setattr(wiki_importer, "wiki_dir", lambda *_a, **_k: tmp_wiki)

    result_b = import_wiki_play(slug)
    v7_b = result_b.play

    assert v7_b is not None, f"{slug}: writer produced md that no longer imports"
    v7_a_norm = _drop_non_renderable_actions(v7_a)
    v7_b_norm = _drop_non_renderable_actions(v7_b)
    assert v7_a_norm == v7_b_norm, (
        f"{slug}: round-trip drift — importer and writer disagree on "
        "renderable content"
    )


def test_roundtrip_covers_some_play() -> None:
    """Guard against the parametrize list going empty (e.g. wiki dir misrouted)."""
    assert PLAY_SLUGS, "expected at least one type:play page in the wiki corpus"
