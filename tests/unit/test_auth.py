"""Clerk JWT verification unit tests (mocked JWKS)."""

from __future__ import annotations

import time
from typing import Any

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from jose import jwk as jose_jwk
from jose import jwt

from motion import auth as auth_module
from motion.auth import AuthedUser, get_current_user
from motion.config import Settings

ISSUER = "https://test.clerk.accounts.dev"
JWKS_URL = "https://test.clerk.accounts.dev/.well-known/jwks.json"
KID = "test-kid-1"
AZP = "http://localhost:3000"


@pytest.fixture(autouse=True)
def _reset_jwks_cache() -> None:
    auth_module._cache = auth_module._JwksCache()


@pytest.fixture
def rsa_keypair() -> tuple[rsa.RSAPrivateKey, dict[str, Any]]:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    public_jwk = jose_jwk.construct(public_pem.decode(), algorithm="RS256").to_dict()
    public_jwk["kid"] = KID
    public_jwk["alg"] = "RS256"
    public_jwk["use"] = "sig"
    return private_key, public_jwk


def _sign(private_key: rsa.RSAPrivateKey, claims: dict[str, Any]) -> str:
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    return jwt.encode(claims, pem.decode(), algorithm="RS256", headers={"kid": KID})


def _settings() -> Settings:
    return Settings(
        clerk_jwks_url=JWKS_URL,
        clerk_issuer=ISSUER,
        clerk_authorized_parties=AZP,
    )


def _app(settings: Settings) -> FastAPI:
    app = FastAPI()

    @app.get("/protected")
    async def protected(
        user: AuthedUser = Depends(get_current_user),  # noqa: B008 — FastAPI idiom
    ) -> dict[str, Any]:
        return {
            "clerk_id": user.clerk_id,
            "session_id": user.session_id,
            "email": user.email,
        }

    app.dependency_overrides[auth_module.get_settings] = lambda: settings
    return app


@pytest.fixture
def patched_jwks(
    rsa_keypair: tuple[rsa.RSAPrivateKey, dict[str, Any]],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Bypass the network JWKS fetch by priming the cache directly."""
    _, public_jwk = rsa_keypair

    async def _fake_get(_kid: str, _url: str) -> dict[str, Any]:
        return public_jwk

    monkeypatch.setattr(auth_module._cache, "get", _fake_get)


@pytest.mark.unit
def test_valid_token_returns_user(
    rsa_keypair: tuple[rsa.RSAPrivateKey, dict[str, Any]],
    patched_jwks: None,
) -> None:
    private_key, _ = rsa_keypair
    now = int(time.time())
    token = _sign(
        private_key,
        {
            "iss": ISSUER,
            "azp": AZP,
            "sub": "user_abc",
            "sid": "sess_xyz",
            "email": "coach@example.com",
            "iat": now,
            "exp": now + 60,
            "nbf": now - 1,
        },
    )
    settings = _settings()
    client = TestClient(_app(settings))
    response = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {
        "clerk_id": "user_abc",
        "session_id": "sess_xyz",
        "email": "coach@example.com",
    }


@pytest.mark.unit
def test_missing_bearer_returns_401(patched_jwks: None) -> None:
    client = TestClient(_app(_settings()))
    response = client.get("/protected")
    assert response.status_code == 401


@pytest.mark.unit
def test_wrong_issuer_returns_401(
    rsa_keypair: tuple[rsa.RSAPrivateKey, dict[str, Any]],
    patched_jwks: None,
) -> None:
    private_key, _ = rsa_keypair
    now = int(time.time())
    token = _sign(
        private_key,
        {
            "iss": "https://attacker.example.com",
            "azp": AZP,
            "sub": "user_abc",
            "sid": "sess_xyz",
            "iat": now,
            "exp": now + 60,
        },
    )
    client = TestClient(_app(_settings()))
    response = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


@pytest.mark.unit
def test_wrong_azp_returns_401(
    rsa_keypair: tuple[rsa.RSAPrivateKey, dict[str, Any]],
    patched_jwks: None,
) -> None:
    private_key, _ = rsa_keypair
    now = int(time.time())
    token = _sign(
        private_key,
        {
            "iss": ISSUER,
            "azp": "http://evil.example.com",
            "sub": "user_abc",
            "sid": "sess_xyz",
            "iat": now,
            "exp": now + 60,
        },
    )
    client = TestClient(_app(_settings()))
    response = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


@pytest.mark.unit
def test_expired_token_returns_401(
    rsa_keypair: tuple[rsa.RSAPrivateKey, dict[str, Any]],
    patched_jwks: None,
) -> None:
    private_key, _ = rsa_keypair
    now = int(time.time())
    token = _sign(
        private_key,
        {
            "iss": ISSUER,
            "azp": AZP,
            "sub": "user_abc",
            "sid": "sess_xyz",
            "iat": now - 3600,
            "exp": now - 60,
        },
    )
    client = TestClient(_app(_settings()))
    response = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
