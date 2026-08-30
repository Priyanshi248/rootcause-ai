from fastapi import HTTPException, status

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserLogin


class AuthService:

    def __init__(self, db):
        self.user_repository = UserRepository(db)

    async def register(
        self,
        user: UserCreate,
    ) -> User:

        existing_user = await self.user_repository.get_by_email(
            user.email
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        new_user = User(
            full_name=user.full_name,
            email=user.email,
            hashed_password=hash_password(user.password),
            role="ENGINEER",
        )

        return await self.user_repository.create(
            new_user
        )

    async def login(
        self,
        user: UserLogin,
    ) -> dict:

        db_user = await self.user_repository.get_by_email(
            user.email
        )

        if (
            db_user is None
            or not verify_password(
                user.password,
                db_user.hashed_password,
            )
        ):
            from app.exceptions.auth import (
                InvalidCredentialsException,
            )
            raise InvalidCredentialsException()

        access_token = create_access_token(
            {
                "sub": str(db_user.id),
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }