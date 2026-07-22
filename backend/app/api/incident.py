from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.incident_query import IncidentQuery
from app.services.incident_service import IncidentService
from app.core.permissions import require_roles
from app.models.user import User
from app.schemas.incident_update import IncidentUpdate
from app.db.session import get_db
from app.enums.incident import (
    Status,
    Severity,
    Environment,
)
from app.schemas.incident import (
    IncidentCreate,
    IncidentResponse,
)


router = APIRouter()


@router.post(
    "/incidents",
    response_model=IncidentResponse,
)
async def create_incident(
    incident: IncidentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "ENGINEER", "SRE")
    ),
):
    service = IncidentService(db)
    return await service.create_incident(incident)


@router.get(
    "/incidents/{incident_id}",
    response_model=IncidentResponse,
)
async def get_incident(
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
    service = IncidentService(db)
    return await service.get_incident(incident_id)

@router.patch(
    "/incidents/{incident_id}",
    response_model=IncidentResponse,
)
async def update_incident(
    incident_id: UUID,
    data: IncidentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "ENGINEER", "SRE")
    ),
):

    service = IncidentService(db)

    return await service.update_incident(
        incident_id,
        data,
    )

@router.get(
    "/incidents",
    response_model=list[IncidentResponse],
)
async def get_all_incidents(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),

    status: Status | None = None,
    severity: Severity | None = None,
    environment: Environment | None = None,

    search: str | None = None,

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

    query = IncidentQuery(
        page=page,
        limit=limit,
        status=status,
        severity=severity,
        environment=environment,
        search=search,
    )

    service = IncidentService(db)

    return await service.get_all_incidents(query)

@router.delete(
    "/incidents/{incident_id}",
)
async def delete_incident(
    incident_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN")
    ),
):

    service = IncidentService(db)

    return await service.delete_incident(
        incident_id
    )