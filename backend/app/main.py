from fastapi import FastAPI
from app.api.incident import router as incident_router

app = FastAPI(title="RootCause AI", version="1.0.0",)
@app.get("/")
def root():
    return {
        "message": "Welcome to RootCause AI"
    }

app.include_router(
    incident_router,
    prefix="/api/v1",
    tags=["Incidents"],
)