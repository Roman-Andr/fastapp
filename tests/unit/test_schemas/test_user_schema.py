import pytest

from fastapp.schemas.user_schema import UserCreate


@pytest.mark.parametrize("password, is_valid", [
    ("Short1!", False),
    ("nouppercase1!", False),
    ("NoNumbers!", False),
    ("ValidPass123!", True),
])
def test_password_validation(password, is_valid):
    if is_valid:
        UserCreate(username="test", email="test@example.com", password=password)
    else:
        with pytest.raises(ValueError):
            UserCreate(username="test", email="test@example.com", password=password)
