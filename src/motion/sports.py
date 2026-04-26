"""Sport boundary primitive.

Single source of truth for which sports the platform supports. Every module
that needs sport-aware behavior (wiki path resolution, prompt prelude,
playing surface, IP guard) reads from here so adding a third sport later is
a one-line change in this file.

Backward-compat default is ``"basketball"``. Code paths that don't yet
thread a sport through (because they pre-date this primitive) implicitly
operate on basketball, matching pre-Step-1 behavior exactly.
"""

from __future__ import annotations

from typing import Literal, get_args

Sport = Literal["basketball", "football"]

SUPPORTED_SPORTS: tuple[Sport, ...] = get_args(Sport)
"""All sports the platform recognizes. Derived from the ``Sport`` Literal so
``mypy`` exhaustiveness and the runtime tuple stay in sync automatically."""

DEFAULT_SPORT: Sport = "basketball"
"""Fallback when no sport is specified — preserves pre-Step-1 behavior.

Per the cross-repo deployment ordering rule (D7), the backend must accept
requests without an ``X-Motion-Sport`` header by falling back to this
default. Removing that tolerance is a Step 7+ hardening, not part of the
sport-portable foundations blueprint.
"""


def is_valid_sport(value: str) -> bool:
    """True if ``value`` is one of the supported sport literals."""
    return value in SUPPORTED_SPORTS
