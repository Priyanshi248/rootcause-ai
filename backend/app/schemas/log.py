from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums.log import LogSource


class LogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    incident_id: UUID
    filename: str
    source: LogSource
    content: str
    file_size: int
    created_at: datetime
    updated_at: datetime