from fastapi import HTTPException, status
from fastapi.params import Depends
from sqlalchemy.sql.annotation import Annotated

from fastapp.core.auth import get_current_active_user
from fastapp.schemas.role_schema import UserRole
from fastapp.schemas.user_schema import UserOutput

UserDeps = Annotated[UserOutput, Depends(get_current_active_user)]


def get_admin(user: UserDeps):
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return user


def get_staff(user: UserDeps):
    if user.role not in [UserRole.ADMIN, UserRole.MODERATOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Moderator or admin access required"
        )
    return user


StuffDeps = Annotated[UserOutput, Depends(get_staff)]
AdminDeps = Annotated[UserOutput, Depends(get_admin)]
