from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.redis import RedisStorage

from redis.asyncio import Redis as AsyncRedis

from settings.conf import BOT_TOKEN, DEBUG, REDIS_URL

bot = Bot(token=BOT_TOKEN)
router = Router(name='main_router')
storage: RedisStorage | None = None
if not DEBUG:
    redis_client = AsyncRedis.from_url(REDIS_URL)
    storage = RedisStorage(redis=redis_client)

dp = Dispatcher(storage=storage)
