import asyncio

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.incident import Incident


async def check_incidents():

    async with SessionLocal() as db:

        result = await db.execute(
            select(Incident.id, Incident.title)
        )

        incidents = result.all()

        print("\nCURRENT INCIDENTS IN DATABASE:\n")

        if not incidents:
            print("NO INCIDENTS FOUND")

        for incident_id, title in incidents:
            print(
                f"ID: {incident_id} | TITLE: {title}"
            )


asyncio.run(check_incidents())