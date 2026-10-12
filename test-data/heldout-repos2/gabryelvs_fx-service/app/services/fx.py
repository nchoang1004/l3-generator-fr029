from decimal import ROUND_HALF_UP, Decimal

from app.snapshot import RateSnapshot


class UnknownCurrency(Exception):
    pass


def _rate(snapshot: RateSnapshot, code: str) -> float:
    code = code.upper()
    if code not in snapshot.rates:
        raise UnknownCurrency(code)
    return snapshot.rates[code]


def cross_rate(snapshot: RateSnapshot, frm: str, to: str) -> float:
    return _rate(snapshot, to) / _rate(snapshot, frm)


def convert_minor(snapshot: RateSnapshot, frm: str, to: str, amount_minor: int) -> int:
    # Validate currencies via cross_rate (raises UnknownCurrency if invalid)
    cross_rate(snapshot, frm, to)
    # Compute rate with Decimal precision to avoid float errors
    to_rate = Decimal(str(snapshot.rates[to.upper()]))
    frm_rate = Decimal(str(snapshot.rates[frm.upper()]))
    rate_decimal = to_rate / frm_rate
    converted = (Decimal(amount_minor) * rate_decimal).quantize(
        Decimal("1"), rounding=ROUND_HALF_UP
    )
    return int(converted)


def rates_for(snapshot: RateSnapshot, base: str, symbols: list[str] | None) -> dict[str, float]:
    base = base.upper()
    _rate(snapshot, base)  # validate base; raises UnknownCurrency if unknown
    if base != snapshot.base:
        # Re-express all rates relative to the requested base.
        base_rate = _rate(snapshot, base)
        all_rates = {k: v / base_rate for k, v in snapshot.rates.items()}
    else:
        all_rates = dict(snapshot.rates)
    if symbols:
        wanted = {s.upper() for s in symbols}
        missing = wanted - all_rates.keys()
        if missing:
            raise UnknownCurrency(sorted(missing)[0])
        return {k: v for k, v in all_rates.items() if k in wanted}
    return all_rates
