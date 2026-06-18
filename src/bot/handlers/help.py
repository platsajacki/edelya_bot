from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.buttons import (
    HELP_BACK_CALLBACK,
    HELP_CALLBACK_PREFIX,
    HELP_START_CALLBACK,
    get_help_keyboard,
    get_help_topic_keyboard,
)
from bot.creation import router
from bot.messages import HELP_MESSAGE
from bot.services.onboarding import get_help_topic


@router.callback_query(F.data.startswith(f'{HELP_CALLBACK_PREFIX}:'))
async def help_callback_handler(callback: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(callback.message, Message):
        await callback.answer()
        return
    await state.clear()
    if callback.data == HELP_START_CALLBACK:
        await callback.message.answer(HELP_MESSAGE, reply_markup=get_help_keyboard())
        await callback.answer()
        return
    if callback.data == HELP_BACK_CALLBACK:
        await callback.message.edit_text(HELP_MESSAGE, reply_markup=get_help_keyboard())
        await callback.answer()
        return
    topic = get_help_topic(callback.data)
    if topic is None:
        await callback.answer()
        return
    await callback.message.edit_text(topic.text, reply_markup=get_help_topic_keyboard())
    await callback.answer()
