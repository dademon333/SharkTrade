import random
from string import ascii_lowercase, digits

from aioredis import Redis


class CRUDUserTokens:
    @staticmethod
    async def get_user_id_by_token(access_token: str, redis_cursor: Redis) -> int | None:
        """Returns user id by access token."""
        user_id = await redis_cursor.get(f'user_token:{access_token}')
        if user_id is None:
            return None
        return int(user_id)

    @staticmethod
    async def create(user_id: int, redis_cursor: Redis) -> str:
        """Creates access token, saves in db and returns it."""
        access_token = ''.join(random.choices(ascii_lowercase + digits, k=32))
        await redis_cursor.set(f'user_token:{access_token}', user_id, ex=3600 * 24 * 30)  # 30 days lifetime
        return access_token

    @staticmethod
    async def delete(access_token: str, redis_cursor: Redis) -> None:
        """Deletes access token."""
        await redis_cursor.delete(f'user_token:{access_token}')
