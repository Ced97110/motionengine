-- Bootstrap extensions on first container start.
-- Alembic still runs the authoritative CREATE EXTENSION statements;
-- this just spares the first migration from needing superuser.
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS btree_gist;
