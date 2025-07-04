from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.schemas.user_schema import UserCreate, UserOutput
from app.services.user_service import UserService, get_user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    service: Annotated[UserService, Depends(get_user_service)]
) -> UserOutput:
    return await service.create_user(user)
