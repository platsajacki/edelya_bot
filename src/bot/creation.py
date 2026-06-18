from aiogram import Bot, Dispatcher, Router
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage

from redis.asyncio import Redis as AsyncRedis

from settings.conf import BOT_TOKEN, DEBUG, PROXY_URL, REDIS_FSM_KEY_PREFIX, REDIS_URL

session = AiohttpSession(proxy=PROXY_URL) if PROXY_URL else AiohttpSession()
bot = Bot(token=BOT_TOKEN, session=session)
router = Router(name='main_router')
storage: RedisStorage | None = None
if not DEBUG:
    redis_client = AsyncRedis.from_url(REDIS_URL)
    storage = RedisStorage(redis=redis_client, key_builder=DefaultKeyBuilder(prefix=REDIS_FSM_KEY_PREFIX))

dp = Dispatcher(storage=storage)
