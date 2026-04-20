"""Clerk session-token verification for FastAPI.

Verifies an incoming `Authorization: Bearer <jwt>` header against Clerk's
JWKS, networkless after the first fetch. Returns an `AuthedUser` on success,
raises HTTP 401 otherwise.

Configured via `CLERK_JWKS_URL`, `CLERK_ISSUER`, `CLERK_AUTHORIZED_PARTIES`.
"""

from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass
from typing import Any

import httpx
from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt

from motion.config import Settings, get_settings

logger = logging.getLogger("motion.auth")

_JWKS_TTL_SECONDS = 3600
_HTTP_TIMEOUT_SECONDS = 5.0


@dataclass(frozen=True)
class AuthedUser:
    """Minimal identity view extracted from a verified Clerk session JWT."""

    clerk_id: str
    session_id: str
    email: str | None


class _JwksCache:
    """In-process JWKS cache keyed by `kid`. One instance per process is enough."""

    def __init__(self) -> None:
        self._keys: dict[str, dict[str, Any]] = {}
        self._fetched_at: float = 0.0
        self._lock = asyncio.Lock()

    async def get(self, kid: str, jwks_url: str) -> dict[str, Any] | None:
        if self._fresh() and kid in self._keys:
            return self._keys[kid]
        async with self._lock:
            if self._fresh() and kid in self._keys:
                return self._keys[kid]
            await self._refresh(jwks_url)
        return self._keys.get(kid)

    def _fresh(self) -> bool:
        return (time.monotonic() - self._fetched_at) < _JWKS_TTL_SECONDS

    async def _refresh(self, jwks_url: str) -> None:
        async with httpx.AsyncClient(timeout=_HTTP_TIMEOUT_SECONDS) as client:
            response = await client.get(jwks_url)
            response.raise_for_status()
            payload = response.json()
        self._keys = {key["kid"]: key for key in payload.get("keys", []) if "kid" in key}
        self._fetched_at = time.monotonic()
        logger.info("clerk jwks refreshed (%d keys)", len(self._keys))


_cache = _JwksCache()


def _extract_bearer(request: Request) -> str:
    header = request.headers.get("authorization") or request.headers.get("Authorization")
    if not header or not header.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="missing_bearer_token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = header[7:].strip()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="empty_bearer_token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


def _unverified_kid(token: str) -> str:
    try:
        headers = jwt.get_unverified_header(token)
    except JWTError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="malformed_token",
        ) from err
    kid = headers.get("kid")
    if not isinstance(kid, str) or not kid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="missing_kid",
        )
    return kid


async def _verify_and_decode(token: str, settings: Settings) -> dict[str, Any]:
    if not settings.clerk_jwks_url or not settings.clerk_issuer:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="clerk_not_configured",
        )

    kid = _unverified_kid(token)
    jwk = await _cache.get(kid, settings.clerk_jwks_url)
    if jwk is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="unknown_signing_key",
        )

    try:
        claims: dict[str, Any] = jwt.decode(
            token,
            jwk,
            algorithms=[jwk.get("alg", "RS256")],
            issuer=settings.clerk_issuer,
            options={"verify_aud": False},
        )
    except JWTError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"token_invalid: {err}",
        ) from err

    # Clerk puts the frontend origin on `azp`. Enforce it if configured.
    authorized = settings.clerk_authorized_parties_list
    if authorized:
        azp = claims.get("azp")
        if azp not in authorized:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="unauthorized_party",
            )

    return claims


def _user_from_claims(claims: dict[str, Any]) -> AuthedUser:
    clerk_id = claims.get("sub")
    session_id = claims.get("sid")
    if not isinstance(clerk_id, str) or not isinstance(session_id, str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incomplete_token",
        )
    email = claims.get("email")
    return AuthedUser(
        clerk_id=clerk_id,
        session_id=session_id,
        email=email if isinstance(email, str) else None,
    )


async def get_current_user(
    request: Request,
    settings: Settings = Depends(get_settings),  # noqa: B008 — FastAPI idiom
) -> AuthedUser:
    """FastAPI dependency: 401 unless a valid Clerk JWT is present."""
    token = _extract_bearer(request)
    claims = await _verify_and_decode(token, settings)
    return _user_from_claims(claims)
