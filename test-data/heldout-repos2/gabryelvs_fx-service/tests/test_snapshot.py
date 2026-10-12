from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from app.snapshot import RateSnapshot


def _snap(fetched_at):
    return RateSnapshot(base="EUR", date="2026-06-18", rates={"GBP": 0.84}, fetched_at=fetched_at)


def test_age_seconds_is_nonnegative_and_uses_now():
    now = datetime.now(UTC)
    snap = _snap(now - timedelta(seconds=120))
    assert snap.age_seconds(now) == 120


def test_age_seconds_defaults_to_current_time():
    snap = _snap(datetime.now(UTC))
    assert 0 <= snap.age_seconds() < 2


def test_naive_fetched_at_is_rejected():
    with pytest.raises(ValidationError):
        RateSnapshot(base="EUR", date="2026-06-18", rates={"GBP": 0.8},
                     fetched_at=datetime(2026, 6, 18, 12, 0, 0))  # naive
