import asyncio

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.incident import Incident
from app.repositories.incident_repository import IncidentRepository


INCIDENT_ID = "6b36c218-a0b0-4b0f-81ae-2aab388fabe2"


async def test_lookup():

    async with SessionLocal() as db:

        print("\n==============================")
        print("DIRECT MODEL QUERY")
        print("==============================")

        result = await db.execute(
            select(Incident).where(
                Incident.id == INCIDENT_ID
            )
        )

        incident = result.scalar_one_or_none()

        print("Direct query result:")
        print(incident)

        if incident:
            print("ID:", incident.id)
            print("TITLE:", incident.title)

        print("\n==============================")
        print("REPOSITORY QUERY")
        print("==============================")

        repository = IncidentRepository(db)

        incident = await repository.get_by_id(
            INCIDENT_ID
        )

        print("Repository result:")
        print(incident)

        if incident:
            print("ID:", incident.id)
            print("TITLE:", incident.title)


asyncio.run(test_lookup())