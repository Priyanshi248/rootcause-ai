from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.timeline import TimelineEvent
from app.repositories.timeline_repository import TimelineRepository


class TimelineService:

    def __init__(self, db: AsyncSession):
        self.repository = TimelineRepository(db)

    async def create_event(
        self,
        incident_id,
        event_type: str,
        description: str,
    ):

        event = TimelineEvent(
            incident_id=incident_id,
            event_type=event_type,
            description=description,
        )

        return await self.repository.create(
            event
        )

    async def get_timeline(
        self,
        incident_id: UUID,
    ):

        return await self.repository.get_by_incident(
            incident_id
        )