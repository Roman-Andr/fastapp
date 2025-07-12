from fastapp.schemas.healthcheck_schema import HealthCheck


def test_health_check_schema_default_values():
    health_check = HealthCheck()

    assert health_check.status == "ok"
    assert health_check.database == "connected"


def test_health_check_schema_with_custom_values():
    health_check = HealthCheck(status="unavailable", database="disconnected")

    assert health_check.status == "unavailable"
    assert health_check.database == "disconnected"
