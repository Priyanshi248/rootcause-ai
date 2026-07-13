from fastapi import FastAPI

from app.api.incident import router as incident_router
from app.api.log import router as log_router
from app.api.analysis import router as analysis_router

from app.api.dashboard import router as dashboard_router

app = FastAPI(
    title="RootCause AI"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to RootCause AI"
    }

app.include_router(incident_router)

app.include_router(log_router)

app.include_router(analysis_router)

app.include_router(dashboard_router)