from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.agents.root_cause_agent import analyze_logs

from app.models.analysis import Analysis

from app.repositories.analysis_repository import AnalysisRepository
from app.repositories.log_repository import LogRepository


class AnalysisService:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.logs = LogRepository(db)
        self.analysis = AnalysisRepository(db)

    async def analyze(
        self,
        incident_id: UUID,
    ):

        logs = await self.logs.get_logs_by_incident(
            incident_id
        )

        if not logs:
            raise Exception(
                "No logs found."
            )

        log_text = "\n".join(
            log.content
            for log in logs
        )

        ai = await analyze_logs(
            log_text
        )

        analysis = Analysis(
            incident_id=incident_id,

            summary=ai["summary"],

            root_cause=ai["root_cause"],

            suggested_fix=ai["suggested_fix"],

            follow_up_actions=ai["follow_up_actions"],

            model_used=settings.GEMINI_MODEL,
        )

        return await self.analysis.create(
            analysis
        )