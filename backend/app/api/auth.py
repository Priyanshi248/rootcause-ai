from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user
from app.models.user import User

from app.db.session import get_db
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserLogin,
    Token,
)
from app.services.auth_service import AuthService


router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
)
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
):

    service = AuthService(db)

    return await service.register(user)

@router.post(
    "/login",
    response_model=Token,
)
async def login(
    user: UserLogin,
    db: AsyncSession = Depends(get_db),
):

    service = AuthService(db)

    return await service.login(user)

@router.get(
    "/me",
    response_model=UserResponse,
)
async def me(
    current_user: User = Depends(get_current_user),
):
    return current_user