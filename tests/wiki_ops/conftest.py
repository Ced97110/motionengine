"""Test fixtures for ``motion.wiki_ops`` parity tests.

The parity gate for Phase 1 of the wiki-ops Python migration is
byte-equal output between the Python port and the TypeScript original
on a shared input fixture.

Because the TS scripts cannot be executed from the Python test runner
without an `npm ci` + `tsx` install that is out of scope for this
package's CI, we rely on two complementary strategies:

1. **Deterministic synthetic fixtures.** Small wiki files and PDF
   directories constructed inside the test itself, with expected
   outputs hand-computed from the TS source. These tests run on every
   invocation of ``uv run pytest``.
2. **Optional full-parity golden capture.** The user regenerates
   byte-equal goldens by running ``npx tsx`` over the real wiki and
   pasting the output under
   ``tests/wiki_ops/golden/<script>/expected.*``. When those files
   exist, the full-parity tests run; when they don't, they skip.

Both strategies satisfy "what changed in the port?" — the synthetic
case provides surface-level coverage, and the golden case provides
end-to-end equivalence.
"""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    """Return the directory that holds committed synthetic fixtures."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def golden_dir() -> Path:
    """Return the optional captured-golden directory."""
    return Path(__file__).parent / "golden"


@pytest.fixture()
def tmp_wiki_dir(tmp_path: Path) -> Path:
    """Return an empty writable wiki directory inside the per-test tmp_path."""
    d = tmp_path / "wiki"
    d.mkdir()
    return d
