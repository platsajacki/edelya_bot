from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from bot.messages import HELP_TOPICS
from settings.conf import MINI_APP_URL, SUPPORT_EMAIL

HELP_BACK_CALLBACK = 'help:back'
HELP_CALLBACK_PREFIX = 'help'
HELP_START_CALLBACK = f'{HELP_CALLBACK_PREFIX}:start'
HOW_IT_WORKS_CALLBACK_PREFIX = 'how_it_works'
HOW_IT_WORKS_BACK_CALLBACK = f'{HOW_IT_WORKS_CALLBACK_PREFIX}:back'
HOW_IT_WORKS_NEXT_CALLBACK = f'{HOW_IT_WORKS_CALLBACK_PREFIX}:next'
HOW_IT_WORKS_START_CALLBACK = f'{HOW_IT_WORKS_CALLBACK_PREFIX}:start'
OPEN_APP_BUTTON_TEXT = 'Открыть Еделю'

MINI_APP = WebAppInfo(url=MINI_APP_URL)


def get_contact_button() -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text='Связаться с нами',
        url=f'mailto:{SUPPORT_EMAIL}',
    )


def get_how_it_works_keyboard(step_index: int, total_steps: int) -> InlineKeyboardMarkup:
    navigation_buttons = []
    if step_index > 0:
        navigation_buttons.append(
            InlineKeyboardButton(
                text='Назад',
                callback_data=HOW_IT_WORKS_BACK_CALLBACK,
            ),
        )
    if step_index < total_steps - 1:
        navigation_buttons.append(
            InlineKeyboardButton(
                text='Дальше',
                callback_data=HOW_IT_WORKS_NEXT_CALLBACK,
            ),
        )

    inline_keyboard = []
    if navigation_buttons:
        inline_keyboard.append(navigation_buttons)
    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text=OPEN_APP_BUTTON_TEXT,
                web_app=MINI_APP,
            ),
        ],
    )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def get_help_keyboard() -> InlineKeyboardMarkup:
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=topic.title,
                callback_data=topic.callback_data,
            ),
        ]
        for topic in HELP_TOPICS
    ]
    inline_keyboard.append([get_contact_button()])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def get_help_topic_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=OPEN_APP_BUTTON_TEXT,
                    web_app=MINI_APP,
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Назад к помощи',
                    callback_data=HELP_BACK_CALLBACK,
                ),
            ],
            [get_contact_button()],
        ],
    )


START_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=OPEN_APP_BUTTON_TEXT,
                web_app=MINI_APP,
            ),
        ],
        [
            InlineKeyboardButton(
                text='Как это работает',
                callback_data=HOW_IT_WORKS_START_CALLBACK,
            ),
        ],
        [
            InlineKeyboardButton(
                text='Помощь',
                callback_data=HELP_START_CALLBACK,
            ),
            get_contact_button(),
        ],
    ],
)


OPEN_APP_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=OPEN_APP_BUTTON_TEXT,
                web_app=MINI_APP,
            ),
        ],
    ],
)
