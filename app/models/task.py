from sqlalchemy import Integer, Column, String, Boolean

from app.core.database import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, default="")
    is_done = Column(Boolean, default=False)
