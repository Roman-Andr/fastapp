import asyncio
import os
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.database import Base
from app.models.task import TaskModel  # noqa
from app.models.user import UserModel  # noqa

load_dotenv(".env" if not os.getenv("TESTING") else ".env.test")

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata
print(target_metadata.tables)


def get_database_url():
    # First try to get from environment variables
    url = os.environ.get("SQLALCHEMY_DATABASE_URL")
    if url:
        return url

    # Fall back to alembic.ini configuration
    return config.get_main_option("sqlalchemy.url")


def run_migrations_offline():
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    connectable = create_async_engine(
        get_database_url(),
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(
            lambda sync_conn: context.configure(
                connection=sync_conn,
                target_metadata=target_metadata,
                compare_type=True,
            )
        )
        # Fix: Remove the connection argument when calling run_migrations
        await connection.run_sync(lambda sync_conn: context.run_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())