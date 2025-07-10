import pytest

from fastapp.schemas.task_schema import TaskUpdate
from tests.fixtures.tasks import TASK_DEFAULT_TITLE, TASK_DEFAULT_DESCRIPTION, TASK_DEFAULT_IS_DONE


@pytest.mark.asyncio
async def test_create_task(task_repository, task_create):
    task = await task_repository.create(task_create())

    assert task.id is not None
    assert task.title == TASK_DEFAULT_TITLE
    assert task.description == TASK_DEFAULT_DESCRIPTION
    assert task.is_done is TASK_DEFAULT_IS_DONE


@pytest.mark.asyncio
async def test_get_task(task_repository, task_create):
    created_task = await task_repository.create(task_create())
    fetched_task = await task_repository.get(created_task.id)

    assert fetched_task is not None
    assert fetched_task.id == created_task.id
    assert fetched_task.title == TASK_DEFAULT_TITLE


@pytest.mark.asyncio
async def test_get_all_tasks(task_repository, task_create):
    await task_repository.create(task_create(title="Task 1"))
    await task_repository.create(task_create(title="Task 2"))

    tasks = await task_repository.get_all()
    assert len(tasks) == 2


@pytest.mark.asyncio
async def test_update_task(task_repository, task_create):
    task = await task_repository.create(task_create())
    updated = await task_repository.update(
        task.id,
        TaskUpdate(title="Updated", is_done=True)
    )

    assert updated.title == "Updated"
    assert updated.is_done is True


@pytest.mark.asyncio
async def test_delete_task(task_repository, task_create):
    task = await task_repository.create(task_create())
    await task_repository.delete(task.id)

    deleted = await task_repository.get(task.id)
    assert deleted is None
