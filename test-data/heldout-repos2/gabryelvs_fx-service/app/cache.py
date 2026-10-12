import redis

from app.config import settings
from app.snapshot import RateSnapshot

redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)


def _key(base: str) -> str:
    return f"fx:snapshot:{base.upper()}"


def set_snapshot(snapshot: RateSnapshot) -> None:
    redis_client.set(_key(snapshot.base), snapshot.model_dump_json())


def get_snapshot(base: str) -> RateSnapshot | None:
    raw = redis_client.get(_key(base))
    if raw is None:
        return None
    return RateSnapshot.model_validate_json(raw)
