import redis
import json
from typing import Iterable
from config import REDIS_HOST, REDIS_PORT, REDIS_DB


# Initialize Redis client
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


def set(key: str, value: float) -> None:
    """Set the value at key `name` to `value`."""
    redis_client.set(key, value)


def get(key: str) -> str:
    """Return the value at key `name`."""
    result = json.loads(redis_client.get(key))
    return result


def keys(key: str) -> Iterable[str]:
    """Returns a list of keys matching `pattern`."""
    result = redis_client.keys(key)
    return result
