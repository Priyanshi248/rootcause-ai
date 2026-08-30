import uuid

from sqlalchemy import ForeignKey, Text, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.mixins.timestamp import TimestampMixin


class Analysis(TimestampMixin, Base):
    __tablename__ = "analysis"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    incident_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "incidents.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    executive_summary: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    summary: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    root_cause: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    confidence: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    confidence_reason: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    subcategory: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    affected_component: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    priority: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    severity_prediction: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    business_impact: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    immediate_actions: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    runbook: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    risk_if_ignored: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    prevention: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    suggested_fix: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    follow_up_actions: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    model_used: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    incident: Mapped["Incident"] = relationship(
        "Incident",
        back_populates="analyses",
    )