import uuid

from sqlalchemy import ForeignKey, Text, String
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

    summary: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    root_cause: Mapped[str] = mapped_column(
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
        String(50),
        nullable=False,
    )

    incident: Mapped["Incident"] = relationship(
        "Incident",
        back_populates="analyses",
    )