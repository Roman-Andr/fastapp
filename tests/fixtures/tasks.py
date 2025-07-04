import pytest

from app.schemas.task_schema import TaskCreate, TaskUpdate

TASK_DEFAULT_TITLE = "Test Task"
TASK_DEFAULT_DESCRIPTION = "Test Description"
TASK_DEFAULT_IS_DONE = False


@pytest.fixture
def task_data():
    def _factory(
        title: str = TASK_DEFAULT_TITLE,
        description: str | None = TASK_DEFAULT_DESCRIPTION,
        is_done: bool = TASK_DEFAULT_IS_DONE,
        **overrides
    ) -> dict:
        data = {
            "title": title,
            "description": description,
            "is_done": is_done,
            **overrides
        }
        return {k: v for k, v in data.items() if v is not None}

    return _factory


@pytest.fixture
def task_create(task_data):
    def _factory(**kwargs) -> TaskCreate:
        data = task_data(**kwargs)
        return TaskCreate(**data)

    return _factory


@pytest.fixture
def task_update(task_data):
    def _factory(**kwargs) -> TaskUpdate:
        default_kwargs = {
            "title": None,
            "description": None,
            "is_done": None,
        }
        combined_kwargs = {**default_kwargs, **kwargs}
        data = task_data(**combined_kwargs)
        return TaskUpdate(**data)

    return _factory
