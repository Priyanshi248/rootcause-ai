from fastapi import FastAPI
from app.api.incident import router as incident_router

app = FastAPI()
@app.get("/")
def root():
    return {
        "message": "Welcome to RootCause AI"
    }

app.include_router(incident_router)