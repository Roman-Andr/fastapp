import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from fastapp.core.database import Base

TEST_SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def db_engine():
    engine = create_async_engine(
        TEST_SQLALCHEMY_DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False}
    )
    return engine


@pytest.fixture
async def setup_db(db_engine):
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def async_db_session(db_engine, setup_db):
    async_session = async_sessionmaker(
        db_engine, expire_on_commit=False, autocommit=False, autoflush=False
    )
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture
def override_get_db(async_db_session):
    async def _override_get_db():
        yield async_db_session

    return _override_get_db
