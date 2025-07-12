import pytest

from fastapp.core.security import get_password_hash
from fastapp.schemas.role_schema import UserRole
from fastapp.schemas.user_schema import UserCreate

USER_DEFAULT_USERNAME = "testuser"
USER_DEFAULT_EMAIL = "test@example.com"
USER_DEFAULT_PASSWORD = "ValidPass123!"


@pytest.fixture
def user_data():
    def _factory(
        username: str = USER_DEFAULT_USERNAME,
        email: str | None = USER_DEFAULT_EMAIL,
        password: str = USER_DEFAULT_PASSWORD,
        hash_password: bool = False,
        is_active: bool = True,
        role: str = "USER",
        **overrides
    ) -> dict:
        data = {
            "username": username,
            "email": email,
            "hashed_password" if hash_password else "password":
                get_password_hash(password) if hash_password else password,
            "is_active": is_active,
            "role": role,
            **overrides
        }
        return {k: v for k, v in data.items() if v is not None}

    return _factory


@pytest.fixture
def user_create():
    def _factory(
        username: str = USER_DEFAULT_USERNAME,
        email: str | None = USER_DEFAULT_EMAIL,
        password: str = USER_DEFAULT_PASSWORD,
        **overrides
    ) -> UserCreate:
        data = {
            "username": username,
            "email": email,
            "password": password,
            **overrides
        }
        clean_data = {k: v for k, v in data.items() if v is not None}
        return UserCreate(**clean_data)

    return _factory


@pytest.fixture
async def test_user(user_repository, user_create):
    return await user_repository.create_user(user_create())


@pytest.fixture
async def inactive_user(user_repository, user_create):
    return await user_repository.create_user(user_create(username="inactive_user", is_active=False))
