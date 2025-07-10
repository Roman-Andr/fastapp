import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def test_app(override_get_db):
    from fastapp.main import app
    from fastapp.core.database import get_db

    app.dependency_overrides[get_db] = override_get_db
    yield app
    app.dependency_overrides.clear()


@pytest.fixture
def client(test_app):
    with TestClient(test_app) as client:
        yield client
