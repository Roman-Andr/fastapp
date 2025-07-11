from typing import List

from fastapi import APIRouter, status

from fastapp.core.auth import ActiveUser
from fastapp.schemas.task_schema import TaskCreate, TaskUpdate, TaskOutput
from fastapp.services.task_service import TaskServiceDep

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/")
async def read_tasks(
    service: TaskServiceDep,
    current_user: ActiveUser,
    skip: int = 0,
    limit: int = 100
) -> List[TaskOutput]:
    return await service.get_all_tasks(current_user.id, skip, limit)


@router.get("/{task_id}")
async def read_task(
    task_id: int,
    service: TaskServiceDep,
    current_user: ActiveUser
) -> TaskOutput:
    return await service.get_task_by_id(current_user.id, task_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    service: TaskServiceDep,
    current_user: ActiveUser
) -> TaskOutput:
    return await service.create_task(current_user.id, task)


@router.patch("/{task_id}")
async def update_task(
    task_id: int,
    task: TaskUpdate,
    service: TaskServiceDep,
    current_user: ActiveUser
) -> TaskOutput:
    return await service.update_task(current_user.id, task_id, task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    service: TaskServiceDep,
    current_user: ActiveUser
):
    await service.delete_task(current_user.id, task_id)
