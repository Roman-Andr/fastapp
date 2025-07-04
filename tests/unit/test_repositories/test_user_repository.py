# tests/unit/test_repositories/test_user_repository.py

import pytest

from tests.fixtures.users import USER_DEFAULT_USERNAME, USER_DEFAULT_EMAIL


@pytest.mark.asyncio
async def test_create_user(user_repository, user_create):
    user = await user_repository.create_user(user_create())

    assert user.id is not None
    assert user.username == USER_DEFAULT_USERNAME
    assert user.email == USER_DEFAULT_EMAIL
    assert user.is_active is True


@pytest.mark.asyncio
async def test_get_user_by_username(user_repository, user_create):
    created_user = await user_repository.create_user(user_create())
    fetched_user = await user_repository.get_user_by_username(created_user.username)

    assert fetched_user is not None
    assert fetched_user.id == created_user.id
    assert fetched_user.username == USER_DEFAULT_USERNAME


@pytest.mark.asyncio
async def test_get_user_by_email(user_repository, user_create):
    created_user = await user_repository.create_user(user_create())
    fetched_user = await user_repository.get_user_by_email(created_user.email)

    assert fetched_user is not None
    assert fetched_user.id == created_user.id
    assert fetched_user.email == USER_DEFAULT_EMAIL


@pytest.mark.asyncio
async def test_create_user_duplicate_username(user_repository, user_create):
    await user_repository.create_user(user_create())
    with pytest.raises(Exception):
        await user_repository.create_user(user_create())
