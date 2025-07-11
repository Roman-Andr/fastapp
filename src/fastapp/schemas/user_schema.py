from pydantic import BaseModel, EmailStr, field_validator

from fastapp.config import settings
from fastapp.schemas.role_schema import UserRole


class UserBase(BaseModel):
    username: str
    email: EmailStr | None = None
    role: UserRole = UserRole.USER


class UserCreate(UserBase):
    password: str

    @field_validator('username')
    @classmethod
    def validate_username(cls, username: str) -> str:
        if username.lower() in settings.forbidden_usernames:
            raise ValueError("This username is not allowed")
        return username

    @field_validator('password')
    @classmethod
    def validate_password_complexity(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")

        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(not c.isalnum() for c in v):
            raise ValueError("Password must contain at least one special character")

        return v


class UserOutput(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "id": 1,
                    "username": "johndoe",
                    "email": "john@example.com",
                    "role": "USER",
                    "is_active": True
                },
                {
                    "id": 1,
                    "username": "admin",
                    "email": "admin@example.com",
                    "role": "ADMIN",
                    "is_active": True
                }
            ]
        }
