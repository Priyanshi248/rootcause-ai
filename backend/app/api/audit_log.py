from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.core.permissions import require_roles

from app.schemas.audit_log import AuditLogResponse

from app.services.audit_log_service import AuditLogService

router = APIRouter()


@router.get(
    "/incidents/{incident_id}/audit",
    response_model=list[AuditLogResponse],
)
async def get_audit_logs(
    incident_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "ADMIN",
            "ENGINEER",
            "SRE",
            "VIEWER",
        )
    ),
):

    service = AuditLogService(db)

    return await service.get_audit_logs(
        incident_id
    )