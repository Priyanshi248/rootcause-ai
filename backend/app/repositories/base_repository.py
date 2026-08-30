from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):

    def __init__(
        self,
        db: AsyncSession,
        model,
    ):
        self.db = db
        self.model = model

    async def create(
        self,
        obj: ModelType,
    ) -> ModelType:

        self.db.add(obj)

        await self.db.commit()

        await self.db.refresh(obj)

        return obj

    async def update(
        self,
        obj: ModelType,
    ) -> ModelType:

        await self.db.commit()

        await self.db.refresh(obj)

        return obj

    async def delete(
        self,
        obj: ModelType,
    ):

        await self.db.delete(obj)

        await self.db.commit()

    async def get_by_id(
        self,
        obj_id,
    ):

        result = await self.db.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )

        return result.scalar_one_or_none()