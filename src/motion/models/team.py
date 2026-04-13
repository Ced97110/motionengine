"""Team, roster, play signals.

Mirrors docs/specs/backend-architecture.md §3.2 and §3.3.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    PrimaryKeyConstraint,
    SmallInteger,
    String,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from motion.db import Base


class Team(Base):
    __tablename__ = "team"
    __table_args__ = (
        CheckConstraint("rules IN ('FIBA','NBA')", name="team_rules_check"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    head_coach_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("coach_profile.coach_id", ondelete="RESTRICT"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    level: Mapped[str] = mapped_column(String, nullable=False)
    rules: Mapped[str] = mapped_column(String, nullable=False, server_default="FIBA")
    region: Mapped[str | None] = mapped_column(String, nullable=True)
    season: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    roster: Mapped[list[TeamRoster]] = relationship(
        back_populates="team", cascade="all, delete-orphan"
    )
    signals: Mapped[list[TeamPlaySignal]] = relationship(
        back_populates="team", cascade="all, delete-orphan"
    )


class TeamRoster(Base):
    __tablename__ = "team_roster"
    __table_args__ = (
        Index("team_roster_team_idx", "team_id"),
        Index("team_roster_attrs_gin", "attributes", postgresql_using="gin"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    team_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("team.id", ondelete="CASCADE"),
        nullable=False,
    )
    player_ref: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    display_name: Mapped[str] = mapped_column(String, nullable=False)
    jersey_num: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    position: Mapped[str | None] = mapped_column(String, nullable=True)
    age_group: Mapped[str | None] = mapped_column(String, nullable=True)
    parental_consent_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    attributes: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, server_default=text("'{}'::jsonb")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    team: Mapped[Team] = relationship(back_populates="roster")


class TeamPlaySignal(Base):
    __tablename__ = "team_play_signal"
    # Note: functional unique index (team_id, signal_kind, signal_detail->>'value')
    # is defined in migration 0001 via raw SQL — Alembic autogenerate should ignore it.
    __table_args__ = (
        PrimaryKeyConstraint("team_id", "play_slug", name="team_play_signal_pk"),
        CheckConstraint(
            "signal_kind IN ('finger_count','closed_fist','open_palm','body_touch',"
            "'verbal_shorthand','combined')",
            name="team_play_signal_kind_check",
        ),
        CheckConstraint(
            "assigned_by IN ('ai','coach','team')", name="team_play_signal_assigned_by_check"
        ),
    )

    team_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("team.id", ondelete="CASCADE"),
        nullable=False,
    )
    play_slug: Mapped[str] = mapped_column(String, nullable=False)
    signal_kind: Mapped[str] = mapped_column(String, nullable=False)
    signal_detail: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    verbal_label: Mapped[str | None] = mapped_column(String, nullable=True)
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    assigned_by: Mapped[str] = mapped_column(String, nullable=False)

    team: Mapped[Team] = relationship(back_populates="signals")
