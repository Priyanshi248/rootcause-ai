from sqlalchemy.ext.asyncio import AsyncSession

from app.models.incident import Incident
from app.repositories.incident_repository import IncidentRepository
from app.schemas.incident import IncidentCreate
from app.enums.incident import Status


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

        return await self.repository.create(incident)