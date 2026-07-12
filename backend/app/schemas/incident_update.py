from pydantic import BaseModel

from app.enums.incident import Status, Severity


class IncidentUpdate(BaseModel):
    status: Status | None = None
    severity: Severity | None = None
    assigned_engineer: str | None = None