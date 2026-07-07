from fastapi import APIRouter
from app.schemas.incident import IncidentCreate

router = APIRouter()

@router.post("/incidents")
async def create_incident(incident: IncidentCreate):  
    return incident

#Take the incoming JSON, validate it against the IncidentCreate schema, and convert it into a Python object.
    