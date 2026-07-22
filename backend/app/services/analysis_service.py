from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.agents.root_cause_agent import analyze_logs

from app.models.analysis import Analysis

from app.repositories.analysis_repository import AnalysisRepository
from app.repositories.log_repository import LogRepository

from app.services.timeline_service import TimelineService

from app.vectorstore.retrieval_service import RetrievalService
from app.repositories.incident_repository import IncidentRepository


class AnalysisService:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.logs = LogRepository(db)
        self.analysis = AnalysisRepository(db)
        self.incidents = IncidentRepository(db)
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

        retrieval = RetrievalService()

        similar_incidents = retrieval.search(
            log_text
        )

        context = "\n\n".join(
            similar_incidents
        )

        ai = await analyze_logs(
            log_text,
            context,
        )

        analysis = Analysis(
            incident_id=incident_id,

            summary=ai["summary"],

            root_cause=ai["root_cause"],

            suggested_fix=ai["suggested_fix"],

            follow_up_actions="\n".join(ai["follow_up_actions"])
            if isinstance(ai["follow_up_actions"], list)
            else ai["follow_up_actions"],

            model_used=settings.AI_MODEL,
        )

        saved_analysis = await self.analysis.create(
            analysis
        )

        incident = await self.incidents.get_incident(
            incident_id
        )

        retrieval.update_incident_knowledge(
            incident.id,
            incident.title,
            incident.description,
            incident.service_name,
            saved_analysis.summary,
            saved_analysis.root_cause,
            saved_analysis.suggested_fix,
            saved_analysis.follow_up_actions,
        )

        await self.timeline.create_event(
            incident_id=incident_id,
            event_type="AI_ANALYSIS_COMPLETED",
            description="AI generated root cause analysis.",
        )

        return {
            "summary": saved_analysis.summary,
            "root_cause": saved_analysis.root_cause,
            "suggested_fix": saved_analysis.suggested_fix,
            "follow_up_actions": saved_analysis.follow_up_actions,
            "retrieved_incidents": similar_incidents,
            "retrieved_count": len(similar_incidents),
}