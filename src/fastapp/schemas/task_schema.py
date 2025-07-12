from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    description: str | None = None


class TaskCreate(TaskBase):
    title: str = Field(..., min_length=1)


class TaskUpdate(TaskBase):
    title: str | None = Field(None, min_length=1)
    is_done: bool | None = None


class TaskOutput(TaskCreate):
    id: int
    is_done: bool
    user_id: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Task Title",
                "description": "Task Description",
                "is_done": False,
                "user_id": 42
            }
        }
