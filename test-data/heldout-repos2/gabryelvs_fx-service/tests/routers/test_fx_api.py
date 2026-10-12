from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.cache import set_snapshot
from app.main import app
from app.snapshot import RateSnapshot

client = TestClient(app)


def _seed():
    set_snapshot(RateSnapshot(
        base="EUR", date="2026-06-18",
        rates={"EUR": 1.0, "GBP": 0.80, "USD": 1.20},
        fetched_at=datetime.now(UTC),
    ))


def test_rates_returns_filtered_symbols():
    _seed()
    r = client.get("/rates", params={"base": "EUR", "symbols": "GBP,USD"})
    assert r.status_code == 200
    body = r.json()
    assert body["rates"] == {"GBP": 0.80, "USD": 1.20}
    assert "rates_age_seconds" in body
    assert body["base"] == "EUR"
    assert "date" in body


def test_convert_minor_half_up():
    _seed()
    r = client.get("/convert", params={"from": "GBP", "to": "USD", "amount_minor": 10000})
    assert r.status_code == 200
    body = r.json()
    assert body["converted_minor"] == 15000
    assert abs(body["rate"] - 1.5) < 0.0001


def test_convert_unknown_currency_422():
    _seed()
    r = client.get("/convert", params={"from": "GBP", "to": "JPY", "amount_minor": 100})
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "UNKNOWN_CURRENCY"


def test_rates_503_when_cache_empty():
    r = client.get("/rates", params={"base": "EUR"})
    assert r.status_code == 503
    assert r.json()["error"]["code"] == "RATES_UNAVAILABLE"


def test_convert_503_when_cache_empty():
    r = client.get("/convert", params={"from": "GBP", "to": "USD", "amount_minor": 100})
    assert r.status_code == 503
    assert r.json()["error"]["code"] == "RATES_UNAVAILABLE"


def test_convert_invalid_amount_uses_error_envelope():
    _seed()
    r = client.get("/convert", params={"from": "GBP", "to": "USD", "amount_minor": 0})
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "VALIDATION_ERROR"
