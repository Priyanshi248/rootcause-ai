from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog
from app.repositories.base_repository import BaseRepository


class AuditLogRepository(BaseRepository[AuditLog]):

    def __init__(
        self,
        db: AsyncSession,
    ):
        super().__init__(
            db,
            AuditLog,
        )

    async def get_by_incident(
        self,
        incident_id: UUID,
    ) -> list[AuditLog]:

        result = await self.db.execute(
            select(AuditLog)
            .where(
                AuditLog.incident_id == incident_id
            )
            .order_by(
                AuditLog.created_at.desc()
            )
        )

        return result.scalars().all()