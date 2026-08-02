from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog
from app.repositories.audit_log_repository import AuditLogRepository


class AuditLogService:

    def __init__(self, db: AsyncSession):
        self.repository = AuditLogRepository(db)

    async def log_action(
        self,
        incident_id: UUID,
        performed_by: UUID,
        action: str,
        old_value: str | None = None,
        new_value: str | None = None,
    ):

        audit = AuditLog(
            incident_id=incident_id,
            performed_by=performed_by,
            action=action,
            old_value=old_value,
            new_value=new_value,
        )

        return await self.repository.create(
            audit
        )

    async def get_audit_logs(
        self,
        incident_id: UUID,
    ):
        return await self.repository.get_by_incident(
            incident_id
        )    