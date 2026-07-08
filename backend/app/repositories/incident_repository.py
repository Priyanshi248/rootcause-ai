from sqlalchemy.ext.asyncio import AsyncSession

from app.models.incident import Incident


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