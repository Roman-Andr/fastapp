from fastapi import APIRouter

from fastapp.schemas.healthcheck_schema import HealthCheck

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    return HealthCheck(status="ok")
