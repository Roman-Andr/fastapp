import logging
from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from tenacity import retry, stop_after_attempt, wait_exponential

from fastapp.config import settings
from fastapp.core.exceptions import DatabaseOperationException, DatabaseConnectionException

logger = logging.getLogger(__name__)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True
)
def create_db_engine():
    try:
        return create_async_engine(
            settings.sqlalchemy_database_url,
            echo=False,
            pool_pre_ping=True,
            pool_size=20,
            max_overflow=10,
            pool_recycle=3600,
            connect_args={
                "check_same_thread": False
            } if "sqlite" in settings.sqlalchemy_database_url else {}
        )
    except Exception as e:
        logger.error(f"Failed to create database engine: {e}")
        raise DatabaseConnectionException()


engine = create_db_engine()

async_session_maker = async_sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as ext:
            await session.rollback()
            logger.error(f"Database error occurred: {ext}")
            raise DatabaseOperationException()
        finally:
            await session.close()


DBSession = Annotated[AsyncSession, Depends(get_db)]
