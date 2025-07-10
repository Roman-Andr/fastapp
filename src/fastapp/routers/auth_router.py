from typing import Annotated

from fastapi import APIRouter, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm

from fastapp.core.auth import create_access_token, get_current_active_user, create_refresh_token, \
    authenticate_user
from fastapp.schemas.token_schema import Token, TokenWithRefresh
from fastapp.schemas.user_schema import UserOutput
from fastapp.services.user_service import UserServiceDeps

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
async def login_for_access_token(
    service: UserServiceDeps,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> TokenWithRefresh:
    user = await authenticate_user(service, form_data.username, form_data.password)
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh")
async def refresh_access_token(
    service: UserServiceDeps,
    refresh_token: str = Body(..., embed=True)
) -> Token:
    user = await service.verify_refresh_token(refresh_token)
    new_access_token = create_access_token(data={"sub": user.username})
    return {"access_token": new_access_token, "token_type": "bearer"}


@router.get("/me")
async def read_users_me(
    current_user: Annotated[UserOutput, Depends(get_current_active_user)],
) -> UserOutput:
    return current_user
