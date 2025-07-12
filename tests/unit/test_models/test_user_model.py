import pytest
from sqlalchemy import inspect
from fastapp.core.security import verify_password

from fastapp.models.user import UserModel
from tests.fixtures.users import USER_DEFAULT_USERNAME, USER_DEFAULT_EMAIL, USER_DEFAULT_PASSWORD


@pytest.mark.asyncio
async def test_user_model_creation(user_data):
    user = UserModel(**user_data(hash_password=True))

    assert user.username == USER_DEFAULT_USERNAME
    assert user.email == USER_DEFAULT_EMAIL
    assert verify_password(USER_DEFAULT_PASSWORD, user.hashed_password)
    assert user.is_active is True
    assert user.role == "USER"


@pytest.mark.asyncio
async def test_user_model_with_custom_values(user_data):
    custom_data = user_data(
        username="custom",
        email="custom@test.com",
        password="CustomPass123!",
        hash_password=True,
        is_active=False,
        role="ADMIN"
    )
    user = UserModel(**custom_data)

    assert user.username == "custom"
    assert user.email == "custom@test.com"
    assert verify_password("CustomPass123!", user.hashed_password)
    assert user.is_active is False
    assert user.role == "ADMIN"


@pytest.mark.asyncio
async def test_user_model_columns():
    inspector = inspect(UserModel)
    columns = [c.name for c in inspector.columns]

    assert "id" in columns
    assert "username" in columns
    assert "email" in columns
    assert "hashed_password" in columns
    assert "is_active" in columns
    assert "role" in columns


@pytest.mark.asyncio
async def test_user_model_relationships():
    inspector = inspect(UserModel)
    relationships = [r.key for r in inspector.relationships]

    assert "tasks" in relationships


@pytest.mark.asyncio
async def test_user_model_role_enum():
    user = UserModel(
        username="test",
        email="test@example.com",
        hashed_password="hashed",
        role="MODERATOR"
    )

    assert user.role == "MODERATOR"


