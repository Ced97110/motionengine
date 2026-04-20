"""Unit tests for ``motion.wiki_ops.retrieval``.

Uses a synthetic in-tmp compiled directory to exercise the three query
functions (``build_play_context``, ``build_readiness_filter``,
``build_drill_justification``) against known fixtures — no dependency on
the live wiki corpus.

A second module-scoped test runs against the real compiled indexes to
pin the play-black bundle shape as a smoke test.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from motion.wiki_ops.retrieval import (
    AnatomyDemand,
    TechniqueDemand,
    build_drill_justification,
    build_play_context,
    build_readiness_filter,
    context_to_dict,
    load_indexes,
)


def _write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


@pytest.fixture()
def synthetic_compiled(tmp_path: Path) -> Path:
    """Build a minimal compiled/ directory with two plays, two regions, two drills."""
    out = tmp_path / "compiled"
    out.mkdir()
    _write_json(
        out / "play-to-anatomy.json",
        {
            "play-alpha": [
                {"region": "glute_max", "criticality": "required"},
                {"region": "ankle_complex", "criticality": "optional"},
            ],
            "play-beta": [{"region": "glute_max", "criticality": "optional"}],
        },
    )
    _write_json(
        out / "play-to-technique.json",
        {"play-alpha": [{"id": "explosive-first-step", "criticality": "required", "role": "1"}]},
    )
    _write_json(
        out / "anatomy-to-play.json",
        {
            "glute_max": [
                {"play": "play-alpha", "criticality": "required"},
                {"play": "play-beta", "criticality": "optional"},
            ],
            "ankle_complex": [{"play": "play-alpha", "criticality": "optional"}],
        },
    )
    _write_json(
        out / "anatomy-to-drill.json",
        {
            "glute_max": [
                {"drill": "drill-hip-thrust", "emphasis": "primary"},
                {"drill": "drill-band-walk", "emphasis": "secondary"},
            ],
            "ankle_complex": [{"drill": "drill-ankling", "emphasis": "primary"}],
        },
    )
    _write_json(
        out / "technique-to-play.json",
        {"explosive-first-step": [{"play": "play-alpha", "criticality": "required", "role": "1"}]},
    )
    _write_json(
        out / "technique-to-drill.json",
        {"explosive-first-step": [{"drill": "drill-hip-thrust", "emphasis": "primary"}]},
    )
    _write_json(
        out / "technique-aliases.json",
        {
            "version": "test",
            "aliases": {
                "explosive-first-step": {
                    "slug": "concept-first-step-quickness",
                    "confidence": "HIGH",
                }
            },
        },
    )
    return out


def test_build_play_context_resolves_anatomy_and_technique(synthetic_compiled: Path) -> None:
    indexes = load_indexes(synthetic_compiled)
    ctx = build_play_context("play-alpha", indexes)

    assert ctx.play_slug == "play-alpha"
    assert AnatomyDemand("glute_max", "concept-anatomy-glute-max", "required") in ctx.anatomy
    assert (
        AnatomyDemand("ankle_complex", "concept-anatomy-ankle-complex", "optional") in ctx.anatomy
    )
    assert ctx.techniques == [
        TechniqueDemand(
            technique_id="explosive-first-step",
            concept_slug="concept-first-step-quickness",
            role="1",
            criticality="required",
        )
    ]


def test_build_play_context_dedupes_drills_and_ranks_primary_first(
    synthetic_compiled: Path,
) -> None:
    """drill-hip-thrust is reachable via anatomy AND technique — must appear once."""
    indexes = load_indexes(synthetic_compiled)
    ctx = build_play_context("play-alpha", indexes)

    slugs = [d.drill_slug for d in ctx.drills]
    assert slugs.count("drill-hip-thrust") == 1
    # primary-emphasis drills first
    primaries = [d for d in ctx.drills if d.emphasis == "primary"]
    secondaries = [d for d in ctx.drills if d.emphasis == "secondary"]
    assert ctx.drills == primaries + secondaries
    # first-reach via anatomy should win (anatomy iteration precedes techniques)
    hip_thrust = next(d for d in ctx.drills if d.drill_slug == "drill-hip-thrust")
    assert hip_thrust.via == "anatomy:glute_max"


def test_build_play_context_unknown_play_returns_empty_bundle(
    synthetic_compiled: Path,
) -> None:
    indexes = load_indexes(synthetic_compiled)
    ctx = build_play_context("play-nonexistent", indexes)
    assert ctx.anatomy == []
    assert ctx.techniques == []
    assert ctx.drills == []


def test_build_readiness_filter_excludes_only_required(synthetic_compiled: Path) -> None:
    indexes = load_indexes(synthetic_compiled)
    bundle = build_readiness_filter(["glute_max"], indexes)
    # play-alpha is required on glute_max → excluded
    assert "play-alpha" in bundle.excluded_plays
    # play-beta is optional on glute_max → stays safe
    assert "play-beta" in bundle.safe_plays
    assert "play-alpha" not in bundle.safe_plays


def test_build_readiness_filter_prescribes_only_primary_emphasis(
    synthetic_compiled: Path,
) -> None:
    indexes = load_indexes(synthetic_compiled)
    bundle = build_readiness_filter(["glute_max"], indexes)
    slugs = [d.drill_slug for d in bundle.prescription_drills]
    assert "drill-hip-thrust" in slugs  # primary
    assert "drill-band-walk" not in slugs  # secondary


def test_build_readiness_filter_optional_region_does_not_exclude(
    synthetic_compiled: Path,
) -> None:
    indexes = load_indexes(synthetic_compiled)
    bundle = build_readiness_filter(["ankle_complex"], indexes)
    assert bundle.excluded_plays == []
    # play-alpha remains safe because ankle is optional on it
    assert "play-alpha" in bundle.safe_plays


def test_build_drill_justification_returns_required_plays(synthetic_compiled: Path) -> None:
    indexes = load_indexes(synthetic_compiled)
    plays = build_drill_justification("drill-hip-thrust", indexes)
    # play-alpha: glute_max required ✓
    # play-beta: glute_max optional → excluded
    assert plays == ["play-alpha"]


def test_build_drill_justification_unknown_drill_returns_empty(
    synthetic_compiled: Path,
) -> None:
    indexes = load_indexes(synthetic_compiled)
    assert build_drill_justification("drill-nonexistent", indexes) == []


def test_context_to_dict_is_json_serialisable(synthetic_compiled: Path) -> None:
    indexes = load_indexes(synthetic_compiled)
    ctx = build_play_context("play-alpha", indexes)
    payload = context_to_dict(ctx)
    # must round-trip through json.dumps without raising
    encoded = json.dumps(payload)
    decoded = json.loads(encoded)
    assert decoded["play_slug"] == "play-alpha"
    assert isinstance(decoded["anatomy"], list)
    assert isinstance(decoded["drills"], list)


# --- smoke test against the real compiled indexes ---------------------------


def test_live_play_black_bundle_smoke() -> None:
    """Pins the play-black bundle shape against the real compiled indexes."""
    indexes = load_indexes()
    ctx = build_play_context("play-black", indexes)

    regions = {a.region for a in ctx.anatomy}
    assert regions == {"hip_flexor_complex", "glute_max", "ankle_complex", "core_outer"}

    required_regions = {a.region for a in ctx.anatomy if a.criticality == "required"}
    assert required_regions == {"hip_flexor_complex", "glute_max"}

    drill_slugs = {d.drill_slug for d in ctx.drills}
    assert drill_slugs == {
        "exercise-hip-thrust",
        "drill-back-extension",
        "drill-band-lateral-walk",
        "drill-bird-dog",
        "drill-ankling",
    }


def test_live_readiness_filter_glute_max_excludes_play_black() -> None:
    indexes = load_indexes()
    bundle = build_readiness_filter(["glute_max"], indexes)
    assert "play-black" in bundle.excluded_plays


def test_live_drill_justification_hip_thrust_points_to_play_black() -> None:
    indexes = load_indexes()
    assert build_drill_justification("exercise-hip-thrust", indexes) == ["play-black"]
