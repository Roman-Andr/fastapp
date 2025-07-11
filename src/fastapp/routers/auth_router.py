from typing import Annotated

from fastapi import APIRouter, Depends, Body, Request
from fastapi.security import OAuth2PasswordRequestForm

from fastapp.core.auth import create_access_token, create_refresh_token, \
    authenticate_user, ActiveUser
from fastapp.schemas.token_schema import Token, TokenWithRefresh
from fastapp.schemas.user_schema import UserOutput
from fastapp.services.user_service import UserServiceDeps

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/token",
    summary="Login for access token",
    description="Authenticate user and return access and refresh tokens"
)
# @limiter.limit("1/minute")
async def login_for_access_token(
    request: Request,  # noqa
    service: UserServiceDeps,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenWithRefresh:
    user = await authenticate_user(service, form_data.username, form_data.password)
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    return TokenWithRefresh(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post(
    "/refresh",
    summary="Refresh access token",
    description="Generate new access token using refresh token"
)
# @limiter.limit("1/minute")
async def refresh_access_token(
    request: Request,  # noqa
    service: UserServiceDeps,
    refresh_token: Annotated[str, Body(..., embed=True)],
) -> Token:
    user = await service.verify_refresh_token(refresh_token)
    new_access_token = create_access_token(data={"sub": user.username})
    return {"access_token": new_access_token, "token_type": "bearer"}


@router.get(
    "/me",
    summary="Get current user",
    description="Retrieve information about the currently authenticated user"
)
async def read_users_me(
    current_user: ActiveUser,
) -> UserOutput:
    return current_user
