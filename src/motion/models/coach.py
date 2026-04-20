"""Coach profile, concept progress, vocab events.

Mirrors backend/spec/architecture.md §3.1 and frontend/docs/specs/coach-profile.md.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    SmallInteger,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from motion.db import Base


class CoachProfile(Base):
    __tablename__ = "coach_profile"
    __table_args__ = (
        CheckConstraint(
            "level IN ('unknown','beginner','intermediate','advanced')",
            name="coach_profile_level_check",
        ),
        CheckConstraint(
            "years_coaching IS NULL OR (years_coaching BETWEEN 0 AND 80)",
            name="coach_profile_years_range",
        ),
        CheckConstraint(
            "level_coached IS NULL OR level_coached IN "
            "('u10','u12','u14','u16','hs','college','pro','mixed')",
            name="coach_profile_level_coached_check",
        ),
    )

    coach_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    level: Mapped[str] = mapped_column(String, nullable=False, server_default="unknown")
    years_coaching: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    level_coached: Mapped[str | None] = mapped_column(String, nullable=True)
    region: Mapped[str | None] = mapped_column(String, nullable=True)
    onboarded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    concept_progress: Mapped[list[CoachConceptProgress]] = relationship(
        back_populates="coach", cascade="all, delete-orphan"
    )
    vocab_events: Mapped[list[CoachVocabEvent]] = relationship(
        back_populates="coach", cascade="all, delete-orphan"
    )


class CoachConceptProgress(Base):
    __tablename__ = "coach_concept_progress"
    __table_args__ = (
        CheckConstraint(
            "status IN ('locked','introduced','mastered')",
            name="coach_concept_status_check",
        ),
    )

    coach_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("coach_profile.coach_id", ondelete="CASCADE"),
        primary_key=True,
    )
    concept_slug: Mapped[str] = mapped_column(String, primary_key=True)
    status: Mapped[str] = mapped_column(String, nullable=False)
    introduced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    mastered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    coach: Mapped[CoachProfile] = relationship(back_populates="concept_progress")


class CoachVocabEvent(Base):
    __tablename__ = "coach_vocab_event"
    __table_args__ = (
        CheckConstraint(
            "event_type IN ('definition-tap','play-used','concept-search')",
            name="coach_vocab_event_type_check",
        ),
        Index("coach_vocab_event_coach_time_idx", "coach_id", "occurred_at"),
        Index("coach_vocab_event_term_idx", "term"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    coach_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("coach_profile.coach_id", ondelete="CASCADE"),
        nullable=False,
    )
    term: Mapped[str] = mapped_column(String, nullable=False)
    event_type: Mapped[str] = mapped_column(String, nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    coach: Mapped[CoachProfile] = relationship(back_populates="vocab_events")
