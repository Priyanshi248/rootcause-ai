from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AnalysisResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    incident_id: UUID

    executive_summary: str

    summary: str

    root_cause: str

    confidence: int

    category: str

    subcategory: str

    affected_component: str

    priority: str

    business_impact: str

    suggested_fix: str

    follow_up_actions: str

    confidence_reason: str

    immediate_actions: str

    runbook: str

    risk_if_ignored: str

    prevention: str

    model_used: str

    created_at: datetime
    updated_at: datetime