"""initial schema — coach profile, teams, roster, signals

Revision ID: 0001_initial
Revises:
Create Date: 2026-04-12

Mirrors docs/specs/backend-architecture.md §3.1-§3.3.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001_initial"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist")

    op.create_table(
        "coach_profile",
        sa.Column("coach_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "level",
            sa.String(),
            nullable=False,
            server_default="unknown",
        ),
        sa.Column("years_coaching", sa.SmallInteger(), nullable=True),
        sa.Column("level_coached", sa.String(), nullable=True),
        sa.Column("region", sa.String(), nullable=True),
        sa.Column("onboarded_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.CheckConstraint(
            "level IN ('unknown','beginner','intermediate','advanced')",
            name="coach_profile_level_check",
        ),
        sa.CheckConstraint(
            "years_coaching IS NULL OR (years_coaching BETWEEN 0 AND 80)",
            name="coach_profile_years_range",
        ),
        sa.CheckConstraint(
            "level_coached IS NULL OR level_coached IN "
            "('u10','u12','u14','u16','hs','college','pro','mixed')",
            name="coach_profile_level_coached_check",
        ),
    )

    op.create_table(
        "coach_concept_progress",
        sa.Column(
            "coach_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("coach_profile.coach_id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("concept_slug", sa.String(), primary_key=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("introduced_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("mastered_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "status IN ('locked','introduced','mastered')",
            name="coach_concept_status_check",
        ),
    )

    op.create_table(
        "coach_vocab_event",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "coach_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("coach_profile.coach_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("term", sa.String(), nullable=False),
        sa.Column("event_type", sa.String(), nullable=False),
        sa.Column(
            "occurred_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.CheckConstraint(
            "event_type IN ('definition-tap','play-used','concept-search')",
            name="coach_vocab_event_type_check",
        ),
    )
    op.create_index(
        "coach_vocab_event_coach_time_idx",
        "coach_vocab_event",
        ["coach_id", sa.text("occurred_at DESC")],
    )
    op.create_index("coach_vocab_event_term_idx", "coach_vocab_event", ["term"])

    op.create_table(
        "team",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "head_coach_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("coach_profile.coach_id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("level", sa.String(), nullable=False),
        sa.Column("rules", sa.String(), nullable=False, server_default="FIBA"),
        sa.Column("region", sa.String(), nullable=True),
        sa.Column("season", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.CheckConstraint("rules IN ('FIBA','NBA')", name="team_rules_check"),
    )

    op.create_table(
        "team_roster",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "team_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("team.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("player_ref", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("display_name", sa.String(), nullable=False),
        sa.Column("jersey_num", sa.SmallInteger(), nullable=True),
        sa.Column("position", sa.String(), nullable=True),
        sa.Column("age_group", sa.String(), nullable=True),
        sa.Column("parental_consent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "attributes",
            postgresql.JSONB(),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    op.create_index("team_roster_team_idx", "team_roster", ["team_id"])
    op.create_index(
        "team_roster_attrs_gin",
        "team_roster",
        ["attributes"],
        postgresql_using="gin",
    )

    op.create_table(
        "team_play_signal",
        sa.Column(
            "team_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("team.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("play_slug", sa.String(), nullable=False),
        sa.Column("signal_kind", sa.String(), nullable=False),
        sa.Column("signal_detail", postgresql.JSONB(), nullable=False),
        sa.Column("verbal_label", sa.String(), nullable=True),
        sa.Column(
            "assigned_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("assigned_by", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("team_id", "play_slug", name="team_play_signal_pk"),
        sa.CheckConstraint(
            "signal_kind IN ('finger_count','closed_fist','open_palm','body_touch',"
            "'verbal_shorthand','combined')",
            name="team_play_signal_kind_check",
        ),
        sa.CheckConstraint(
            "assigned_by IN ('ai','coach','team')",
            name="team_play_signal_assigned_by_check",
        ),
    )
    op.execute(
        "CREATE UNIQUE INDEX team_signal_uniqueness "
        "ON team_play_signal (team_id, signal_kind, (signal_detail->>'value'))"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS team_signal_uniqueness")
    op.drop_table("team_play_signal")
    op.drop_index("team_roster_attrs_gin", table_name="team_roster")
    op.drop_index("team_roster_team_idx", table_name="team_roster")
    op.drop_table("team_roster")
    op.drop_table("team")
    op.drop_index("coach_vocab_event_term_idx", table_name="coach_vocab_event")
    op.drop_index("coach_vocab_event_coach_time_idx", table_name="coach_vocab_event")
    op.drop_table("coach_vocab_event")
    op.drop_table("coach_concept_progress")
    op.drop_table("coach_profile")
