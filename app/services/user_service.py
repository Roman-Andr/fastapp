from datetime import timezone, datetime
from typing import Optional, Annotated

import jwt
from fastapi import HTTPException, status, Depends
from jwt import InvalidTokenError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.database import DBSession
from app.models.user import UserModel
from app.repository.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserOutput


class UserService:
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)

    async def create_user(self, user_data: UserCreate) -> UserOutput:
        forbidden_usernames = ["admin", "root", "system"]
        if user_data.username.lower() in forbidden_usernames:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This username is not allowed"
            )

        try:
            return await self.repository.create_user(user_data)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already registered"
            )

    async def get_user_by_username(self, username: str) -> Optional[UserModel]:
        return await self.repository.get_user_by_username(username)

    async def verify_refresh_token(self, token: str) -> UserModel:
        try:
            payload = jwt.decode(
                token,
                settings.secret_key,
                algorithms=[settings.algorithm]
            )

            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid token type"
                )

            if datetime.now(timezone.utc) > datetime.fromtimestamp(payload["exp"], tz=timezone.utc):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expired"
                )

            username = payload.get("sub")
            if not username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid token payload"
                )

            user = await self.get_user_by_username(username)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            return user

        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token"
            )


def get_user_service(db: DBSession) -> UserService:
    return UserService(db)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
