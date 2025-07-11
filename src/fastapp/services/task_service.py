from typing import List, Annotated

from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fastapp.core.database import DBSession
from fastapp.core.exceptions import TaskNotFoundException
from fastapp.repositories.task_repository import TaskRepository
from fastapp.schemas.task_schema import TaskCreate, TaskUpdate, TaskOutput


class TaskService:
    def __init__(self, db: AsyncSession):
        self.repository = TaskRepository(db)

    async def get_all_tasks(self, user_id: int, skip: int = 0, limit: int = 100) -> List[TaskOutput]:
        return await self.repository.get_all(user_id, skip, limit)

    async def get_task_by_id(self, user_id: int, task_id: int) -> TaskOutput:
        task = await self.repository.get(user_id, task_id)
        if not task:
            raise TaskNotFoundException()
        return task

    async def create_task(self, user_id: int, task_data: TaskCreate) -> TaskOutput:
        return await self.repository.create(user_id, task_data)

    async def update_task(self, user_id: int, task_id: int, task_data: TaskUpdate) -> TaskOutput:
        task = await self.repository.get(user_id, task_id)
        if not task:
            raise TaskNotFoundException()

        return await self.repository.update(user_id, task_id, task_data)

    async def delete_task(self, user_id: int, task_id: int) -> None:
        task = await self.repository.get(user_id, task_id)
        if not task:
            raise TaskNotFoundException()
        await self.repository.delete(user_id, task_id)


def get_task_service(db: DBSession) -> TaskService:
    return TaskService(db)


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]
