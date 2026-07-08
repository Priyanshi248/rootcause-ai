import uuid

from sqlalchemy import String, Text, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.enums.incident import (
    Severity, 
    Status,
    Environment,
)
from app.mixins.timestamp import TimestampMixin


class Incident(TimestampMixin, Base):
    __tablename__ = "incidents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    service_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    environment: Mapped[Environment] = mapped_column(
        SQLEnum(Environment),
        nullable=False,
    )

    severity: Mapped[Severity] = mapped_column(
        SQLEnum(Severity),
        nullable=False,
    )

    status: Mapped[Status] = mapped_column(
        SQLEnum(Status),
        default=Status.OPEN,
        nullable=False,
    )

    assigned_engineer: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )