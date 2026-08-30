from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.analysis import Analysis
from app.repositories.base_repository import BaseRepository


class AnalysisRepository(BaseRepository[Analysis]):

    def __init__(
        self,
        db: AsyncSession,
    ):
        super().__init__(
            db,
            Analysis,
        )

    async def get_by_incident(
        self,
        incident_id: UUID,
    ) -> Analysis | None:

        result = await self.db.execute(
            select(Analysis)
            .where(
                Analysis.incident_id == incident_id
            )
            .order_by(
                Analysis.created_at.desc()
            )
        )

        return result.scalars().first()