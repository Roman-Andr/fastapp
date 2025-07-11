from fastapi import APIRouter, status

from fastapp.core.permissions import AdminDeps
from fastapp.schemas.role_schema import UserRole
from fastapp.schemas.user_schema import UserCreate, UserOutput
from fastapp.services.user_service import UserServiceDeps

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create new user",
    description="Register a new user account"
)
async def create_user(
    user: UserCreate,
    service: UserServiceDeps
) -> UserOutput:
    return await service.create_user(user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Delete a user account (admin only)"
)
async def delete_user(
    user_id: int,
    service: UserServiceDeps,
    _: AdminDeps
) -> None:
    await service.delete_user(user_id)
    return None


@router.patch(
    "/{user_id}/role",
    summary="Update user role",
    description="Update a user's role (admin only)"
)
async def update_user_role(
    user_id: int,
    new_role: UserRole,
    service: UserServiceDeps,
    _: AdminDeps
) -> UserOutput:
    return await service.update_user_role(user_id, new_role)
