from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.timeline import TimelineEvent


class TimelineRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        event: TimelineEvent,
    ):
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)
        return event

    async def get_by_incident(
        self,
        incident_id: UUID,
    ):

        result = await self.db.execute(
            select(TimelineEvent)
            .where(
                TimelineEvent.incident_id == incident_id
            )
            .order_by(
                TimelineEvent.created_at.asc()
            )
        )

        return result.scalars().all()