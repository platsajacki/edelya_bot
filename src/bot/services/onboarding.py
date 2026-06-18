from aiogram.fsm.context import FSMContext

from bot.buttons import (
    HOW_IT_WORKS_BACK_CALLBACK,
    HOW_IT_WORKS_NEXT_CALLBACK,
    HOW_IT_WORKS_START_CALLBACK,
)
from bot.messages import HELP_TOPICS, HOW_IT_WORKS_STEPS, HelpTopic

HOW_IT_WORKS_STEP_INDEX_KEY = 'how_it_works_step_index'
HOW_IT_WORKS_FINISHED_KEY = 'how_it_works_finished'


def get_how_it_works_step_index(callback_data: str | None, current_step_index: int) -> int | None:
    if callback_data == HOW_IT_WORKS_START_CALLBACK:
        return 0
    if callback_data == HOW_IT_WORKS_BACK_CALLBACK:
        return max(current_step_index - 1, 0)
    if callback_data == HOW_IT_WORKS_NEXT_CALLBACK:
        return min(current_step_index + 1, len(HOW_IT_WORKS_STEPS) - 1)
    return None


async def get_current_how_it_works_step_index(state: FSMContext) -> int:
    data = await state.get_data()
    step_index = data.get(HOW_IT_WORKS_STEP_INDEX_KEY, 0)
    if isinstance(step_index, int):
        return step_index
    return 0


def get_help_topic(callback_data: str | None) -> HelpTopic | None:
    if callback_data is None:
        return None
    return next((topic for topic in HELP_TOPICS if topic.callback_data == callback_data), None)
