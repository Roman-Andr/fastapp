import pytest

from fastapp.schemas.task_schema import TaskUpdate
from tests.fixtures.tasks import TASK_DEFAULT_TITLE, TASK_DEFAULT_DESCRIPTION, TASK_DEFAULT_IS_DONE
from tests.fixtures.users import test_user


@pytest.mark.asyncio
async def test_create_task(task_repository, task_create, test_user):
    task = await task_repository.create(test_user.id, task_create())

    assert task.id is not None
    assert task.title == TASK_DEFAULT_TITLE
    assert task.description == TASK_DEFAULT_DESCRIPTION
    assert task.is_done is TASK_DEFAULT_IS_DONE
    assert task.user_id == test_user.id


@pytest.mark.asyncio
async def test_get_task(task_repository, task_create, test_user):
    created_task = await task_repository.create(test_user.id, task_create())
    fetched_task = await task_repository.get(test_user.id, created_task.id)

    assert fetched_task is not None
    assert fetched_task.id == created_task.id
    assert fetched_task.title == TASK_DEFAULT_TITLE
    assert fetched_task.user_id == test_user.id


@pytest.mark.asyncio
async def test_get_all_tasks(task_repository, task_create, test_user):
    await task_repository.create(test_user.id, task_create(title="Task 1"))
    await task_repository.create(test_user.id, task_create(title="Task 2"))

    tasks = await task_repository.get_all(test_user.id)
    assert len(tasks) == 2
    assert all(task.user_id == test_user.id for task in tasks)


@pytest.mark.asyncio
async def test_update_task(task_repository, task_create, test_user):
    task = await task_repository.create(test_user.id, task_create())
    updated = await task_repository.update(
        test_user.id,
        task.id,
        TaskUpdate(title="Updated", is_done=True)
    )

    assert updated.title == "Updated"
    assert updated.is_done is True
    assert updated.user_id == test_user.id


@pytest.mark.asyncio
async def test_delete_task(task_repository, task_create, test_user):
    task = await task_repository.create(test_user.id, task_create())
    await task_repository.delete(test_user.id, task.id)

    deleted = await task_repository.get(test_user.id, task.id)
    assert deleted is None
