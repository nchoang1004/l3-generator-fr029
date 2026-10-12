import pytest

from app.cache import redis_client


@pytest.fixture(autouse=True)
def _clear_redis():
    redis_client.flushdb()
    yield
    redis_client.flushdb()
