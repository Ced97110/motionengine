"""SportMiddleware contract tests.

Verifies the header-tolerance contract (D7 of the sport-portable
foundations blueprint): missing header → DEFAULT_SPORT, unknown sport →
HTTP 400, valid sport → state.sport set.
"""
from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from motion.middleware.sport import SportMiddleware, current_sport


@pytest.fixture
def client() -> Iterator[TestClient]:
    app = FastAPI()
    app.add_middleware(SportMiddleware)

    @app.get("/echo-sport")
    async def echo_sport(request: Request) -> dict[str, str]:
        return {"sport": current_sport(request)}

    with TestClient(app) as c:
        yield c


def test_missing_header_falls_back_to_default(client: TestClient) -> None:
    r = client.get("/echo-sport")
    assert r.status_code == 200
    assert r.json() == {"sport": "basketball"}


def test_empty_header_falls_back_to_default(client: TestClient) -> None:
    r = client.get("/echo-sport", headers={"X-Motion-Sport": ""})
    assert r.status_code == 200
    assert r.json() == {"sport": "basketball"}


def test_basketball_header_resolves(client: TestClient) -> None:
    r = client.get("/echo-sport", headers={"X-Motion-Sport": "basketball"})
    assert r.status_code == 200
    assert r.json() == {"sport": "basketball"}


def test_football_header_resolves(client: TestClient) -> None:
    r = client.get("/echo-sport", headers={"X-Motion-Sport": "football"})
    assert r.status_code == 200
    assert r.json() == {"sport": "football"}


def test_unknown_sport_returns_400(client: TestClient) -> None:
    r = client.get("/echo-sport", headers={"X-Motion-Sport": "hockey"})
    assert r.status_code == 400
    body = r.json()
    assert body["error"]["code"] == "invalid_sport"
    assert "hockey" in body["error"]["message"]


def test_uppercase_sport_returns_400(client: TestClient) -> None:
    """Header values are case-sensitive matches against the Literal."""
    r = client.get("/echo-sport", headers={"X-Motion-Sport": "Basketball"})
    assert r.status_code == 400
