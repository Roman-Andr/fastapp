# fastapp/core/database.py
from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

from fastapp.config import settings

engine = create_async_engine(
    settings.sqlalchemy_database_url,
    echo=False,
    connect_args={"check_same_thread": False} if "sqlite" in settings.sqlalchemy_database_url else {}
)

async_session_maker = async_sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


DBSession = Annotated[AsyncSession, Depends(get_db)]
