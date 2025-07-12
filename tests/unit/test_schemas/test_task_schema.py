import pytest
from pydantic import ValidationError

from fastapp.schemas.task_schema import TaskBase, TaskCreate, TaskUpdate, TaskOutput


def test_task_base_schema():
    task = TaskBase(description="Test Description")

    assert task.description == "Test Description"


def test_task_create_schema():
    task = TaskCreate(title="Test Task", description="Test Description")

    assert task.title == "Test Task"
    assert task.description == "Test Description"


@pytest.mark.parametrize("title", ["", None])
def test_task_create_invalid_title(title):
    with pytest.raises(ValidationError):
        TaskCreate(title=title)


def test_task_update_schema():
    task = TaskUpdate(title="Updated Task", description="Updated Desc", is_done=True)

    assert task.title == "Updated Task"
    assert task.description == "Updated Desc"
    assert task.is_done is True


def test_task_update_partial():
    task = TaskUpdate(is_done=True)

    assert task.is_done is True
    assert task.title is None
    assert task.description is None


def test_task_output_schema():
    task_data = {
        "id": 1,
        "title": "Test Task",
        "description": "Test Description",
        "is_done": False,
        "user_id": 1
    }
    task = TaskOutput(**task_data)

    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.is_done is False
    assert task.user_id == 1


def test_task_output_from_attributes():
    class MockTask:
        id = 1
        title = "Test"
        description = "Desc"
        is_done = False
        user_id = 1

    task = TaskOutput.model_validate(MockTask())

    assert task.id == 1
    assert task.title == "Test"
