from typing import List, Annotated

from fastapi import APIRouter, Depends, status

from app.core.auth import get_current_active_user
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskOutput
from app.schemas.user_schema import UserOutput
from app.services.task_service import TaskServiceDep

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/")
async def read_tasks(
    service: TaskServiceDep,
    _: Annotated[UserOutput, Depends(get_current_active_user)],
    skip: int = 0,
    limit: int = 100
) -> List[TaskOutput]:
    return await service.get_all_tasks(skip, limit)


@router.get("/{task_id}")
async def read_task(
    task_id: int,
    service: TaskServiceDep,
    _: Annotated[UserOutput, Depends(get_current_active_user)]
) -> TaskOutput:
    return await service.get_task_by_id(task_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    service: TaskServiceDep,
    _: Annotated[UserOutput, Depends(get_current_active_user)]
) -> TaskOutput:
    return await service.create_task(task)


@router.patch("/{task_id}")
async def update_task(
    task_id: int,
    task: TaskUpdate,
    service: TaskServiceDep,
    _: Annotated[UserOutput, Depends(get_current_active_user)]
) -> TaskOutput:
    return await service.update_task(task_id, task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    service: TaskServiceDep,
    _: Annotated[UserOutput, Depends(get_current_active_user)]
):
    await service.delete_task(task_id)
