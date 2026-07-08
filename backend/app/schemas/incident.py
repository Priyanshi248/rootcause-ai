
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.enums.incident import (
    Severity,
    Environment,
    Status,
)

class IncidentCreate(BaseModel):
    title: str
    description: str
    service_name: str
    environment: Environment
    severity: Severity

class IncidentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str
    service_name: str
    environment: Environment
    severity: Severity
    status: Status
    created_at: datetime
    updated_at: datetime