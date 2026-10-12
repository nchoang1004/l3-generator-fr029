from fastapi import APIRouter, Query

from app.cache import get_snapshot
from app.config import settings
from app.errors import error_response
from app.services.fx import UnknownCurrency, convert_minor, cross_rate, rates_for

router = APIRouter(tags=["fx"])


@router.get("/rates")
def get_rates(
    base: str = Query(default=None),
    symbols: str = Query(default=None),
):
    base = (base or settings.base_currency).upper()
    snap = get_snapshot(settings.base_currency)
    if snap is None:
        return error_response(503, "RATES_UNAVAILABLE", "no rates cached yet")
    symbol_list = symbols.split(",") if symbols else None
    try:
        rates = rates_for(snap, base, symbol_list)
    except UnknownCurrency as e:
        return error_response(422, "UNKNOWN_CURRENCY", f"unknown currency: {e}")
    return {
        "base": base,
        "date": snap.date,
        "rates": rates,
        "rates_age_seconds": snap.age_seconds(),
    }


@router.get("/convert")
def convert(
    from_: str = Query(alias="from"),
    to: str = Query(),
    amount_minor: int = Query(ge=1),
):
    snap = get_snapshot(settings.base_currency)
    if snap is None:
        return error_response(503, "RATES_UNAVAILABLE", "no rates cached yet")
    try:
        rate = cross_rate(snap, from_, to)
        converted = convert_minor(snap, from_, to, amount_minor)
    except UnknownCurrency as e:
        return error_response(422, "UNKNOWN_CURRENCY", f"unknown currency: {e}")
    return {
        "from": from_.upper(),
        "to": to.upper(),
        "amount_minor": amount_minor,
        "converted_minor": converted,
        "rate": rate,
        "rates_age_seconds": snap.age_seconds(),
    }
