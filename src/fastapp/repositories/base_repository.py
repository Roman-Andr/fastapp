import logging
from typing import TypeVar, Generic

from sqlalchemy.exc import SQLAlchemyError, DBAPIError

from fastapp.core.exceptions import DatabaseConnectionException, DatabaseOperationException

logger = logging.getLogger(__name__)

T = TypeVar('T')


class BaseRepository(Generic[T]):
    def __init__(self, db):
        self.db = db

    async def _handle_db_operation(self, operation, *args, **kwargs):
        try:
            return await operation(*args, **kwargs)
        except DBAPIError as e:
            logger.error(f"Database connection error: {e}")
            raise DatabaseConnectionException()
        except SQLAlchemyError as e:
            logger.error(f"Database operation error: {e}")
            raise DatabaseOperationException()
