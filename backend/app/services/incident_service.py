from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.incident import Incident
from app.repositories.incident_repository import IncidentRepository
from app.schemas.incident import IncidentCreate
from app.schemas.incident_query import IncidentQuery
from app.schemas.incident_update import IncidentUpdate
from app.enums.incident import Status
from app.services.timeline_service import TimelineService
from app.vectorstore.retrieval_service import RetrievalService
from app.services.audit_log_service import AuditLogService


class IncidentService:

    def __init__(self, db: AsyncSession):
        self.repository = IncidentRepository(db)

    async def _check_permission(
        self,
        incident: Incident,
        current_user: User,
    ):
        # Admin and SRE can modify every incident
        if current_user.role in ["ADMIN", "SRE"]:
            return

        # Engineers can modify only their own incidents
        if incident.created_by != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to modify this incident.",
            )

    async def create_incident(
        self,
        incident_data: IncidentCreate,
        current_user: User,
    ) -> Incident:

        incident = Incident(
            title=incident_data.title,
            description=incident_data.description,
            service_name=incident_data.service_name,
            environment=incident_data.environment,
            severity=incident_data.severity,
            status=Status.OPEN,
            created_by=current_user.id,
        )

        incident = await self.repository.create(
            incident,
        )

        retrieval = RetrievalService()

        retrieval.add_incident(
            incident.id,
            incident.title,
            incident.description,
            incident.service_name,
        )

        timeline = TimelineService(
            self.repository.db
        )

        await timeline.create_event(
            incident.id,
            "INCIDENT_CREATED",
            f"Incident '{incident.title}' was created.",
        )

        return incident

    async def get_incident(
        self,
        incident_id,
    ):
        return await self.repository.get_incident(
            incident_id
        )

    async def get_all_incidents(
        self,
        query: IncidentQuery,
    ):
        return await self.repository.get_all(
            query
        )

    async def update_incident(
        self,
        incident_id,
        data: IncidentUpdate,
        current_user: User,
    ):

        incident = await self.repository.get_incident(
            incident_id
        )

        await self._check_permission(
            incident,
            current_user,
        )

        audit = AuditLogService(
            self.repository.db
        )

        timeline = TimelineService(
            self.repository.db
        )

    # ---------------- STATUS ----------------
        if (
            data.status is not None
            and data.status != incident.status
        ):

            old_status = incident.status

            incident.status = data.status

            await timeline.create_event(
                incident.id,
                "STATUS_CHANGED",
                f"Status changed from {old_status.value} to {incident.status.value}.",
            )

            await audit.log_action(
                incident_id=incident.id,
                performed_by=current_user.id,
                action="STATUS_CHANGED",
                old_value=old_status.value,
                new_value=incident.status.value,
            )

    # ---------------- SEVERITY ----------------
        if (
            data.severity is not None
            and data.severity != incident.severity
        ):

            old_severity = incident.severity

            incident.severity = data.severity

            await timeline.create_event(
                incident.id,
                "SEVERITY_CHANGED",
                f"Severity changed from {old_severity.value} to {incident.severity.value}.",
            )

            await audit.log_action(
                incident_id=incident.id,
                performed_by=current_user.id,
                action="SEVERITY_CHANGED",
                old_value=old_severity.value,
                new_value=incident.severity.value,
            )

    # ---------------- ASSIGNED ENGINEER ----------------
        if (
            data.assigned_engineer is not None
            and data.assigned_engineer != incident.assigned_engineer
        ):

            old_engineer = incident.assigned_engineer

            incident.assigned_engineer = data.assigned_engineer

            await timeline.create_event(
                incident.id,
                "ENGINEER_ASSIGNED",
                f"Assigned to {incident.assigned_engineer}.",
            )

            await audit.log_action(
                incident_id=incident.id,
                performed_by=current_user.id,
                action="ENGINEER_ASSIGNED",
                old_value=old_engineer,
                new_value=incident.assigned_engineer,
            )

        return await self.repository.update(
            incident
        )

    async def delete_incident(
        self,
        incident_id,
        current_user: User,
    ):

        incident = await self.repository.get_incident(
            incident_id
        )

        await self._check_permission(
            incident,
            current_user,
        )

        await self.repository.delete(
            incident
        )

        return {
            "message": "Incident deleted successfully."
        }