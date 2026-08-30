from uuid import UUID

from pydantic import BaseModel


class AnalysisResult(BaseModel):

    id: UUID
    incident_id: UUID

    executive_summary: str
    summary: str
    root_cause: str

    confidence: int
    confidence_reason: str

    category: str
    subcategory: str
    affected_component: str
    priority: str
    severity_prediction: str | None = None

    business_impact: str

    immediate_actions: str
    runbook: str
    risk_if_ignored: str
    prevention: str

    suggested_fix: str
    follow_up_actions: str

    model_used: str

    retrieved_incidents: list[str]
    retrieved_count: int