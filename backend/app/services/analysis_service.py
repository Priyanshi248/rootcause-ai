from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.parser import LogParser
from app.core.config import settings
from app.agents.root_cause_agent import analyze_logs

from app.models.analysis import Analysis

from app.repositories.analysis_repository import AnalysisRepository
from app.repositories.log_repository import LogRepository
from app.repositories.incident_repository import IncidentRepository

from app.services.timeline_service import TimelineService

from app.vectorstore.retrieval_service import RetrievalService


class AnalysisService:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.logs = LogRepository(db)
        self.analysis = AnalysisRepository(db)
        self.incidents = IncidentRepository(db)
        self.timeline = TimelineService(db)

    # ==================================================
    # ANALYZE INCIDENT
    # ==================================================

    async def analyze(
        self,
        incident_id: UUID,
    ):

        # --------------------------------------------------
        # 1. GET INCIDENT
        # --------------------------------------------------

        incident = await self.incidents.get_incident(
            incident_id
        )

        # --------------------------------------------------
        # 2. GET LOGS
        # --------------------------------------------------

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

        # --------------------------------------------------
        # 3. PARSE LOGS
        # --------------------------------------------------

        parsed = LogParser.parse(
            log_text
        )

        # --------------------------------------------------
        # 4. RETRIEVE SIMILAR INCIDENTS
        # --------------------------------------------------

        retrieval = RetrievalService()

        similar_incidents = retrieval.search(
            log_text
        )

        context = "\n\n".join(
            similar_incidents
        )

        # --------------------------------------------------
        # 5. AI ROOT CAUSE ANALYSIS
        # --------------------------------------------------

        ai = await analyze_logs(
            logs=log_text,
            context=context,
            parsed_logs=parsed,
        )

        # --------------------------------------------------
        # 6. SAVE ANALYSIS
        # --------------------------------------------------

        analysis = Analysis(
            incident_id=incident_id,

            executive_summary=ai.get(
                "executive_summary",
                "",
            ),

            summary=ai.get(
                "summary",
                "",
            ),

            root_cause=ai.get(
                "root_cause",
                "",
            ),

            confidence=ai.get(
                "confidence",
                0,
            ),

            confidence_reason=ai.get(
                "confidence_reason",
                "",
            ),

            category=ai.get(
                "category",
                "Unknown",
            ),

            subcategory=ai.get(
                "subcategory",
                "Unknown",
            ),

            affected_component=ai.get(
                "affected_component",
                "Unknown",
            ),

            priority=ai.get(
                "priority",
                "UNKNOWN",
            ),

            business_impact=ai.get(
                "business_impact",
                "",
            ),

            immediate_actions="\n".join(
                ai.get(
                    "immediate_actions",
                    [],
                )
            )
            if isinstance(
                ai.get(
                    "immediate_actions",
                    [],
                ),
                list,
            )
            else ai.get(
                "immediate_actions",
                "",
            ),

            runbook="\n".join(
                ai.get(
                    "runbook",
                    [],
                )
            )
            if isinstance(
                ai.get(
                    "runbook",
                    []),
                list,
            )
            else ai.get(
                "runbook",
                "",
            ),

            risk_if_ignored=ai.get(
                "risk_if_ignored",
                "",
            ),

            prevention=ai.get(
                "prevention",
                "",
            ),

            suggested_fix=ai.get(
                "suggested_fix",
                "",
            ),

            follow_up_actions="\n".join(
                ai.get(
                    "follow_up_actions",
                    [],
                )
            )
            if isinstance(
                ai.get(
                    "follow_up_actions",
                    [],
                ),
                list,
            )
            else ai.get(
                "follow_up_actions",
                "",
            ),

            model_used=settings.AI_MODEL,
        )

        # --------------------------------------------------
        # SAVE TO DATABASE
        # --------------------------------------------------

        saved_analysis = await self.analysis.create(
            analysis
        )

        # --------------------------------------------------
        # 7. UPDATE RAG KNOWLEDGE BASE
        # --------------------------------------------------

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

        # --------------------------------------------------
        # 8. CREATE TIMELINE EVENT
        # --------------------------------------------------

        await self.timeline.create_event(
            incident_id=incident_id,
            event_type="AI_ANALYSIS_COMPLETED",
            description="AI generated root cause analysis.",
        )

        # --------------------------------------------------
        # 9. RETURN RESULT
        # --------------------------------------------------

        return {
            "id": saved_analysis.id,

            "incident_id":
                saved_analysis.incident_id,

            "executive_summary":
                saved_analysis.executive_summary,

            "summary":
                saved_analysis.summary,

            "root_cause":
                saved_analysis.root_cause,

            "confidence":
                saved_analysis.confidence,

            "confidence_reason":
                saved_analysis.confidence_reason,

            "category":
                saved_analysis.category,

            "subcategory":
                saved_analysis.subcategory,

            "affected_component":
                saved_analysis.affected_component,

            "priority":
                saved_analysis.priority,

            "business_impact":
                saved_analysis.business_impact,

            "immediate_actions":
                saved_analysis.immediate_actions,

            "runbook":
                saved_analysis.runbook,

            "risk_if_ignored":
                saved_analysis.risk_if_ignored,

            "prevention":
                saved_analysis.prevention,

            "suggested_fix":
                saved_analysis.suggested_fix,

            "follow_up_actions":
                saved_analysis.follow_up_actions,

            "model_used":
                saved_analysis.model_used,

            "retrieved_incidents":
                similar_incidents,

            "retrieved_count":
                len(similar_incidents),
        }

    # ==================================================
    # GET SAVED ANALYSIS
    # ==================================================

    async def get_analysis(
        self,
        incident_id: UUID,
    ):

        analysis = await self.analysis.get_by_incident(
            incident_id
        )

        if not analysis:
            raise Exception(
                "Analysis not found."
            )

        return {
            "id": analysis.id,

            "incident_id":
                analysis.incident_id,

            "executive_summary":
                analysis.executive_summary,

            "summary":
                analysis.summary,

            "root_cause":
                analysis.root_cause,

            "confidence":
                analysis.confidence,

            "confidence_reason":
                analysis.confidence_reason,

            "category":
                analysis.category,

            "subcategory":
                analysis.subcategory,

            "affected_component":
                analysis.affected_component,

            "priority":
                analysis.priority,

            "severity_prediction":
                analysis.severity_prediction,

            "business_impact":
                analysis.business_impact,

            "immediate_actions":
                analysis.immediate_actions,

            "runbook":
                analysis.runbook,

            "risk_if_ignored":
                analysis.risk_if_ignored,

            "prevention":
                analysis.prevention,

            "suggested_fix":
                analysis.suggested_fix,

            "follow_up_actions":
                analysis.follow_up_actions,

            "model_used":
                analysis.model_used,

            "retrieved_incidents": [],

            "retrieved_count": 0,
        }