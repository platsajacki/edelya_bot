from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto, Message

from bot.buttons import HOW_IT_WORKS_CALLBACK_PREFIX, HOW_IT_WORKS_START_CALLBACK, get_how_it_works_keyboard
from bot.creation import router
from bot.messages import HOW_IT_WORKS_STEPS, HowItWorksStep
from bot.services.onboarding import (
    HOW_IT_WORKS_STEP_INDEX_KEY,
    get_current_how_it_works_step_index,
    get_how_it_works_step_index,
)
from bot.states import OnboardingStates


async def send_how_it_works_step(message: Message, step_index: int) -> None:
    step = HOW_IT_WORKS_STEPS[step_index]
    reply_markup = get_how_it_works_keyboard(step_index, len(HOW_IT_WORKS_STEPS))
    if step.image_path.exists():
        await message.answer_photo(photo=FSInputFile(step.image_path), caption=step.text, reply_markup=reply_markup)
        return
    await message.answer(step.text, reply_markup=reply_markup)


async def edit_how_it_works_step(message: Message, step: HowItWorksStep, step_index: int) -> None:
    reply_markup = get_how_it_works_keyboard(step_index, len(HOW_IT_WORKS_STEPS))
    if step.image_path.exists():
        media = InputMediaPhoto(media=FSInputFile(step.image_path), caption=step.text)
        await message.edit_media(media=media, reply_markup=reply_markup)
        return
    await message.edit_text(step.text, reply_markup=reply_markup)


@router.callback_query(F.data.startswith(f'{HOW_IT_WORKS_CALLBACK_PREFIX}:'))
async def how_it_works_callback_handler(callback: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(callback.message, Message):
        await callback.answer()
        return
    current_step_index = await get_current_how_it_works_step_index(state)
    step_index = get_how_it_works_step_index(callback.data, current_step_index)
    if step_index is None:
        await callback.answer()
        return
    await state.set_state(OnboardingStates.how_it_works)
    await state.update_data({HOW_IT_WORKS_STEP_INDEX_KEY: step_index})
    if callback.data == HOW_IT_WORKS_START_CALLBACK:
        await send_how_it_works_step(callback.message, step_index)
        await callback.answer()
        return
    await edit_how_it_works_step(callback.message, HOW_IT_WORKS_STEPS[step_index], step_index)
    await callback.answer()
