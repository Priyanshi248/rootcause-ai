from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.dashboard_repository import DashboardRepository


class DashboardService:

    def __init__(self, db: AsyncSession):
        self.repository = DashboardRepository(db)

    async def get_dashboard(self):
        return await self.repository.get_dashboard_stats()
