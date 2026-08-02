from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog


class AuditLogRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        audit_log: AuditLog,
    ):

        self.db.add(audit_log)

        await self.db.commit()

        await self.db.refresh(audit_log)

        return audit_log

    async def get_by_incident(
        self,
        incident_id: UUID,
    ):

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