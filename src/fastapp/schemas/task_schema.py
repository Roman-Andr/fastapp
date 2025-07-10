from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    is_done: bool


class TaskOutput(TaskBase):
    id: int
    is_done: bool
    user_id: int

    class Config:
        from_attributes = True
