from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.enums.incident import (
    Severity,
    Status,
    Environment,
)


class RecentIncident(BaseModel):
    id: UUID
    title: str
    severity: Severity
    status: Status
    environment: Environment
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class DashboardResponse(BaseModel):
    total_incidents: int

    open_incidents: int
    resolved_incidents: int

    critical_incidents: int
    high_incidents: int
    medium_incidents: int
    low_incidents: int

    production_incidents: int
    staging_incidents: int
    development_incidents: int

    recent_incidents: list[RecentIncident]