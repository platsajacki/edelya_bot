from os import getenv

from dotenv import load_dotenv

load_dotenv()

DEBUG = getenv('DEBUG', '') == '1'
DEBUG_LOGGER_LEVEL = getenv('DEBUG_LOGGER_LEVEL', 'DEBUG')

BOT_TOKEN = getenv('BOT_TOKEN', '')
REDIS_URL = getenv('REDIS_URL', 'redis://localhost:6379/0')
REDIS_FSM_KEY_PREFIX = getenv('REDIS_FSM_KEY_PREFIX', 'edelya_bot:fsm')
MINI_APP_URL = getenv('MINI_APP_URL', '')
SUPPORT_EMAIL = getenv('SUPPORT_EMAIL', 'edelya@corpdi.com')
PROXY_URL = getenv('PROXY_URL', None)

LOG_DIR = getenv('LOG_DIR', './logs')
LOKI_CONTAINER = getenv('LOKI_CONTAINER', 'loki.loki.svc.cluster.local:3100')
