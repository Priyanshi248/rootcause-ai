from fastapi import HTTPException, status

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    UserCreate,
    UserLogin,
)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)


class AuthService:

    def __init__(self, db):

        self.user_repo = UserRepository(db)

    async def register(
        self,
        user: UserCreate,
    ):

        existing = await self.user_repo.get_by_email(
            user.email
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Email already registered",
            )

        db_user = User(
            full_name=user.full_name,
            email=user.email,
            hashed_password=hash_password(user.password),
            role="ENGINEER",
        )

        return await self.user_repo.create(
            db_user
        )

    async def login(
        self,
        user: UserLogin,
    ):

        db_user = await self.user_repo.get_by_email(
            user.email
        )

        if (
            not db_user
            or not verify_password(
                user.password,
                db_user.hashed_password,
            )
        ):

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        token = create_access_token(
            {
                "sub": str(db_user.id)
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }