import json
from typing import Optional

from apps.core.config import r


def redis_set_json(key: str, value: dict, ex: int = 600):
    """
    Store a Python dictionary in Redis as a JSON string.

    Args:
        key (str): Redis key under which the object will be stored.
        value (dict): Python dictionary to store in Redis.
        ex (int, optional): Expiration time in seconds. Default is 600 (10 minutes).
    """
    r.set(key, json.dumps(value), ex=ex)


def redis_get_json(key: str) -> Optional[dict]:
    """
    Retrieve a Python dictionary stored in Redis as JSON.

    Args:
        key (str): Redis key to fetch.

    Returns:
        dict | None: The Python dictionary if found, otherwise None.
    """
    row = r.get(key)
    if not row:
        return None
    return json.loads(row)
