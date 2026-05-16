from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from settings.conf import MINI_APP_URL

mini_app = WebAppInfo(url=MINI_APP_URL)

mini_app_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Открыть приложение "Еделя"', web_app=mini_app)]],
)
