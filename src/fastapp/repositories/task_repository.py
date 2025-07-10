from typing import List

from sqlalchemy import select, update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession

from fastapp.models.task import TaskModel
from fastapp.schemas.task_schema import TaskCreate, TaskUpdate


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, user_id: int, skip: int = 0, limit: int = 100) -> List[TaskModel]:
        result = await self.db.execute(
            select(TaskModel)
            .where(TaskModel.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get(self, user_id: int, task_id: int) -> TaskModel | None:
        result = await self.db.execute(
            select(TaskModel)
            .where(and_(TaskModel.id == task_id, TaskModel.user_id == user_id))
        )
        return result.scalar_one_or_none()

    async def create(self, user_id: int, task: TaskCreate) -> TaskModel:
        db_task = TaskModel(**task.model_dump(), user_id=user_id)
        self.db.add(db_task)
        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task

    async def update(self, user_id: int, task_id: int, task: TaskUpdate) -> TaskModel | None:
        await self.db.execute(
            update(TaskModel)
            .where(and_(TaskModel.id == task_id, TaskModel.user_id == user_id))
            .values(**task.model_dump(exclude_unset=True))
        )
        await self.db.commit()
        return await self.get(user_id, task_id)

    async def delete(self, user_id: int, task_id: int) -> None:
        await self.db.execute(
            delete(TaskModel)
            .where(and_(TaskModel.id == task_id, TaskModel.user_id == user_id))
        )
        await self.db.commit()
