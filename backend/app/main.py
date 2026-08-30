from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.analysis import router as analysis_router
from app.api.audit_log import router as audit_router
from app.api.auth import router as auth_router
from app.api.dashboard import router as dashboard_router
from app.api.incident import router as incident_router
from app.api.log import router as log_router
from app.api.timeline import router as timeline_router
from app.api.ai import router as ai_router

from app.exceptions.auth import (
    InvalidCredentialsException,
    UnauthorizedException,
)
from app.exceptions.incident import (
    IncidentNotFoundException,
)
from app.exceptions.user import (
    UserNotFoundException,
)

app = FastAPI(
    title="RootCause AI",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "https://rootcause-ai-sand.vercel.app/",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to RootCause AI 🚀"
    }


# ==========================
# Exception Handlers
# ==========================

@app.exception_handler(IncidentNotFoundException)
async def incident_not_found_handler(
    request: Request,
    exc: IncidentNotFoundException,
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": exc.message,
        },
    )


@app.exception_handler(UserNotFoundException)
async def user_not_found_handler(
    request: Request,
    exc: UserNotFoundException,
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": exc.message,
        },
    )


@app.exception_handler(InvalidCredentialsException)
async def invalid_credentials_handler(
    request: Request,
    exc: InvalidCredentialsException,
):
    return JSONResponse(
        status_code=401,
        content={
            "detail": exc.message,
        },
    )


@app.exception_handler(UnauthorizedException)
async def unauthorized_handler(
    request: Request,
    exc: UnauthorizedException,
):
    return JSONResponse(
        status_code=401,
        content={
            "detail": exc.message,
        },
    )


# ==========================
# Routers
# ==========================

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

app.include_router(
    audit_router,
    prefix="/audit",
    tags=["Audit Logs"],
)

app.include_router(
    ai_router,
    prefix="/ai",
    tags=["AI Assistant"],
)