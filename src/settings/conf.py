from os import getenv

from dotenv import load_dotenv

load_dotenv()

DEBUG = getenv('DEBUG', '') == '1'
DEBUG_LOGGER_LEVEL = getenv('DEBUG_LOGGER_LEVEL', 'DEBUG')

BOT_TOKEN = getenv('BOT_TOKEN', '')
REDIS_URL = getenv('REDIS_URL', 'redis://localhost:6379/0')
MINI_APP_URL = getenv('MINI_APP_URL', 'https://edelya.corpdi.ru/')

LOG_DIR = getenv('LOG_DIR', './logs')
LOKI_CONTAINER = getenv('LOKI_CONTAINER', 'loki.loki.svc.cluster.local:3100')
