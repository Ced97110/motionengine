"""YAML frontmatter parsing helpers.

Two distinct parsers are exposed because the TS originals use two
different strategies and byte-level parity demands we mirror each one
exactly:

1. :func:`parse_full` — used by ``resynth_manifest``. The TS original
   relies on ``gray-matter`` (js-yaml under the hood), which parses a
   full YAML document. We use PyYAML's safe loader to match.
2. :func:`parse_shallow` — used by ``lint_wiki``. The TS original uses a
   hand-rolled ``^key: value$`` line regex that flattens every value to
   a string and ignores lists/nested structures. We reproduce the same
   single-line regex.

Both parsers consume the leading ``---\\n...\\n---`` block and return
the body starting immediately after it (preserving any trailing newline
byte-for-byte).
"""

from __future__ import annotations

import re
from typing import Any

import yaml

# Matches a frontmatter block that starts at byte 0, per TS convention
# (``gray-matter`` and the lint-wiki ``FRONTMATTER_RE`` both anchor at
# the start of the file).
_FRONTMATTER_RE = re.compile(r"^---\n([\s\S]*?)\n---\n?")

# Shallow ``key: value`` extractor for lint_wiki parity.
_SHALLOW_KV_RE = re.compile(r"^([a-zA-Z_][\w-]*):\s*(.*)$")


def parse_full(raw: str) -> tuple[dict[str, Any], str]:
    """Parse a full YAML frontmatter block + return ``(data, content)``.

    Matches ``gray-matter`` semantics: if no frontmatter is present, an
    empty ``data`` dict is returned and ``content`` is the original raw
    string. If YAML parsing fails, ``data`` is an empty dict (mirroring
    ``gray-matter``'s tolerance; the TS port silently degrades rather
    than crashing on malformed YAML).
    """
    match = _FRONTMATTER_RE.match(raw)
    if match is None:
        return {}, raw
    block = match.group(1)
    try:
        loaded = yaml.safe_load(block)
    except yaml.YAMLError:
        loaded = None
    if isinstance(loaded, dict):
        data: dict[str, Any] = {str(k): v for k, v in loaded.items()}
    else:
        data = {}
    return data, raw[len(match.group(0)) :]


def parse_shallow(raw: str) -> tuple[dict[str, str], str, int]:
    """Parse frontmatter with the lint-wiki shallow line regex.

    Returns ``(frontmatter, body, body_start_line)`` where
    ``body_start_line`` is the 1-based line number of the body's first
    line, matching the TS ``parseFrontmatter`` output at
    ``frontend/scripts/lint-wiki.ts:211-235``.
    """
    match = _FRONTMATTER_RE.match(raw)
    if match is None:
        return {}, raw, 1
    block = match.group(1)
    fm: dict[str, str] = {}
    for line in block.split("\n"):
        kv = _SHALLOW_KV_RE.match(line)
        if kv:
            fm[kv.group(1)] = kv.group(2).strip()
    consumed = match.group(0)
    body_start = len(consumed.split("\n"))
    return fm, raw[len(consumed) :], body_start
