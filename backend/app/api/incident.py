from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.incident import IncidentCreate, IncidentResponse
from app.services.incident_service import IncidentService

router = APIRouter()


@router.post("/incidents", response_model=IncidentResponse)
async def create_incident(
    incident: IncidentCreate,
    db: AsyncSession = Depends(get_db),
):
    service = IncidentService(db)
    return await service.create_incident(incident)