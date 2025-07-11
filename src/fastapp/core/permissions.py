from typing import Annotated

from fastapi.params import Depends

from fastapp.core.auth import ActiveUser
from fastapp.core.exceptions import PermissionDeniedException
from fastapp.schemas.role_schema import UserRole
from fastapp.schemas.user_schema import UserOutput


def get_admin(user: ActiveUser):
    if user.role != UserRole.ADMIN:
        raise PermissionDeniedException(detail="Admin access required")
    return user


def get_staff(user: ActiveUser):
    if user.role not in [UserRole.ADMIN, UserRole.MODERATOR]:
        raise PermissionDeniedException(detail="Moderator or admin access required")
    return user


StuffDeps = Annotated[UserOutput, Depends(get_staff)]
AdminDeps = Annotated[UserOutput, Depends(get_admin)]
