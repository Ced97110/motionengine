"""Integration tests for the knowledge-retrieval HTTP endpoints.

Uses FastAPI's TestClient to hit the router end-to-end against the real
compiled indexes under ``knowledge-base/wiki/compiled/``. Each test pins
a key shape assertion so regressions on the HTTP contract are caught
immediately by CI.
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from motion.routers.knowledge import router as knowledge_router


@pytest.fixture(scope="module")
def client() -> Iterator[TestClient]:
    """Minimal app with just the knowledge router — no DB, no auth."""
    app = FastAPI()
    app.include_router(knowledge_router)
    with TestClient(app) as test_client:
        yield test_client


def test_play_context_returns_play_black_bundle(client: TestClient) -> None:
    response = client.post("/api/knowledge/play-context", json={"playSlug": "play-black"})
    assert response.status_code == 200
    body = response.json()

    assert body["playSlug"] == "play-black"
    regions = {a["region"] for a in body["anatomy"]}
    assert regions == {"hip_flexor_complex", "glute_max", "ankle_complex", "core_outer"}

    drill_slugs = {d["drillSlug"] for d in body["drills"]}
    assert drill_slugs == {
        "exercise-hip-thrust",
        "drill-back-extension",
        "drill-band-lateral-walk",
        "drill-bird-dog",
        "drill-ankling",
    }

    # primary-emphasis drills are ranked first
    emphases = [d["emphasis"] for d in body["drills"]]
    assert emphases == sorted(emphases, key=lambda e: 0 if e == "primary" else 1)


def test_play_context_unknown_play_returns_empty_bundle(client: TestClient) -> None:
    response = client.post("/api/knowledge/play-context", json={"playSlug": "play-does-not-exist"})
    assert response.status_code == 200
    body = response.json()
    assert body["anatomy"] == []
    assert body["techniques"] == []
    assert body["drills"] == []


def test_readiness_hip_flexor_excludes_play_black(client: TestClient) -> None:
    response = client.post(
        "/api/knowledge/readiness",
        json={"flaggedRegions": ["hip_flexor_complex"]},
    )
    assert response.status_code == 200
    body = response.json()
    assert "play-black" in body["excludedPlays"]
    assert "play-black" not in body["safePlays"]


def test_readiness_ankle_optional_does_not_exclude(client: TestClient) -> None:
    response = client.post(
        "/api/knowledge/readiness",
        json={"flaggedRegions": ["ankle_complex"]},
    )
    assert response.status_code == 200
    body = response.json()
    # ankle is optional on play-black → not excluded
    assert "play-black" not in body["excludedPlays"]


def test_readiness_glute_max_prescribes_primary_drills(client: TestClient) -> None:
    response = client.post(
        "/api/knowledge/readiness",
        json={"flaggedRegions": ["glute_max"]},
    )
    assert response.status_code == 200
    body = response.json()
    slugs = {d["drillSlug"] for d in body["prescriptionDrills"]}
    assert slugs == {"exercise-hip-thrust", "drill-back-extension", "drill-band-lateral-walk"}
    assert all(d["emphasis"] == "primary" for d in body["prescriptionDrills"])


def test_drill_justification_hip_thrust_returns_play_black(client: TestClient) -> None:
    response = client.post(
        "/api/knowledge/drill-justification",
        json={"drillSlug": "exercise-hip-thrust"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["drillSlug"] == "exercise-hip-thrust"
    assert body["plays"] == ["play-black"]


def test_validation_error_returns_422(client: TestClient) -> None:
    response = client.post("/api/knowledge/play-context", json={})
    assert response.status_code == 422


def test_play_brief_stub_path(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    """Without an ANTHROPIC_API_KEY, the brief endpoint falls back to the stub."""
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    response = client.post("/api/knowledge/play-brief", json={"playSlug": "play-black"})
    assert response.status_code == 200
    body = response.json()
    assert body["playSlug"] == "play-black"
    assert body["source"] == "stub"
    assert isinstance(body["brief"], str)
    # stub brief mentions at least one required region from play-black
    assert any(region in body["brief"].lower() for region in ["hip flexor", "glute max", "glutes"])


def test_play_brief_with_roster_readiness_adds_caveat(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Passing a flagged region that matches a required region yields a caveat."""
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    response = client.post(
        "/api/knowledge/play-brief",
        json={
            "playSlug": "play-black",
            "rosterReadiness": [{"playerName": "Rivera", "flaggedRegions": ["hip_flexor_complex"]}],
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert "caveat" in body["brief"].lower() or "substitution" in body["brief"].lower()
