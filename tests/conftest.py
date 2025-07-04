import os

from app.models.task import TaskModel  # noqa
from app.models.user import UserModel  # noqa

os.environ["TESTING"] = "1"

pytest_plugins = [
    "tests.fixtures.app",
    "tests.fixtures.database",
    "tests.fixtures.repositories",
    "tests.fixtures.tasks",
    "tests.fixtures.users"
]
