import os
from functools import cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


def _load_env():
    env_file = ".env.test" if os.getenv("TESTING") else ".env"
    load_dotenv(env_file)


@cache
def get_settings():
    _load_env()

    class Settings(BaseSettings):
        if os.getenv("TESTING"):
            sqlalchemy_database_url: str = "sqlite+aiosqlite:///:memory:"
        else:
            postgres_user: str = os.getenv("POSTGRES_USER")
            postgres_password: str = os.getenv("POSTGRES_PASSWORD")
            postgres_db: str = os.getenv("POSTGRES_DB")
            postgres_host: str = os.getenv("POSTGRES_HOST")
            postgres_port: int = os.getenv("POSTGRES_PORT", 5432)
            sqlalchemy_database_url: str = (
                f"postgresql+asyncpg://{postgres_user}:{postgres_password}@"
                f"{postgres_host}:{postgres_port}/{postgres_db}"
            )

        title: str = os.getenv("TITLE")

        secret_key: str = os.getenv("SECRET_KEY")
        algorithm: str = os.getenv("ALGORITHM", "HS256")
        refresh_token_expire_days: int = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7)
        access_token_expire_minutes: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)

        forbidden_usernames: list[str] = ["admin", "root", "system", "superuser"]

    return Settings()


settings = get_settings()
