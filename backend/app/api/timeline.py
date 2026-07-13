from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.timeline import TimelineResponse
from app.services.timeline_service import TimelineService

router = APIRouter()


@router.get(
    "/timeline/{incident_id}",
    response_model=list[TimelineResponse],
)
async def get_timeline(
    incident_id: UUID,
    db: AsyncSession = Depends(get_db),
):

    service = TimelineService(db)

    return await service.get_timeline(
        incident_id
    )