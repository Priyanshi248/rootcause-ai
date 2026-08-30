import pytest

from sqlalchemy import text

from app.db.session import engine


@pytest.mark.asyncio
async def test_connection():

    async with engine.begin() as conn:

        result = await conn.execute(
            text("SELECT version();")
        )

        version = result.scalar()

        print(version)

        assert version is not None