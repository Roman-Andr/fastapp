from typing import Annotated

from fastapi import Depends
from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapp.core.database import DBSession
from fastapp.core.security import get_password_hash
from fastapp.models.user import UserModel
from fastapp.schemas.role_schema import UserRole
from fastapp.schemas.user_schema import UserCreate


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_data: UserCreate) -> UserModel:
        try:
            result = await self.db.execute(
                insert(UserModel)
                .values(
                    username=user_data.username,
                    email=user_data.email,
                    hashed_password=get_password_hash(user_data.password),
                    is_active=True,
                    role=user_data.role
                )
                .returning(UserModel)
            )
            await self.db.commit()
            return result.scalar_one()
        except IntegrityError:
            await self.db.rollback()
            raise

    async def delete_user(self, user_id: int) -> None:
        await self.db.execute(delete(UserModel).where(UserModel.id == user_id))
        await self.db.commit()

    async def update_user_role(self, user_id: int, new_role: UserRole) -> UserModel | None:
        await self.db.execute(
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(role=new_role)
        )
        await self.db.commit()
        return await self.get_user_by_id(user_id)

    async def get_user_by_id(self, user_id: int) -> UserModel | None:
        result = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> UserModel | None:
        result = await self.db.execute(select(UserModel).where(UserModel.username == username))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> UserModel | None:
        result = await self.db.execute(select(UserModel).where(UserModel.email == email))
        return result.scalar_one_or_none()


async def get_user_repository(db: DBSession):
    return UserRepository(db)


UserRepo = Annotated[UserRepository, Depends(get_user_repository)]
