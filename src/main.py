from asyncio import run
from logging import config as logging_config

from bot.creation import bot, dp, router
from bot.handlers import register_handlers
from settings.logging_handlers import LOGGING, main_logger

if __name__ == '__main__':
    logging_config.dictConfig(LOGGING)
    main_logger.info('Logging is configured.')
    register_handlers()
    dp.include_router(router)
    run(dp.start_polling(bot))
