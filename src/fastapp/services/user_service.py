from datetime import timezone, datetime
from typing import Annotated

import jwt
from fastapi import Depends
from jwt import InvalidTokenError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapp.config import settings
from fastapp.core.database import DBSession
from fastapp.core.exceptions import UserNotFoundException, TokenExpiredException, InvalidTokenException, PermissionDeniedException, AlreadyExistsException
from fastapp.models.user import UserModel
from fastapp.repositories.user_repository import UserRepository
from fastapp.schemas.role_schema import UserRole
from fastapp.schemas.user_schema import UserCreate, UserOutput


class UserService:
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)

    async def create_user(self, user_data: UserCreate) -> UserOutput:
        if user_data.role in [UserRole.ADMIN, UserRole.MODERATOR]:
            raise PermissionDeniedException(detail="Cannot register with this role")

        try:
            return await self.repository.create_user(user_data)
        except IntegrityError:
            raise AlreadyExistsException(detail="Username or email already registered")

    async def delete_user(self, user_id: int) -> None:
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException()
        await self.repository.delete_user(user_id)

    async def update_user_role(self, user_id: int, new_role: UserRole) -> UserOutput:
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException()

        updated_user = await self.repository.update_user_role(user_id, new_role)
        return UserOutput.model_validate(updated_user)

    async def get_user_by_username(self, username: str) -> UserModel | None:
        return await self.repository.get_user_by_username(username)

    async def verify_refresh_token(self, token: str) -> UserModel:
        try:
            payload = jwt.decode(
                token,
                settings.secret_key,
                algorithms=[settings.algorithm]
            )

            if payload.get("type") != "refresh":
                raise InvalidTokenException(detail="Invalid token type")

            if datetime.now(timezone.utc) > datetime.fromtimestamp(payload["exp"], tz=timezone.utc):
                raise TokenExpiredException()

            username = payload.get("sub")
            if not username:
                raise InvalidTokenException(detail="Invalid token payload")

            user = await self.get_user_by_username(username)
            if not user:
                raise UserNotFoundException()

            return user

        except InvalidTokenError:
            raise InvalidTokenException()


def get_user_service(db: DBSession) -> UserService:
    return UserService(db)


UserServiceDeps = Annotated[UserService, Depends(get_user_service)]
