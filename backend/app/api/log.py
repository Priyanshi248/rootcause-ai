from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.enums.log import LogSource
from app.schemas.log import LogResponse
from app.services.log_service import LogService

router = APIRouter()


@router.post(
    "/logs/upload",
    response_model=LogResponse,
)
async def upload_log(
    incident_id: UUID = Form(...),
    source: LogSource = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):

    service = LogService(db)

    return await service.upload_log(
        incident_id=incident_id,
        source=source,
        file=file,
    )