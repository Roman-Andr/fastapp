import pytest


@pytest.fixture
def user_repository(async_db_session):
    from app.repository.user_repository import UserRepository
    return UserRepository(async_db_session)


@pytest.fixture
def task_repository(async_db_session):
    from app.repository.task_repository import TaskRepository
    return TaskRepository(async_db_session)


@pytest.fixture
def task_service(async_db_session):
    from app.services.task_service import TaskService
    return TaskService(async_db_session)


@pytest.fixture
def user_service(async_db_session):
    from app.services.user_service import UserService
    return UserService(async_db_session)
