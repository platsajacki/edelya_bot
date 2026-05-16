from asyncio import run
from logging import config as logging_config

from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.buttons import mini_app_keyboard
from bot.creation import bot, dp, router
from settings.logging_handlers import LOGGING, main_logger

FIRST_MESSAGE = r"""*Еделя — планирование питания в Telegram*

Еделя помогает заранее понять, что готовить и что купить\.

В приложении можно:
• составлять меню на неделю
• сохранять рецепты и блюда
• автоматически собирать список покупок
• отмечать купленные продукты в магазине

Как начать:
1\. Откройте приложение
2\. Добавьте блюда или рецепты
3\. Распределите их по дням недели
4\. Сформируйте список покупок
5\. Отмечайте продукты, которые уже купили
"""


@router.message(CommandStart())
async def start_command_handler(message: Message) -> None:
    await message.answer(FIRST_MESSAGE, reply_markup=mini_app_keyboard, parse_mode=ParseMode.MARKDOWN_V2)


if __name__ == '__main__':
    logging_config.dictConfig(LOGGING)
    main_logger.info('Logging is configured.')
    dp.include_router(router)
    run(dp.start_polling(bot))
