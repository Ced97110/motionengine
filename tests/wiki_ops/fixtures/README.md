# Synthetic test fixtures

This directory is intentionally empty. All synthetic fixtures for the
Phase 1 wiki-ops parity tests are constructed **in-test** using
`tmp_path` to keep each test self-contained and to avoid committing
large blobs to the repo.

If a future port needs committed fixtures (e.g. a real PDF for
ingestion testing), add them here one subdirectory per script:

```
fixtures/
├── count_pages/
├── resynth_manifest/
├── check_nba_terms/
└── lint_wiki/
```
