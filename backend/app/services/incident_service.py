from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import (
    INCIDENT_CREATED,   
    STATUS_CHANGED,
    SEVERITY_CHANGED,
    ENGINEER_ASSIGNED,
)
from app.enums.incident import Status
from app.models.incident import Incident
from app.models.user import User
from app.repositories.incident_repository import IncidentRepository
from app.schemas.incident import IncidentCreate
from app.schemas.incident_query import IncidentQuery
from app.schemas.incident_update import IncidentUpdate
from app.services.audit_log_service import AuditLogService
from app.services.timeline_service import TimelineService
from app.vectorstore.retrieval_service import RetrievalService
from app.enums.role import Role

class IncidentService:

    def __init__(self, db: AsyncSession):

        self.db = db

        self.repository = IncidentRepository(db)

        self.timeline = TimelineService(db)

        self.audit = AuditLogService(db)

        self.retrieval = RetrievalService()

    async def _check_permission(
        self,
        incident: Incident,
        current_user: User,
    ):
        # Admin and SRE can modify every incident
        if current_user.role in {
            Role.ADMIN.value,
            Role.SRE.value,
        }:
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

        self.retrieval.add_incident(
            incident.id,
            incident.title,
            incident.description,
            incident.service_name,
        )

        await self.timeline.create_event(
            incident.id,
            INCIDENT_CREATED,
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
    ) -> list[Incident]:
        return await self.repository.get_all(
            query
        )

    async def update_incident(
        self,
        incident_id,
        data: IncidentUpdate,
        current_user: User,
    ) -> Incident:

        incident = await self.repository.get_incident(
            incident_id
        )

        await self._check_permission(
            incident,
            current_user,
        )

        await self._update_status(
            incident,
            data,
            current_user,
        )

        await self._update_severity(
            incident,
            data,
            current_user,
        )

        await self._update_assignment(
            incident,
            data,
            current_user,
        )

        return await self.repository.update(
            incident
        )

    # ---------------- STATUS ----------------
    async def _record_change(
        self,
        incident: Incident,
        current_user: User,
        action: str,
        old_value,
        new_value,
        message: str,
    ):

        await self.timeline.create_event(
            incident.id,
            action,
            message,
        )

        await self.audit.log_action(
            incident_id=incident.id,
            performed_by=current_user.id,
            action=action,
            old_value=str(old_value) if old_value is not None else None,
            new_value=str(new_value) if new_value is not None else None,
        )

    async def _update_status(
        self,
        incident: Incident,
        data: IncidentUpdate,
        current_user: User,
    ):

        if (
            data.status is None
            or data.status == incident.status
        ):
            return

        old_status = incident.status

        incident.status = data.status

        await self._record_change(
            incident,
            current_user,
            STATUS_CHANGED,
            old_status.value,
            incident.status.value,
            f"Status changed from {old_status.value} to {incident.status.value}.",
        )
    # ---------------- SEVERITY ----------------
    async def _update_severity(
        self,
        incident: Incident,
        data: IncidentUpdate,
        current_user: User,
    ):

        if (
            data.severity is None
            or data.severity == incident.severity
        ):
            return

        old_severity = incident.severity

        incident.severity = data.severity

        await self._record_change(
            incident,
            current_user,
            SEVERITY_CHANGED,
            old_severity.value,
            incident.severity.value,
            f"Severity changed from {old_severity.value} to {incident.severity.value}.",
        )

    # ---------------- ASSIGNED ENGINEER ----------------
    async def _update_assignment(
        self,
        incident: Incident,
        data: IncidentUpdate,
        current_user: User,
    ):

        if (
            data.assigned_engineer is None
            or data.assigned_engineer == incident.assigned_engineer
        ):
            return

        old_engineer = incident.assigned_engineer

        incident.assigned_engineer = data.assigned_engineer

        await self._record_change(
            incident,
            current_user,
            ENGINEER_ASSIGNED,
            old_engineer,
            incident.assigned_engineer,
            f"Assigned to {incident.assigned_engineer}.",
        )

    async def delete_incident(
        self,
        incident_id,
        current_user: User,
    )-> dict:

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