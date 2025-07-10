from pydantic import BaseModel, EmailStr

from fastapp.schemas.role_schema import UserRole


class UserBase(BaseModel):
    username: str
    email: EmailStr | None = None
    role: UserRole = UserRole.USER


class UserCreate(UserBase):
    password: str


class UserOutput(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
