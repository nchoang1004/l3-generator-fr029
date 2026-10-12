from datetime import UTC, datetime

import httpx

from app.config import settings
from app.snapshot import RateSnapshot


class ProviderError(Exception):
    pass


async def fetch_latest(
    base: str | None = None, client: httpx.AsyncClient | None = None
) -> RateSnapshot:
    base = (base or settings.base_currency).upper()
    owns_client = client is None
    client = client or httpx.AsyncClient(base_url=settings.frankfurter_base_url, timeout=10.0)
    try:
        resp = await client.get("/latest", params={"base": base})
        resp.raise_for_status()
        data = resp.json()
        rates = {k.upper(): float(v) for k, v in data["rates"].items()}
        rates[base] = 1.0
        return RateSnapshot(
            base=base,
            date=str(data["date"]),
            rates=rates,
            fetched_at=datetime.now(UTC),
        )
    except (httpx.HTTPError, KeyError, ValueError) as e:
        raise ProviderError(str(e)) from e
    finally:
        if owns_client:
            await client.aclose()
