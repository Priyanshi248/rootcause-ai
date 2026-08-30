from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.timeline import TimelineEvent
from app.repositories.base_repository import BaseRepository


class TimelineRepository(BaseRepository[TimelineEvent]):

    def __init__(
        self,
        db: AsyncSession,
    ):
        super().__init__(
            db,
            TimelineEvent,
        )

    async def get_by_incident(
        self,
        incident_id: UUID,
    ) -> list[TimelineEvent]:

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