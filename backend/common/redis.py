import aioredis
from aioredis import Redis

from tokens import Tokens


def get_redis_cursor() -> Redis:
    return aioredis.from_url(
        f'redis://{Tokens.REDIS_HOST}',
        encoding='utf-8',
        decode_responses=True
    )
