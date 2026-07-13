from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.agents.root_cause_agent import analyze_logs

from app.models.analysis import Analysis

from app.repositories.analysis_repository import AnalysisRepository
from app.repositories.log_repository import LogRepository

from app.services.timeline_service import TimelineService


class AnalysisService:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.logs = LogRepository(db)
        self.analysis = AnalysisRepository(db)
        self.timeline = TimelineService(db)

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

            model_used=settings.AI_MODEL,
        )

        analysis = await self.analysis.create(
            analysis
        )

        await self.timeline.create_event(
            incident_id=incident_id,
            event_type="AI_ANALYSIS_COMPLETED",
            description="AI generated root cause analysis using Gemini.",
        )

        return analysis