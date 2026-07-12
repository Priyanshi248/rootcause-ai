from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.analysis import Analysis


class AnalysisRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        analysis: Analysis,
    ) -> Analysis:

        self.db.add(analysis)

        await self.db.commit()

        await self.db.refresh(analysis)

        return analysis

    async def get_latest(
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

    async def get_all(
        self,
        incident_id: UUID,
    ) -> list[Analysis]:

        result = await self.db.execute(
            select(Analysis)
            .where(
                Analysis.incident_id == incident_id
            )
            .order_by(
                Analysis.created_at.desc()
            )
        )

        return result.scalars().all()