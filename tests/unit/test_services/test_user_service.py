import pytest
from fastapi import HTTPException, status

from tests.fixtures.users import USER_DEFAULT_USERNAME, USER_DEFAULT_EMAIL


@pytest.mark.asyncio
async def test_create_user(user_service, user_create):
    user = await user_service.create_user(user_create())

    assert user.id is not None
    assert user.username == USER_DEFAULT_USERNAME
    assert user.email == USER_DEFAULT_EMAIL


@pytest.mark.asyncio
async def test_create_user_with_forbidden_username(user_service, user_create):
    with pytest.raises(HTTPException) as exc_info:
        await user_service.create_user(user_create(username="admin"))
    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_create_user_duplicate(user_service, user_create):
    await user_service.create_user(user_create())
    with pytest.raises(HTTPException) as exc_info:
        await user_service.create_user(user_create())
    assert exc_info.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_verify_refresh_token(user_service, user_create, test_user):
    from fastapp.core.auth import create_refresh_token

    refresh_token = create_refresh_token(data={"sub": test_user.username})
    user = await user_service.verify_refresh_token(refresh_token)

    assert user.username == test_user.username


@pytest.mark.asyncio
async def test_verify_invalid_refresh_token(user_service):
    with pytest.raises(HTTPException) as exc_info:
        await user_service.verify_refresh_token("invalid_token")
    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
