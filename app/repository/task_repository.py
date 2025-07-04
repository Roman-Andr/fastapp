from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from app.models.task import TaskModel
from app.schemas.task_schema import TaskCreate, TaskUpdate


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[TaskModel]:
        result = await self.db.execute(select(TaskModel).offset(skip).limit(limit))
        return result.scalars().all()

    async def get(self, task_id: int) -> Optional[TaskModel]:
        result = await self.db.execute(select(TaskModel).where(TaskModel.id == task_id))
        return result.scalar_one_or_none()

    async def create(self, task: TaskCreate) -> TaskModel:
        db_task = TaskModel(**task.model_dump())
        self.db.add(db_task)
        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task

    async def update(self, task_id: int, task: TaskUpdate) -> Optional[TaskModel]:
        stmt = (
            update(TaskModel)
            .where(TaskModel.id == task_id)
            .values(**task.model_dump(exclude_unset=True)))
        await self.db.execute(stmt)
        await self.db.commit()
        return await self.get(task_id)

    async def delete(self, task_id: int) -> None:
        stmt = delete(TaskModel).where(TaskModel.id == task_id)
        await self.db.execute(stmt)
        await self.db.commit()