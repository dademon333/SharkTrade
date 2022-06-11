from typing import AsyncIterator

import aioredis
from aioredis import Redis

from tokens import Tokens


async def get_redis_cursor() -> AsyncIterator[Redis]:
    cursor = aioredis.from_url(
        f'redis://{Tokens.REDIS_HOST}',
        encoding='utf-8',
        decode_responses=True
    )
    try:
        yield cursor
    finally:
        await cursor.close()
