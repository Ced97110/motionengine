# Motion — Backend

> Parent: [`../CLAUDE.md`](../CLAUDE.md) — read for vision, IP rules, voice, and anti-choices.

FastAPI service + Python ingestion pipeline + wiki source-of-truth.

---

## Stack

- **Runtime**: Python 3.12 via `uv`
- **API**: FastAPI
- **DB**: Postgres via `asyncpg`, Alembic migrations
- **ML**: stdlib + scikit-learn (service imports `lib/ml/`)

---

## Boot

```bash
cd backend
docker compose up -d
uv run alembic upgrade head
PORT=8080 uv run motion-api
```

Port 8000 conflicts with another local service — use 8080.

Copy `.env.example → .env` before first run. If Compose complains, use:
```bash
docker compose -f docker-compose.yml --env-file .env up
```

---

## Layout

| Path | Purpose |
|---|---|
| `src/motion/` | FastAPI service |
| `pipeline/01_download_dataset.py` … `11_test_ml.py` | SportsSettBasketball ingestion. See `spec/SPORTSETT_INTEGRATION.md`. |
| `lib/game_report.py`, `halftime.py`, `ml/` | Production functions imported by the FastAPI service |
| `eval/*.jsonl` | Fixture cases for resolver + synth quality gates |
| `tests/` | pytest suite |
| `knowledge-base/raw/` | Raw PDFs (gitignored) |
| `knowledge-base/wiki/` | Compiled cited wiki markdown (source of truth) |
| `data/parsed_games.json` (~61 MB) | Regeneratable via `scripts/02_parse_dataset.py`. **Don't commit without LFS.** |

---

## Gotchas (from E1 boot)

- `greenlet` is a hidden dep of SQLAlchemy async — pinned in `pyproject.toml`.
- `.env.example` requires the `docker compose -f … --env-file .env up` syntax above.
- `UniqueConstraint(text(...))` breaks alembic autogen — use explicit column names.

---

## Gates

- `uv run pytest` — tests
- `uv run ruff check` — lint
- `uv run alembic upgrade head` — migrations are additive; don't autogen from `text()` constraints
- Eval fixtures in `eval/*.jsonl` are the resolver/synth quality gate — run them when changing either.
