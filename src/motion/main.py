"""FastAPI application factory."""

from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from typing import Any, cast

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from motion import __version__
from motion.config import get_settings
from motion.db import get_engine
from motion.middleware.request_id import RequestIdMiddleware
from motion.routers.knowledge import router as knowledge_router
from motion.routers.playlab import router as playlab_router
from motion.schemas.errors import ErrorBody, ErrorEnvelope

logger = logging.getLogger("motion.main")


@asynccontextmanager
async def _lifespan(_: FastAPI) -> Any:
    settings = get_settings()
    logging.basicConfig(level=settings.log_level)
    logger.info("motion backend starting (env=%s)", settings.environment)
    yield
    await get_engine().dispose()
    logger.info("motion backend stopped")


def _cors_origins() -> list[str]:
    """Comma-separated env var CORS_ORIGINS, with sensible dev defaults."""
    default = (
        "http://localhost:3000,http://127.0.0.1:3000,"
        "http://localhost:3001,http://127.0.0.1:3001"
    )
    raw = os.getenv("CORS_ORIGINS", default)
    return [o.strip() for o in raw.split(",") if o.strip()]


def _envelope(code: str, message: str, *, retryable: bool = False, hint: str | None = None) -> dict[str, Any]:
    return ErrorEnvelope(
        error=ErrorBody(code=code, message=message, retryable=retryable, hint=hint)
    ).model_dump(by_alias=True)


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Motion API",
        version=__version__,
        docs_url="/docs" if not settings.is_prod else None,
        redoc_url=None,
        lifespan=_lifespan,
    )

    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["x-request-id"],
    )

    @app.exception_handler(RequestValidationError)
    async def _validation_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=_envelope(
                "validation_error",
                "Request payload failed validation.",
                hint=str(exc.errors()[:3]),
            ),
        )

    @app.exception_handler(SQLAlchemyError)
    async def _db_handler(_: Request, exc: SQLAlchemyError) -> JSONResponse:
        logger.exception("database error: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=_envelope(
                "database_unavailable",
                "Database is temporarily unavailable.",
                retryable=True,
            ),
        )

    @app.exception_handler(Exception)
    async def _unhandled(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("unhandled error: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=_envelope(
                "internal_error",
                "An unexpected error occurred.",
                retryable=True,
            ),
        )

    @app.get("/healthz", tags=["system"])
    async def healthz() -> dict[str, Any]:
        engine = get_engine()
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            ok = cast(int, result.scalar()) == 1
        return {"status": "ok" if ok else "degraded", "db": ok}

    @app.get("/version", tags=["system"])
    async def version() -> dict[str, str]:
        return {
            "version": __version__,
            "git_sha": os.getenv("GIT_SHA", "unknown"),
            "environment": settings.environment,
        }

    app.include_router(knowledge_router)
    app.include_router(playlab_router)

    return app


app = create_app()


def run() -> None:
    """uvicorn entrypoint for the `motion-api` console script."""
    import uvicorn

    uvicorn.run(
        "motion.main:app",
        host="0.0.0.0",  # noqa: S104 — bind-all intentional for containers
        port=int(os.getenv("PORT", "8000")),
        reload=os.getenv("RELOAD", "false").lower() == "true",
    )
