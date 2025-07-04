from typing import List, Annotated

from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import DBSession
from app.repository.task_repository import TaskRepository
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskOutput


class TaskService:
    def __init__(self, db: AsyncSession):
        self.repository = TaskRepository(db)

    async def get_all_tasks(self, skip: int = 0, limit: int = 100) -> List[TaskOutput]:
        return await self.repository.get_all(skip, limit)

    async def get_task_by_id(self, task_id: int) -> TaskOutput:
        task = await self.repository.get(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        return task

    async def create_task(self, task_data: TaskCreate) -> TaskOutput:
        return await self.repository.create(task_data)

    async def update_task(self, task_id: int, task_data: TaskUpdate) -> TaskOutput:
        task = await self.repository.get(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        if task_data.is_done and not task_data.description:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot mark task as done without description"
            )

        return await self.repository.update(task_id, task_data)

    async def delete_task(self, task_id: int) -> None:
        task = await self.repository.get(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        await self.repository.delete(task_id)


def get_task_service(db: DBSession) -> TaskService:
    return TaskService(db)


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]
