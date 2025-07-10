import pytest

from fastapp.models.task import TaskModel
from tests.fixtures.tasks import TASK_DEFAULT_TITLE, TASK_DEFAULT_DESCRIPTION, TASK_DEFAULT_IS_DONE


@pytest.mark.asyncio
async def test_task_model_creation(task_data):
    task = TaskModel(**task_data())

    assert task.title == TASK_DEFAULT_TITLE
    assert task.description == TASK_DEFAULT_DESCRIPTION
    assert task.is_done == TASK_DEFAULT_IS_DONE


@pytest.mark.asyncio
async def test_task_model_with_custom_values(task_data):
    custom_data = task_data(title="Custom Title", description="Custom Desc", is_done=True)
    task = TaskModel(**custom_data)

    assert task.title == "Custom Title"
    assert task.description == "Custom Desc"
    assert task.is_done is True


@pytest.mark.asyncio
async def test_task_model_optional_description(task_data):
    task = TaskModel(**task_data(description=None))

    assert task.description is None
