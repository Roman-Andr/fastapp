from pydantic import BaseModel


class HealthCheck(BaseModel):
    status: str = "ok"
    database: str = "connected"
