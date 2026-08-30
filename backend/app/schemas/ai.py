from typing import Literal

from pydantic import BaseModel


class AIRequest(BaseModel):

    task: Literal[
        "chat",
        "summary",
        "jira",
        "postmortem",
        "prevention",
    ]

    question: str | None = None

    incident_id: str | None = None


class AIResponse(BaseModel):

    response: str

    sources: list[str] = []