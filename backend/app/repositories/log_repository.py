from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.log import Log


class LogRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        log: Log,
    ) -> Log:

        self.db.add(log)

        await self.db.commit()

        await self.db.refresh(log)

        return log

    async def get_logs_by_incident(
        self,
        incident_id,
    ):

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