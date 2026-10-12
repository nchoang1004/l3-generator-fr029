from datetime import UTC, datetime

from app.cache import get_snapshot, set_snapshot
from app.snapshot import RateSnapshot


def test_round_trip_preserves_fetched_at():
    ts = datetime.now(UTC)
    snap = RateSnapshot(
        base="EUR",
        date="2026-06-18",
        rates={"EUR": 1.0, "GBP": 0.8},
        fetched_at=ts,
    )
    set_snapshot(snap)
    got = get_snapshot("EUR")
    assert got is not None
    assert got.rates["GBP"] == 0.8
    assert got.fetched_at == ts


def test_missing_returns_none():
    assert get_snapshot("USD") is None
