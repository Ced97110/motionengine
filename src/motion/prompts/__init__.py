"""Per-sport prompt preludes — Step 4 of the sport-portable foundations.

Each sport module exposes the same surface so the registry can dispatch
without knowing which sport's vocabulary it's fetching. The values are
the **literal** substrings + blocks that previously lived inline inside
``services/play_brief.py``, ``services/practice_brief.py``, and
``services/form_brief.py``.

The basketball module preserves byte-identical wording so the 36/36
play-brief eval baseline does not drift after this refactor (see memory
``m6-eval-shipped.md``). Football is the parallel scaffold for the
content workstream — its vocabulary is a coach-voice mirror, not a
clinical-mirror.
"""

from __future__ import annotations

from motion.prompts.registry import get_prompts

__all__ = ["get_prompts"]
