from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.log import LogSource
from app.models.log import Log
from app.repositories.log_repository import LogRepository
from app.services.timeline_service import TimelineService


class LogService:

    def __init__(self, db: AsyncSession):
        self.repository = LogRepository(db)
        self.timeline = TimelineService(db)

    async def upload_log(
        self,
        incident_id: UUID,
        source: LogSource,
        file: UploadFile,
    ) -> Log:

        content = await file.read()

        log = Log(
            incident_id=incident_id,
            filename=file.filename,
            source=source,
            content=content.decode("utf-8"),
            file_size=len(content),
        )

        log = await self.repository.create(log)

        await self.timeline.create_event(
            incident_id=incident_id,
            event_type="LOG_UPLOADED",
            description=f"Log file '{file.filename}' uploaded.",
        )

        return log