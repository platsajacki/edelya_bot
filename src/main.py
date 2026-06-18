from asyncio import run
from logging import config as logging_config

from bot.commands import BOT_COMMANDS
from bot.creation import bot, dp, router
from bot.handlers import register_handlers
from settings.logging_handlers import LOGGING, main_logger


async def main() -> None:
    await bot.set_my_commands(BOT_COMMANDS)
    register_handlers()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging_config.dictConfig(LOGGING)
    main_logger.info('Logging is configured.')
    run(main())
