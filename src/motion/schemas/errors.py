"""Typed error envelope — every endpoint returns {error: ErrorBody} on failure.

Shape is contracted with the frontend (see docs/specs/implementation-roadmap.md §1.4).
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class ErrorBody(_CamelModel):
    code: str
    message: str
    retryable: bool = False
    hint: str | None = None


class ErrorEnvelope(_CamelModel):
    error: ErrorBody
