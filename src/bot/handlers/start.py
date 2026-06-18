from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.buttons import START_KEYBOARD
from bot.creation import router
from bot.messages import START_MESSAGE


@router.message(CommandStart())
async def start_command_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(START_MESSAGE, reply_markup=START_KEYBOARD)
