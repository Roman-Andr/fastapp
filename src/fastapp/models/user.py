from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship

from fastapp.core.database import Base
from fastapp.schemas.role_schema import UserRole


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True, nullable=False)
    role = Column(
        Enum(UserRole, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        default=UserRole.USER
    )
    tasks = relationship("TaskModel", back_populates="user", cascade="all, delete-orphan")
