"""Sport → prompt-prelude module dispatcher.

Service layers (`play_brief`, `practice_brief`, `form_brief`) call
:func:`get_prompts(sport)` to fetch the prelude module for the active
sport instead of importing ``motion.prompts.basketball`` directly. This
keeps the service code sport-agnostic and makes adding a third sport a
content-only change (new module + one tuple entry below).
"""

from __future__ import annotations

from types import ModuleType

from motion.prompts import basketball, football
from motion.sports import DEFAULT_SPORT, Sport, is_valid_sport

_REGISTRY: dict[Sport, ModuleType] = {
    "basketball": basketball,
    "football": football,
}


def get_prompts(sport: Sport = DEFAULT_SPORT) -> ModuleType:
    """Return the prompt-prelude module for ``sport``.

    Falls back to :data:`motion.sports.DEFAULT_SPORT` (basketball) when
    the caller cannot resolve a sport — preserves pre-Step-4 behavior on
    code paths that have not yet threaded sport through.

    Raises :class:`ValueError` for unknown sport strings to fail fast on
    typos rather than silently swap content.
    """
    if not is_valid_sport(sport):
        raise ValueError(
            f"unknown sport {sport!r}; expected one of {sorted(_REGISTRY)}"
        )
    return _REGISTRY[sport]
