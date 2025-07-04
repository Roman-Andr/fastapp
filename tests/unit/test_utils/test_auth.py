import pytest
from fastapi import HTTPException, status

from app.core.auth import create_access_token, create_refresh_token, authenticate_user
from tests.fixtures.users import USER_DEFAULT_USERNAME, USER_DEFAULT_PASSWORD


@pytest.mark.asyncio
async def test_create_access_token():
    token = create_access_token(data={"sub": "test"})
    assert isinstance(token, str)
    assert len(token) > 0


@pytest.mark.asyncio
async def test_create_refresh_token():
    token = create_refresh_token(data={"sub": "test"})
    assert isinstance(token, str)
    assert len(token) > 0


@pytest.mark.asyncio
async def test_authenticate_user_success(user_repository, user_create):
    await user_repository.create_user(user_create())
    user = await authenticate_user(user_repository, USER_DEFAULT_USERNAME, USER_DEFAULT_PASSWORD)

    assert user.username == USER_DEFAULT_USERNAME


@pytest.mark.asyncio
async def test_authenticate_user_wrong_password(user_repository, user_create):
    await user_repository.create_user(user_create())
    with pytest.raises(HTTPException) as exc_info:
        await authenticate_user(user_repository, USER_DEFAULT_USERNAME, "wrong_password")
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_authenticate_user_nonexistent(user_repository):
    with pytest.raises(HTTPException) as exc_info:
        await authenticate_user(user_repository, "nonexistent", "password")
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
