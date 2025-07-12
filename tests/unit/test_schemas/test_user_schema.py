import pytest
from pydantic import ValidationError
from pydantic_core import PydanticCustomError

from fastapp.schemas.user_schema import UserBase, UserCreate, UserOutput


def test_user_base_schema():
    user = UserBase(
        username="testuser",
        email="test@example.com",
        role="USER"
    )

    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.role == "USER"


@pytest.mark.parametrize("username", ["", None])
def test_user_base_invalid_username(username):
    with pytest.raises(ValidationError):
        UserBase(username=username, email="test@example.com")


def test_user_create_schema():
    user = UserCreate(
        username="testuser",
        email="test@example.com",
        password="ValidPass123!"
    )

    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.password == "ValidPass123!"


@pytest.mark.parametrize("password,expected_error", [
    ("short", "Password must be at least 8 characters long"),
    ("nouppercase1!", "Password must contain at least one uppercase letter"),
    ("NOLOWERCASE1!", "Password must contain at least one lowercase letter"),
    ("NoNumbers!", "Password must contain at least one digit"),
    ("Valid123", "Password must contain at least one special character"),
])
def test_user_create_password_validation(password, expected_error):
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        UserCreate(username="testuser", email="test@example.com", password=password)

    assert expected_error in str(exc_info.value)


def test_user_output_schema():
    user_data = {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "role": "USER",
        "is_active": True
    }
    user = UserOutput(**user_data)

    assert user.id == 1
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.role == "USER"
    assert user.is_active is True


def test_user_output_from_attributes():
    class MockUser:
        id = 1
        username = "testuser"
        email = "test@example.com"
        role = "USER"
        is_active = True

    user = UserOutput.model_validate(MockUser())

    assert user.id == 1
    assert user.username == "testuser"