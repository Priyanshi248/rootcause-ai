from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.log import Log
from app.repositories.base_repository import BaseRepository


class LogRepository(BaseRepository[Log]):

    def __init__(
        self,
        db: AsyncSession,
    ):
        super().__init__(
            db,
            Log,
        )

    async def get_logs_by_incident(
        self,
        incident_id,
    ) -> list[Log]:

        result = await self.db.execute(
            select(Log).where(
                Log.incident_id == incident_id
            )
        )

        return result.scalars().all()

    async def get_log_text(
        self,
        incident_id,
    ) -> str:

        logs = await self.get_logs_by_incident(
            incident_id
        )

        return "\n\n".join(
            log.content
            for log in logs
        )