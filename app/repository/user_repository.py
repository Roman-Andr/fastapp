from typing import Optional, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError

from app.core.database import DBSession
from app.core.security import get_password_hash
from app.models.user import UserModel
from app.schemas.user_schema import UserCreate


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_data: UserCreate) -> UserModel:
        try:
            stmt = (
                insert(UserModel)
                .values(
                    username=user_data.username,
                    email=user_data.email,
                    hashed_password=get_password_hash(user_data.password),
                    is_active=True
                )
                .returning(UserModel)
            )
            result = await self.db.execute(stmt)
            await self.db.commit()
            return result.scalar_one()
        except IntegrityError:
            await self.db.rollback()
            raise

    async def get_user_by_username(self, username: str) -> Optional[UserModel]:
        result = await self.db.execute(select(UserModel).where(UserModel.username == username))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[UserModel]:
        result = await self.db.execute(select(UserModel).where(UserModel.email == email))
        return result.scalar_one_or_none()


async def get_user_repository(db: DBSession):
    return UserRepository(db)


UserRepo = Annotated[UserRepository, Depends(get_user_repository)]
