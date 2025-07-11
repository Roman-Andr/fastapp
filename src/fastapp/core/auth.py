from datetime import timedelta, datetime, timezone
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy import select

from fastapp.config import settings
from fastapp.core.database import DBSession
from fastapp.core.exceptions import InvalidCredentialsException, InactiveUserException
from fastapp.core.security import verify_password
from fastapp.models.user import UserModel
from fastapp.repositories.user_repository import UserRepo
from fastapp.schemas.user_schema import UserOutput

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
REFRESH_TOKEN_EXPIRE_DAYS = settings.refresh_token_expire_days
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
TokenAuth = Annotated[str, Depends(oauth2_scheme)]


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def authenticate_user(repo: UserRepo, username: str, password: str):
    user = await repo.get_user_by_username(username)
    if not user or not verify_password(password, user.hashed_password):
        raise InvalidCredentialsException(detail="Incorrect username or password")
    return user


async def get_current_user(
    token: TokenAuth,
    db: DBSession
) -> UserOutput:
    credentials_exception = InvalidCredentialsException(detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    result = await db.execute(select(UserModel).where(UserModel.username == username))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return UserOutput.model_validate(user)


async def get_current_active_user(
    current_user: Annotated[UserOutput, Depends(get_current_user)]
) -> UserOutput:
    if not current_user.is_active:
        raise InactiveUserException()
    return current_user


ActiveUser = Annotated[UserOutput, Depends(get_current_active_user)]
