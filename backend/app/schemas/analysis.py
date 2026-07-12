from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AnalysisResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    incident_id: UUID

    summary: str
    root_cause: str
    suggested_fix: str
    follow_up_actions: str

    model_used: str

    created_at: datetime
    updated_at: datetime