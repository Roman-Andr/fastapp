import pytest

from fastapp.core.security import get_password_hash, verify_password
from fastapp.models.user import UserModel
from tests.fixtures.users import USER_DEFAULT_USERNAME, USER_DEFAULT_EMAIL, USER_DEFAULT_PASSWORD


@pytest.mark.asyncio
async def test_user_model_creation(user_data):
    user = UserModel(**user_data(hash_password=True))

    assert user.username == USER_DEFAULT_USERNAME
    assert user.email == USER_DEFAULT_EMAIL
    assert verify_password(USER_DEFAULT_PASSWORD, user.hashed_password)
    assert user.is_active is True


@pytest.mark.asyncio
async def test_user_model_with_custom_values(user_data):
    custom_data = user_data(username="custom", email="custom@test.com",
                            hash_password=True, is_active=False)
    user = UserModel(**custom_data)
    assert user.username == "custom"
    assert user.email == "custom@test.com"
    assert verify_password(USER_DEFAULT_PASSWORD, user.hashed_password)
    assert user.is_active is False
