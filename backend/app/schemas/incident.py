
from pydantic import BaseModel

from app.enums.incident import (
    SeverityLevel,
    Environment,
    Status,
)

class IncidentCreate(BaseModel):
    title: str
    description: str
    service_name: str
    environment: Environment
    severity: SeverityLevel

from uuid import UUID
from datetime import datetime

class IncidentResponse(BaseModel):
    id: UUID
    title: str
    description: str
    service_name: str
    environment: Environment
    severity: SeverityLevel
    status: Status
    created_at: datetime
    updated_at: datetime