from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.incident import Status, Severity, Environment
from app.models.incident import Incident


class DashboardRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_dashboard_stats(self):

        async def count(condition):
            result = await self.db.execute(
                select(func.count()).select_from(Incident).where(condition)
            )
            return result.scalar() or 0

        total_result = await self.db.execute(
            select(func.count()).select_from(Incident)
        )
        total = total_result.scalar() or 0

        return {
            "total_incidents": total,

            "open_incidents": await count(
                Incident.status == Status.OPEN
            ),

            "resolved_incidents": await count(
                Incident.status == Status.RESOLVED
            ),

            "critical_incidents": await count(
                Incident.severity == Severity.CRITICAL
            ),

            "high_incidents": await count(
                Incident.severity == Severity.HIGH
            ),

            "medium_incidents": await count(
                Incident.severity == Severity.MEDIUM
            ),

            "low_incidents": await count(
                Incident.severity == Severity.LOW
            ),

            "production_incidents": await count(
                Incident.environment == Environment.PRODUCTION
            ),

            "staging_incidents": await count(
                Incident.environment == Environment.STAGING
            ),

            "development_incidents": await count(
                Incident.environment == Environment.DEVELOPMENT
            ),
        }