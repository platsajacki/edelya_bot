from aiogram.fsm.state import State, StatesGroup


class OnboardingStates(StatesGroup):
    how_it_works = State()
