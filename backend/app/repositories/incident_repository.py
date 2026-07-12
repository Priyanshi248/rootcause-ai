from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import select, or_
from app.models.incident import Incident
from fastapi import HTTPException
from app.schemas.incident_query import IncidentQuery


class IncidentRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        incident: Incident,
    ) -> Incident:

        self.db.add(incident)

        await self.db.commit()

        await self.db.refresh(incident)

        return incident
    
    async def get_by_id(
        self,
        incident_id: UUID,
    ) -> Incident | None:

        result = await self.db.execute(
            select(Incident).where(Incident.id == incident_id)
        )

        return result.scalar_one_or_none()
    
    async def get_incident(
        self,
    incident_id: UUID,
    ) -> Incident:
        incident = await self.get_by_id(incident_id)
        
        if incident is None:
            raise HTTPException(
                status_code=404,
                detail="Incident not found",
            )

        return incident


    async def get_all(
        self,
        query: IncidentQuery,
    ):

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
            .offset(
                (query.page - 1) * query.limit
            )
            .limit(query.limit)
            .order_by(
                Incident.created_at.desc()
            )
        )

        result = await self.db.execute(
            stmt
        )

        return result.scalars().all()


    async def update(
        self,
        incident: Incident,
    ) -> Incident:

        await self.db.commit()

        await self.db.refresh(incident)

        return incident

    async def delete(
        self,
        incident: Incident,
    ):

        await self.db.delete(incident)

        await self.db.commit()