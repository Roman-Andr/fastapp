from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr | None = None


class UserCreate(UserBase):
    password: str


class UserOutput(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
