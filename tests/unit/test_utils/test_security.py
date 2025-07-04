from app.core.security import verify_password, get_password_hash
from tests.fixtures.users import USER_DEFAULT_PASSWORD


def test_verify_password_correct():
    hashed = get_password_hash(USER_DEFAULT_PASSWORD)
    assert verify_password(USER_DEFAULT_PASSWORD, hashed)


def test_verify_password_incorrect():
    hashed = get_password_hash(USER_DEFAULT_PASSWORD)
    assert not verify_password("wrong_password", hashed)


def test_get_password_hash():
    hashed = get_password_hash(USER_DEFAULT_PASSWORD)
    assert isinstance(hashed, str)
    assert len(hashed) > 0
    assert hashed != USER_DEFAULT_PASSWORD
