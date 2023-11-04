import os
import time

import redis
from redis_cache import RedisCache


class APICache:
    def __init__(self, prefix="api"):
        host = os.environ.get("REDIS_URL", "localhost")
        if password := os.environ.get("REDIS_PASSWORD", None):
            client = redis.from_url(
                f"redis://default:{password}@{host}",
                encoding="utf-8",
                decode_responses=True,
            )
        else:
            client = redis.from_url(
                f"redis://{host}", encoding="utf-8", decode_responses=True
            )
        self._cache = RedisCache(redis_client=client, prefix=prefix)

    @property
    def cache(self):
        return self._cache.cache


api_cache = APICache(prefix="cache-test")


def some_expensive_operation():
    print("some_expensive_operation")
    time.sleep(4)
    return "result"


@api_cache.cache(ttl=60 * 15, limit=10_000)
def my_func():
    return some_expensive_operation()


def caching_examples():  # sourcery skip: extract-duplicate-method
    # Use the function
    print("starting slow function")
    my_func(1, 2)
    print("done")

    # Call it again with the same arguments and it will use cache
    print("retrying - should be quick")
    my_func(1, 2)
    print("done")

    # Invalidate a single value
    print("Invalidate a single value")

    my_func.invalidate(1, 2)
    print("starting slow function")
    my_func(1, 2)
    print("done")

    # Call it again with the same arguments and it will use cache
    print("retrying - should be quick")
    my_func(1, 2)
    print("done")

    print("Invalidate all values for function")
    my_func.invalidate_all()
    print("starting slow function")
    my_func(1, 2)
    print("done")

    # Call it again with the same arguments and it will use cache
    print("retrying - should be quick")
    my_func(1, 2)
    print("done")

    # CLEAR CACHE TO START OVER WITH EXAMPLES
    my_func.invalidate_all()


if __name__ == "__main__":
    caching_examples()
