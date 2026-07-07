import uuid
from sqlalchemy import String, Text, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.mixins.timestamp import TimestampMixin
from app.enums.incident import (
    SeverityLevel,
    Environment,
    Status,
)

class Incident(TimestampMixin, Base):
    __tablename__ = "incidents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
    )

    title: Mapped[str] = mapped_column(String(200))

    description: Mapped[str] = mapped_column(Text)

    service_name: Mapped[str] = mapped_column(String(100))

    environment: Mapped[Environment] = mapped_column(SQLEnum(Environment))

    severity: Mapped[SeverityLevel] = mapped_column(SQLEnum(SeverityLevel))

    status: Mapped[Status] = mapped_column(SQLEnum(Status), default=Status.OPEN)

    assigned_engineer: Mapped[str|None] = mapped_column(String(100), nullable=True)