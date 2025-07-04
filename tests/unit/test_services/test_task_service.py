import pytest
from fastapi import HTTPException, status

from tests.fixtures.tasks import TASK_DEFAULT_TITLE, TASK_DEFAULT_DESCRIPTION, task_update


@pytest.mark.asyncio
async def test_get_all_tasks(task_service, task_create):
    await task_service.create_task(task_create(title="Task 1"))
    await task_service.create_task(task_create(title="Task 2"))

    tasks = await task_service.get_all_tasks()
    assert len(tasks) == 2


@pytest.mark.asyncio
async def test_get_task_by_id(task_service, task_create):
    created_task = await task_service.create_task(task_create())
    fetched_task = await task_service.get_task_by_id(created_task.id)

    assert fetched_task.id == created_task.id
    assert fetched_task.title == TASK_DEFAULT_TITLE


@pytest.mark.asyncio
async def test_get_nonexistent_task(task_service):
    with pytest.raises(HTTPException) as exc_info:
        await task_service.get_task_by_id(999)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_task(task_service, task_create):
    task = await task_service.create_task(task_create())

    assert task.id is not None
    assert task.title == TASK_DEFAULT_TITLE
    assert task.description == TASK_DEFAULT_DESCRIPTION


@pytest.mark.asyncio
async def test_update_task(task_service, task_create, task_update):
    created_task = await task_service.create_task(task_create())
    updated_task = await task_service.update_task(
        created_task.id,
        task_update(title="Updated", description="New desc", is_done=True)
    )

    assert updated_task.title == "Updated"
    assert updated_task.description == "New desc"
    assert updated_task.is_done is True


@pytest.mark.asyncio
async def test_delete_task(task_service, task_create):
    created_task = await task_service.create_task(task_create())
    await task_service.delete_task(created_task.id)

    with pytest.raises(HTTPException) as exc_info:
        await task_service.get_task_by_id(created_task.id)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
