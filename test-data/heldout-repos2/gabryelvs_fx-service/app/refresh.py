import asyncio
import logging

from app.cache import set_snapshot
from app.config import settings
from app.providers.frankfurter import ProviderError, fetch_latest

log = logging.getLogger("fx.refresh")


async def refresh_once(fetcher=fetch_latest) -> bool:
    try:
        snapshot = await fetcher(settings.base_currency)
    except ProviderError as e:
        log.warning("rate refresh failed, keeping previous snapshot: %s", e)
        return False
    set_snapshot(snapshot)
    return True


async def refresh_loop(
    stop_event: asyncio.Event,
    fetcher=fetch_latest,
    interval: int | None = None,
) -> None:
    interval = interval if interval is not None else settings.refresh_interval_seconds
    while not stop_event.is_set():
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=interval)
        except TimeoutError:
            pass
        if stop_event.is_set():
            break
        await refresh_once(fetcher=fetcher)
