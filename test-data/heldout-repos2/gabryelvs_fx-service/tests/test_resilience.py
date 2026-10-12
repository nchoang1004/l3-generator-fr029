import asyncio
from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.cache import get_snapshot, set_snapshot
from app.main import app
from app.providers.frankfurter import ProviderError
from app.refresh import refresh_once
from app.snapshot import RateSnapshot

client = TestClient(app)


async def _bad_fetcher(base=None, client=None):
    raise ProviderError("upstream down")


def test_serves_cached_rates_when_upstream_down():
    # Given a cached snapshot...
    set_snapshot(RateSnapshot(
        base="EUR", date="2026-06-18",
        rates={"EUR": 1.0, "GBP": 0.80, "USD": 1.20},
        fetched_at=datetime.now(UTC),
    ))
    # When a refresh fails (upstream down)...
    ok = asyncio.run(refresh_once(fetcher=_bad_fetcher))
    assert ok is False
    # Then the cache is intact and the API still serves rates.
    assert get_snapshot("EUR") is not None
    assert get_snapshot("EUR").rates == {"EUR": 1.0, "GBP": 0.80, "USD": 1.20}
    r = client.get("/convert", params={"from": "GBP", "to": "USD", "amount_minor": 10000})
    assert r.status_code == 200
    assert r.json()["converted_minor"] == 15000
