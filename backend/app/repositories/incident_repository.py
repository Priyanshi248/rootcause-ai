from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.incident import Incident
from app.repositories.base_repository import BaseRepository
from app.schemas.incident_query import IncidentQuery
from app.exceptions.incident import IncidentNotFoundException


class IncidentRepository(BaseRepository[Incident]):

    def __init__(
        self,
        db: AsyncSession,
    ):
        super().__init__(
            db,
            Incident,
        )

    async def get_incident(
        self,
        incident_id: UUID,
    ) -> Incident:

        incident = await self.get_by_id(
            incident_id
        )

        if incident is None:
            raise IncidentNotFoundException()

        return incident

    async def get_all(
        self,
        query: IncidentQuery,
    ) -> list[Incident]:

        stmt = select(Incident)

        if query.status:
            stmt = stmt.where(
                Incident.status == query.status
            )

        if query.severity:
            stmt = stmt.where(
                Incident.severity == query.severity
            )

        if query.environment:
            stmt = stmt.where(
                Incident.environment == query.environment
            )

        if query.search:
            stmt = stmt.where(
                or_(
                    Incident.title.ilike(
                        f"%{query.search}%"
                    ),
                    Incident.description.ilike(
                        f"%{query.search}%"
                    ),
                    Incident.service_name.ilike(
                        f"%{query.search}%"
                    ),
                )
            )

        stmt = (
            stmt
            .order_by(
                Incident.created_at.desc()
            )
            .offset(
                (query.page - 1) * query.limit
            )
            .limit(query.limit)
        )

        result = await self.db.execute(
            stmt
        )

        return result.scalars().all()