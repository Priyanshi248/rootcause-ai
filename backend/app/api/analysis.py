from uuid import UUID

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.schemas.analysis import AnalysisResponse

from app.services.analysis_service import AnalysisService
from app.schemas.analysis_result import AnalysisResult

router = APIRouter()


@router.post(
    "/analysis/{incident_id}",
    response_model=AnalysisResult,
)
async def analyze_incident(
    incident_id: UUID,
    db: AsyncSession = Depends(
        get_db
    ),
):

    service = AnalysisService(
        db
    )

    return await service.analyze(
        incident_id
    )