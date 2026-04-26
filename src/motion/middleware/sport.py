"""Resolve the requested sport for each HTTP request.

Reads the ``X-Motion-Sport`` header set by the FE API client. Falls back to
:data:`motion.sports.DEFAULT_SPORT` when the header is absent so partial
deployments (BE-shipped, FE-not-yet) keep working — see D7 of the
sport-portable foundations blueprint.

Unknown sports return HTTP 400 rather than silently falling back, so a
typo or schema drift surfaces immediately instead of corrupting downstream
queries with the default sport's data.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from motion.sports import DEFAULT_SPORT, Sport, is_valid_sport

SPORT_HEADER = "x-motion-sport"


class SportMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        raw = request.headers.get(SPORT_HEADER)
        if raw is None or raw == "":
            request.state.sport = DEFAULT_SPORT
            return await call_next(request)
        if not is_valid_sport(raw):
            return JSONResponse(
                status_code=400,
                content={
                    "error": {
                        "code": "invalid_sport",
                        "message": f"unknown sport: {raw!r}",
                    }
                },
            )
        # ``request.state`` accepts arbitrary attribute assignment; the type
        # narrows downstream via :func:`current_sport`.
        request.state.sport = raw  # type: ignore[assignment]
        return await call_next(request)


def current_sport(request: Request) -> Sport:
    """Return the sport resolved by :class:`SportMiddleware` for this request.

    Defaults to :data:`motion.sports.DEFAULT_SPORT` when the middleware
    didn't run (e.g. unit tests that bypass the app stack).
    """
    return getattr(request.state, "sport", DEFAULT_SPORT)
