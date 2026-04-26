"""coach_profile.sports text[] — sport-portable foundations Step 1

Adds the per-coach sport list. Default ``{basketball}`` so every existing
coach is treated as a basketball coach (matches pre-Step-1 behavior).
Future football coaches set ``{football}`` or ``{basketball,football}`` via
the onboarding flow.

Per D8 of the sport-portable foundations blueprint, this column is **data
only** — it does not gate access. All authenticated coaches can browse all
sports until per-sport authorization is explicitly added in a later step.

Revision ID: 0002_coach_profile_sports
Revises: 0001_initial
Create Date: 2026-04-26
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "0002_coach_profile_sports"
down_revision: str | None = "0001_initial"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "coach_profile",
        sa.Column(
            "sports",
            postgresql.ARRAY(sa.String()),
            nullable=False,
            server_default="{basketball}",
        ),
    )
    # Belt-and-braces backfill — server_default handles new rows, but if any
    # existing rows somehow ended up with NULL (race during migration on a
    # busy table), the explicit UPDATE makes that impossible.
    op.execute(
        "UPDATE coach_profile SET sports = '{basketball}' WHERE sports IS NULL"
    )


def downgrade() -> None:
    op.drop_column("coach_profile", "sports")
