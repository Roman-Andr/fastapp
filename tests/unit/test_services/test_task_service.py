import pytest
from fastapi import HTTPException, status

from tests.fixtures.tasks import TASK_DEFAULT_TITLE, TASK_DEFAULT_DESCRIPTION, task_update
from tests.fixtures.users import test_user


@pytest.mark.asyncio
async def test_get_all_tasks(task_service, task_create, test_user):
    await task_service.create_task(test_user.id, task_create(title="Task 1"))
    await task_service.create_task(test_user.id, task_create(title="Task 2"))

    tasks = await task_service.get_all_tasks(test_user.id)
    assert len(tasks) == 2
    assert all(task.user_id == test_user.id for task in tasks)


@pytest.mark.asyncio
async def test_get_task_by_id(task_service, task_create, test_user):
    created_task = await task_service.create_task(test_user.id, task_create())
    fetched_task = await task_service.get_task_by_id(test_user.id, created_task.id)

    assert fetched_task.id == created_task.id
    assert fetched_task.title == TASK_DEFAULT_TITLE
    assert fetched_task.user_id == test_user.id


@pytest.mark.asyncio
async def test_get_nonexistent_task(task_service, test_user):
    with pytest.raises(HTTPException) as exc_info:
        await task_service.get_task_by_id(test_user.id, 999)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_task(task_service, task_create, test_user):
    task = await task_service.create_task(test_user.id, task_create())

    assert task.id is not None
    assert task.title == TASK_DEFAULT_TITLE
    assert task.description == TASK_DEFAULT_DESCRIPTION
    assert task.user_id == test_user.id


@pytest.mark.asyncio
async def test_update_task(task_service, task_create, task_update, test_user):
    created_task = await task_service.create_task(test_user.id, task_create())
    updated_task = await task_service.update_task(
        test_user.id,
        created_task.id,
        task_update(title="Updated", description="New desc", is_done=True)
    )

    assert updated_task.title == "Updated"
    assert updated_task.description == "New desc"
    assert updated_task.is_done is True
    assert updated_task.user_id == test_user.id


@pytest.mark.asyncio
async def test_delete_task(task_service, task_create, test_user):
    created_task = await task_service.create_task(test_user.id, task_create())
    await task_service.delete_task(test_user.id, created_task.id)

    with pytest.raises(HTTPException) as exc_info:
        await task_service.get_task_by_id(test_user.id, created_task.id)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
