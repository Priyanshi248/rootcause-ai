from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class AuditLogResponse(BaseModel):
    id: UUID
    incident_id: UUID
    performed_by: UUID
    action: str
    old_value: str | None
    new_value: str | None
    created_at: datetime

    class Config:
        from_attributes = True