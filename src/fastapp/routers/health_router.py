import logging

from fastapi import APIRouter, Response
from sqlalchemy import text

from fastapp.core.database import engine, status

router = APIRouter(tags=["health"])
logger = logging.getLogger(__name__)


@router.get("/health", include_in_schema=False)
async def health_check():
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return Response(
            content={"status": "unavailable", "database": "disconnected"},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
