from logging import LogRecord, getLogger
from pathlib import Path
from typing import Any

from logging_loki import LokiQueueHandler

from settings.conf import DEBUG, DEBUG_LOGGER_LEVEL, LOKI_CONTAINER

log_dir = Path('logs')
log_dir.mkdir(parents=True, exist_ok=True)

main_logger = getLogger('main')
only_internal_logger = getLogger('only_internal_logger')


class SafeLokiQueueHandler(LokiQueueHandler):
    def emit(self, record: LogRecord) -> None:
        try:
            super().emit(record)
        except Exception as e:
            only_internal_logger.error(f'Failed to send log to Loki: {e}\nOriginal log: {self.format(record)}')


def get_logging_dict(
    log_formatter: str,
    datetime_formatter: str,
    log_dir: Path,
    loki_container: str,
    loki_app_name: str,
    color_log_formatter: str,
    debug: bool = False,
) -> dict:
    logging_dict: dict[str, Any] = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'main': {
                'format': log_formatter,
                'datefmt': datetime_formatter,
            },
            'colored': {
                '()': 'colorlog.ColoredFormatter',
                'format': color_log_formatter,
                'datefmt': datetime_formatter,
                'log_colors': {
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'red,bg_white',
                },
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'colored',
            },
            'loki': {
                'level': 'DEBUG',
                'class': 'logging_handlers.SafeLokiQueueHandler',
                'url': f'http://{loki_container}/loki/api/v1/push',
                'tags': {'application': loki_app_name},
                'version': '1',
            },
            'timed_rotating_file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': log_dir / 'main.log',
                'formatter': 'main',
                'when': 'midnight',
                'interval': 1,
                'backupCount': 7,
            },
        },
        'loggers': {
            'main': {
                'handlers': ['console', 'timed_rotating_file', 'loki'],
                'level': 'INFO',
                'propagate': False,
            },
            'aiogram': {
                'handlers': ['console', 'timed_rotating_file', 'loki'],
                'level': 'INFO',
                'propagate': False,
            },
            'only_internal_logger': {
                'handlers': ['console', 'timed_rotating_file'],
                'level': 'DEBUG',
                'propagate': False,
            },
        },
    }
    if debug:
        logging_dict['loggers']['main']['level'] = DEBUG_LOGGER_LEVEL
        logging_dict['loggers']['aiogram']['level'] = DEBUG_LOGGER_LEVEL
        logging_dict['loggers']['main']['handlers'].remove('loki')
        logging_dict['loggers']['aiogram']['handlers'].remove('loki')
    return logging_dict


LOG_FORMATTER = (
    '[%(asctime)s] [%(levelname)s] %(name)s:%(funcName)s:%(lineno)d\nFile: %(pathname)s\nMessage: %(message)s\n'
)
COLOR_LOG_FORMATTER = (
    '%(log_color)s[%(asctime)s] [%(levelname)s]%(reset)s '
    '%(cyan)s%(name)s:%(funcName)s:%(lineno)d%(reset)s\n'
    '%(blue)sFile: %(pathname)s%(reset)s\n'
    '%(purple)sMessage: %(message)s%(reset)s\n'
)
DATE_FORMATTER = '%d.%m.%Y %H:%M:%S'
LOKI_NAME_APP = 'edelya_bot' if not DEBUG else 'dev_edelya_bot'

LOGGING = get_logging_dict(
    log_formatter=LOG_FORMATTER,
    datetime_formatter=DATE_FORMATTER,
    log_dir=log_dir,
    loki_container=LOKI_CONTAINER,
    loki_app_name=LOKI_NAME_APP,
    color_log_formatter=COLOR_LOG_FORMATTER,
    debug=DEBUG,
)
