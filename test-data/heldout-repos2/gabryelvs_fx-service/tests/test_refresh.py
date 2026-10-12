import asyncio
from datetime import UTC, datetime

from app.cache import get_snapshot, set_snapshot
from app.providers.frankfurter import ProviderError
from app.refresh import refresh_loop, refresh_once
from app.snapshot import RateSnapshot


async def _ok_fetcher(base=None, client=None):
    return RateSnapshot(
        base="EUR",
        date="2026-06-18",
        rates={"EUR": 1.0, "GBP": 0.8},
        fetched_at=datetime.now(UTC),
    )


async def _bad_fetcher(base=None, client=None):
    raise ProviderError("boom")


async def test_refresh_once_success_writes_cache():
    ok = await refresh_once(fetcher=_ok_fetcher)
    assert ok is True
    assert get_snapshot("EUR").rates["GBP"] == 0.8


async def test_refresh_once_failure_keeps_old_cache():
    old = RateSnapshot(
        base="EUR",
        date="2026-06-01",
        rates={"EUR": 1.0, "GBP": 0.9},
        fetched_at=datetime.now(UTC),
    )
    set_snapshot(old)
    ok = await refresh_once(fetcher=_bad_fetcher)
    assert ok is False
    assert get_snapshot("EUR").rates["GBP"] == 0.9  # unchanged


async def test_refresh_loop_stops_immediately_when_event_preset():
    calls = []

    async def counting_fetcher(base=None, client=None):
        calls.append(1)
        return await _ok_fetcher()

    stop = asyncio.Event()
    stop.set()  # already stopped → loop must exit without fetching
    await refresh_loop(stop, fetcher=counting_fetcher, interval=100)
    assert calls == []


async def test_refresh_loop_runs_then_stops():
    calls = []

    async def counting_fetcher(base=None, client=None):
        calls.append(1)
        return await _ok_fetcher()

    stop = asyncio.Event()
    task = asyncio.create_task(refresh_loop(stop, fetcher=counting_fetcher, interval=0.01))
    await asyncio.sleep(0.05)
    stop.set()
    await task
    assert len(calls) >= 1
