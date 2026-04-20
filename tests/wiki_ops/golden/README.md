# Captured TS-parity golden outputs

This directory is **optional**. It holds byte-equal captures of TS
script outputs for full end-to-end parity regression. When the files
listed below are present, the corresponding parity tests (marked with
`@pytest.mark.golden`) compare the Python port output byte-for-byte
against the captured TS output.

When these files are absent, the parity tests skip with a clear
message. Synthetic-fixture tests in the same modules run on every
invocation and cover the same code paths with deterministic input.

## Status (post Phase 6 — 2026-04-14)

The TS originals (`count-pages.ts`, `resynth-manifest.ts`,
`check-nba-terms.ts`, `lint-wiki.ts`, …) were **deleted in Phase 6**.
Any captured goldens already on disk are the **frozen reference**.
Re-capture is no longer a routine operation.

If a parity question arises and the goldens need refreshing, the path is:

1. `git log -- frontend/scripts/<deleted-script>.ts` to find the last
   commit that contained the TS original.
2. `git restore --source=<commit> -- frontend/scripts/<script>.ts` to
   bring it back into the working tree (do NOT commit).
3. Run the original capture command (see git history of this README for
   the exact `npx tsx` invocations).
4. `git restore frontend/scripts/<script>.ts` (clean back up).

Synthetic-fixture tests in `tests/wiki_ops/test_<module>.py` now
provide the deterministic parity story for everyday work; goldens are
historical.

## Normalization

The lint-wiki report contains a `Generated: YYYY-MM-DD` header line.
Both the captured golden and the Python output are passed through
`_strip_generation_timestamp` in `test_lint_wiki.py` before diff so the
parity test doesn't flap on date. No other normalization should be
required for the remaining three scripts.

## CI

These captures are **not** regenerated in CI. The Phase 6 switchover
will delete the TS scripts; at that point the captured goldens become
the frozen reference and no further regeneration happens until Phase
2+ scripts port. See `backend/spec/wiki-ops-python-migration.md` §6.
