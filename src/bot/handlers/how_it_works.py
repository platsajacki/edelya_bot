from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto, Message

from bot.buttons import (
    HOW_IT_WORKS_BACK_CALLBACK,
    HOW_IT_WORKS_FINISH_CALLBACK,
    HOW_IT_WORKS_NEXT_CALLBACK,
    HOW_IT_WORKS_START_CALLBACK,
    START_PLANNING_KEYBOARD,
    get_how_it_works_keyboard,
)
from bot.creation import router
from bot.messages import HOW_IT_WORKS_FINAL_MESSAGE, HOW_IT_WORKS_STEPS, HowItWorksStep
from bot.services.onboarding import (
    HOW_IT_WORKS_FINISHED_KEY,
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


async def set_how_it_works_step(state: FSMContext, step_index: int) -> None:
    await state.set_state(OnboardingStates.how_it_works)
    await state.update_data({HOW_IT_WORKS_FINISHED_KEY: False, HOW_IT_WORKS_STEP_INDEX_KEY: step_index})


@router.callback_query(F.data == HOW_IT_WORKS_START_CALLBACK)
async def start_how_it_works_callback_handler(callback: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(callback.message, Message):
        await callback.answer()
        return

    step_index = 0
    await set_how_it_works_step(state, step_index)
    await send_how_it_works_step(callback.message, step_index)
    await callback.answer()


@router.callback_query(F.data == HOW_IT_WORKS_BACK_CALLBACK)
@router.callback_query(F.data == HOW_IT_WORKS_NEXT_CALLBACK)
async def navigate_how_it_works_callback_handler(callback: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(callback.message, Message):
        await callback.answer()
        return

    current_step_index = await get_current_how_it_works_step_index(state)
    step_index = get_how_it_works_step_index(callback.data, current_step_index)
    if step_index is None:
        await callback.answer()
        return

    await set_how_it_works_step(state, step_index)
    await edit_how_it_works_step(callback.message, HOW_IT_WORKS_STEPS[step_index], step_index)
    await callback.answer()


@router.callback_query(F.data == HOW_IT_WORKS_FINISH_CALLBACK)
async def finish_how_it_works_callback_handler(callback: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(callback.message, Message):
        await callback.answer()
        return
    data = await state.get_data()
    if data.get(HOW_IT_WORKS_FINISHED_KEY) is True:
        await callback.answer()
        return
    await state.update_data({HOW_IT_WORKS_FINISHED_KEY: True})
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(HOW_IT_WORKS_FINAL_MESSAGE, reply_markup=START_PLANNING_KEYBOARD)
    await callback.answer()
