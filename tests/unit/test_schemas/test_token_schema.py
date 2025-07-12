from fastapp.schemas.token_schema import Token, TokenWithRefresh, TokenData


def test_token_schema():
    token = Token(
        access_token="test_token",
        token_type="bearer"
    )

    assert token.access_token == "test_token"
    assert token.token_type == "bearer"


def test_token_with_refresh_schema():
    token = TokenWithRefresh(
        access_token="access_token",
        refresh_token="refresh_token",
        token_type="bearer"
    )

    assert token.access_token == "access_token"
    assert token.refresh_token == "refresh_token"
    assert token.token_type == "bearer"


def test_token_data_schema():
    token_data = TokenData(username="testuser")

    assert token_data.username == "testuser"


def test_token_data_empty():
    token_data = TokenData()

    assert token_data.username is None
