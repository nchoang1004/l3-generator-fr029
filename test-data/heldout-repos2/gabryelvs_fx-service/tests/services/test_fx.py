from datetime import UTC, datetime

import pytest

from app.services.fx import UnknownCurrency, convert_minor, cross_rate, rates_for
from app.snapshot import RateSnapshot

SNAP = RateSnapshot(
    base="EUR",
    date="2026-06-18",
    rates={"EUR": 1.0, "GBP": 0.80, "USD": 1.20},
    fetched_at=datetime.now(UTC),
)


def test_cross_rate_via_base():
    # 1 GBP -> USD = rates[USD]/rates[GBP] = 1.20/0.80 = 1.5
    assert cross_rate(SNAP, "GBP", "USD") == pytest.approx(1.5)


def test_cross_rate_same_currency_is_one():
    assert cross_rate(SNAP, "USD", "USD") == pytest.approx(1.0)


def test_convert_minor_half_up_rounding():
    # 10000 pence GBP -> USD at 1.5 = 15000
    assert convert_minor(SNAP, "GBP", "USD", 10000) == 15000


def test_convert_minor_rounds_half_up():
    # contrived: 1 unit * 1.5 = 1.5 -> 2
    assert convert_minor(SNAP, "GBP", "USD", 1) == 2


def test_unknown_currency_raises():
    with pytest.raises(UnknownCurrency):
        cross_rate(SNAP, "GBP", "JPY")


def test_rates_for_filters_symbols():
    assert rates_for(SNAP, "EUR", ["GBP"]) == {"GBP": 0.80}


def test_convert_minor_unknown_currency_raises():
    with pytest.raises(UnknownCurrency):
        convert_minor(SNAP, "GBP", "JPY", 100)


def test_rates_for_unknown_base_raises():
    with pytest.raises(UnknownCurrency):
        rates_for(SNAP, "JPY", None)


def test_rates_for_non_default_base_rebases():
    # base=GBP: USD per GBP = 1.20/0.80 = 1.5; EUR per GBP = 1.0/0.80 = 1.25; GBP per GBP = 1.0
    out = rates_for(SNAP, "GBP", None)
    assert out["USD"] == pytest.approx(1.5)
    assert out["EUR"] == pytest.approx(1.25)
    assert out["GBP"] == pytest.approx(1.0)


def test_rates_for_non_default_base_with_symbols():
    out = rates_for(SNAP, "GBP", ["USD"])
    assert out["USD"] == pytest.approx(1.5)
