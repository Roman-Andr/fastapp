import pytest
from sqlalchemy import inspect

from fastapp.models.task import TaskModel
from tests.fixtures.tasks import TASK_DEFAULT_TITLE, TASK_DEFAULT_DESCRIPTION, TASK_DEFAULT_IS_DONE


@pytest.mark.asyncio
async def test_task_model_creation(task_data):
    task = TaskModel(**task_data())

    assert task.title == TASK_DEFAULT_TITLE
    assert task.description == TASK_DEFAULT_DESCRIPTION
    assert task.is_done == TASK_DEFAULT_IS_DONE
    assert task.user_id is None


@pytest.mark.asyncio
async def test_task_model_with_custom_values(task_data):
    custom_data = task_data(
        title="Custom Title",
        description="Custom Desc",
        is_done=True,
        user_id=1
    )
    task = TaskModel(**custom_data)

    assert task.title == "Custom Title"
    assert task.description == "Custom Desc"
    assert task.is_done is True
    assert task.user_id == 1


@pytest.mark.asyncio
async def test_task_model_optional_description(task_data):
    task = TaskModel(**task_data(description=None))

    assert task.description is None


@pytest.mark.asyncio
async def test_task_model_columns():
    inspector = inspect(TaskModel)
    columns = [c.name for c in inspector.columns]

    assert "id" in columns
    assert "title" in columns
    assert "description" in columns
    assert "is_done" in columns
    assert "user_id" in columns


@pytest.mark.asyncio
async def test_task_model_relationships():
    inspector = inspect(TaskModel)
    relationships = [r.key for r in inspector.relationships]

    assert "user" in relationships
