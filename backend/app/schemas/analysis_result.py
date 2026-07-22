from pydantic import BaseModel


class AnalysisResult(BaseModel):

    summary: str

    root_cause: str

    suggested_fix: str

    follow_up_actions: str

    retrieved_incidents: list[str]

    retrieved_count: int