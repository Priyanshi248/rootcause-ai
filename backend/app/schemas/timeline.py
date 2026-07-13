from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class TimelineResponse(BaseModel):
    id: UUID
    incident_id: UUID
    event_type: str
    description: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }