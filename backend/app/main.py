from fastapi import FastAPI

from app.api.incident import router as incident_router
from app.api.log import router as log_router
from app.api.analysis import router as analysis_router
from app.api.timeline import router as timeline_router
from app.api.dashboard import router as dashboard_router
from app.api.auth import router as auth_router

app = FastAPI(
    title="RootCause AI"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to RootCause AI"
    }

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"],
)

app.include_router(
    incident_router,
    prefix="/incidents",
    tags=["Incidents"],
)

app.include_router(
    log_router,
    prefix="/logs",
    tags=["Logs"],
)

app.include_router(
    analysis_router,
    prefix="/analysis",
    tags=["AI Analysis"],
)

app.include_router(
    dashboard_router,
    prefix="/dashboard",
    tags=["Dashboard"],
)

app.include_router(
    timeline_router,
    prefix="/timeline",
    tags=["Timeline"],
)