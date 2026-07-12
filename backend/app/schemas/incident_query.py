from typing import Optional

from pydantic import BaseModel

from app.enums.incident import (
    Status,
    Severity,
    Environment,
)


class IncidentQuery(BaseModel):
    page: int = 1
    limit: int = 10

    status: Optional[Status] = None
    severity: Optional[Severity] = None
    environment: Optional[Environment] = None

    search: Optional[str] = None