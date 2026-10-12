import httpx
import pytest

from app.providers.frankfurter import ProviderError, fetch_latest


def _client(handler):
    return httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")


async def test_fetch_latest_maps_payload():
    def handler(request):
        return httpx.Response(
            200, json={"base": "EUR", "date": "2026-06-18", "rates": {"GBP": 0.8}}
        )

    snap = await fetch_latest("EUR", client=_client(handler))
    assert snap.base == "EUR"
    assert snap.rates["GBP"] == 0.8
    assert snap.rates["EUR"] == 1.0
    assert snap.fetched_at.utcoffset() is not None  # timezone-aware


async def test_fetch_latest_http_error_raises_provider_error():
    def handler(request):
        return httpx.Response(500)

    with pytest.raises(ProviderError):
        await fetch_latest("EUR", client=_client(handler))


async def test_fetch_latest_parse_error_raises_provider_error():
    def handler(request):
        return httpx.Response(200, json={"base": "EUR"})  # missing "rates" key

    with pytest.raises(ProviderError):
        await fetch_latest("EUR", client=_client(handler))
