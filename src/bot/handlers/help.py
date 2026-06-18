from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.buttons import (
    CONTACT_CALLBACK,
    HELP_BACK_CALLBACK,
    HELP_START_CALLBACK,
    get_help_keyboard,
    get_help_topic_keyboard,
)
from bot.creation import router
from bot.messages import CONTACT_MESSAGE, HELP_MESSAGE, HELP_TOPICS
from bot.services.onboarding import get_help_topic
from settings.conf import SUPPORT_EMAIL

HELP_TOPIC_CALLBACKS = {topic.callback_data for topic in HELP_TOPICS}


@router.callback_query(F.data == HELP_START_CALLBACK)
async def start_help_callback_handler(callback: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(callback.message, Message):
        await callback.answer()
        return
    await state.clear()
    await callback.message.answer(HELP_MESSAGE, reply_markup=get_help_keyboard())
    await callback.answer()


@router.callback_query(F.data == HELP_BACK_CALLBACK)
async def back_to_help_callback_handler(callback: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(callback.message, Message):
        await callback.answer()
        return
    await state.clear()
    await callback.message.edit_text(HELP_MESSAGE, reply_markup=get_help_keyboard())
    await callback.answer()


@router.callback_query(F.data == CONTACT_CALLBACK)
async def contact_callback_handler(callback: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(callback.message, Message):
        await callback.answer()
        return
    await state.clear()
    await callback.message.answer(CONTACT_MESSAGE.format(email=SUPPORT_EMAIL))
    await callback.answer()


@router.callback_query(F.data.in_(HELP_TOPIC_CALLBACKS))
async def help_topic_callback_handler(callback: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(callback.message, Message):
        await callback.answer()
        return
    await state.clear()
    topic = get_help_topic(callback.data)
    if topic is None:
        await callback.answer()
        return
    await callback.message.edit_text(topic.text, reply_markup=get_help_topic_keyboard())
    await callback.answer()
