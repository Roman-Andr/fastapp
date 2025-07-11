import logging

from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from starlette.middleware.cors import CORSMiddleware

from fastapp.config import settings
from fastapp.core.database import engine
from fastapp.routers.auth_router import router as auth_router
from fastapp.routers.health_router import router as health_router
from fastapp.routers.task_router import router as task_router
from fastapp.routers.user_router import router as user_router

logger = logging.getLogger(__name__)


async def lifespan(_: FastAPI):
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            logger.info("Database connection established")
    except OperationalError as e:
        logger.critical(f"Failed to connect to database: {e}")
        raise RuntimeError("Database connection failed") from e

    yield

    await engine.dispose()


app = FastAPI(
    title=settings.title,
    lifespan=lifespan,
    exception_handlers={
        RateLimitExceeded: _rate_limit_exceeded_handler
    }
)

# app.state.limiter = limiter
# app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health_router)
app.include_router(task_router)
app.include_router(user_router)
app.include_router(auth_router)
