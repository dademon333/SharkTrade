from aioredis import Redis


async def get_current_online(redis_cursor: Redis) -> int:
    return int(await redis_cursor.get('current_online'))


async def set_current_online(redis_cursor: Redis, new_online: int) -> None:
    await redis_cursor.set('current_online', new_online)
