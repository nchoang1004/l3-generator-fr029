from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthz_returns_status_and_age_field():
    r = client.get("/healthz")
    assert r.status_code in (200, 503)
    assert "rates_age_seconds" in r.json()


def test_settings_defaults():
    from app.config import settings
    assert settings.base_currency == "EUR"
    assert settings.refresh_interval_seconds == 3600
