from typing import Optional, Dict, Any

from fastapi import HTTPException, status


class BaseAPIException(HTTPException):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Internal server error"
    headers: Optional[Dict[str, Any]] = None

    def __init__(self, **kwargs):
        super().__init__(
            status_code=self.status_code,
            detail=kwargs.get("detail", self.detail),
            headers=kwargs.get("headers", self.headers)
        )


class InvalidTokenException(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Invalid token"


class InactiveUserException(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Inactive user"


class InvalidCredentialsException(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    headers = {"WWW-Authenticate": "Bearer"}
    detail = "Invalid credentials"


class TokenExpiredException(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token has expired"


class PermissionDeniedException(BaseAPIException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Permission denied"


class UserNotFoundException(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User not found"


class TaskNotFoundException(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Task not found"


class AlreadyExistsException(BaseAPIException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Resource already exists"


class DatabaseConnectionException(BaseAPIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    detail = "Database connection failed"


class DatabaseOperationException(BaseAPIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Database operation failed"
