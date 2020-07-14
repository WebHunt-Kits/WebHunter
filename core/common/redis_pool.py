import redis

__REDIS_POOL = dict()


def __create_redis_pool_if_not_exists(redis_url: str):
    if redis_url not in __REDIS_POOL:
        pool = redis.ConnectionPool.from_url(redis_url)
        __REDIS_POOL[redis_url] = pool
    return __REDIS_POOL[redis_url]


def get_redis_connection(redis_url: str):
    return redis.Redis(
        connection_pool=__create_redis_pool_if_not_exists(redis_url), decode_responses=False)
