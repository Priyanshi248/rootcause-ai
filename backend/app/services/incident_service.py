from sqlalchemy.ext.asyncio import AsyncSession

from app.models.incident import Incident
from app.repositories.incident_repository import IncidentRepository
from app.schemas.incident import IncidentCreate
from app.schemas.incident_query import IncidentQuery
from app.schemas.incident_update import IncidentUpdate
from app.enums.incident import Status
from app.services.timeline_service import TimelineService


class IncidentService:

    def __init__(self, db: AsyncSession):
        self.repository = IncidentRepository(db)

    async def create_incident(
        self,
        incident_data: IncidentCreate,
    ) -> Incident:

        incident = Incident(
            title=incident_data.title,
            description=incident_data.description,
            service_name=incident_data.service_name,
            environment=incident_data.environment,
            severity=incident_data.severity,
            status=Status.OPEN,
        )

        incident = await self.repository.create(
            incident
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
    ):

        incident = await self.repository.get_incident(
            incident_id
        )

        timeline = TimelineService(
            self.repository.db
        )

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

        if (
            data.assigned_engineer is not None
            and data.assigned_engineer != incident.assigned_engineer
        ):

            incident.assigned_engineer = data.assigned_engineer

            await timeline.create_event(
                incident.id,
                "ENGINEER_ASSIGNED",
                f"Assigned to {incident.assigned_engineer}.",
            )

        return await self.repository.update(
            incident
        )

        incident = await self.repository.get_incident(
            incident_id
        )

        if data.status is not None:
            incident.status = data.status

        if data.severity is not None:
            incident.severity = data.severity

        if data.assigned_engineer is not None:
            incident.assigned_engineer = data.assigned_engineer

        incident = await self.repository.update(
            incident
        )

        return incident

    async def delete_incident(
        self,
        incident_id,
    ):

        incident = await self.repository.get_incident(
            incident_id
        )

        await self.repository.delete(
            incident
        )

        return {
            "message": "Incident deleted successfully."
        }