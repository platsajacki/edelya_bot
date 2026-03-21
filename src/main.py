from asyncio import run
from logging import config as logging_config

from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.buttons import mini_app_keyboard
from bot.creation import bot, dp, router
from settings.logging_handlers import LOGGING, main_logger


@router.message(CommandStart())
async def start_command_handler(message: Message) -> None:
    await message.answer(
        'Привет! Заходи в приложение!',
        reply_markup=mini_app_keyboard,
    )


if __name__ == '__main__':
    logging_config.dictConfig(LOGGING)
    main_logger.info('Logging is configured.')
    dp.include_router(router)
    run(dp.start_polling(bot))
