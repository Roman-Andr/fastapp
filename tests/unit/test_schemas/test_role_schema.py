import pytest

from fastapp.schemas.role_schema import UserRole


@pytest.mark.parametrize("role,value", [
    (UserRole.USER, "USER"),
    (UserRole.MODERATOR, "MODERATOR"),
    (UserRole.ADMIN, "ADMIN"),
])
def test_user_role_values(role, value):
    assert role.value == value

