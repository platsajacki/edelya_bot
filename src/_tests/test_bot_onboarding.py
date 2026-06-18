from pathlib import Path

from bot.buttons import (
    HELP_BACK_CALLBACK,
    HELP_START_CALLBACK,
    HOW_IT_WORKS_BACK_CALLBACK,
    HOW_IT_WORKS_NEXT_CALLBACK,
    HOW_IT_WORKS_START_CALLBACK,
    OPEN_APP_BUTTON_TEXT,
    OPEN_APP_KEYBOARD,
    START_KEYBOARD,
    get_help_keyboard,
    get_help_topic_keyboard,
    get_how_it_works_keyboard,
)
from bot.messages import HELP_MESSAGE, HELP_TOPICS, HOW_IT_WORKS_STEPS, START_MESSAGE, HelpTopic, HowItWorksStep
from bot.services.onboarding import get_help_topic, get_how_it_works_step_index
from settings.conf import SUPPORT_EMAIL


class TestBotOnboardingMessages:
    def test_start_message_focuses_on_first_value(self) -> None:
        assert 'не думать каждый вечер, что приготовить' in START_MESSAGE
        assert 'Первые 14 дней доступны бесплатно' in START_MESSAGE
        assert 'Как начать:' not in START_MESSAGE

    def test_how_it_works_has_three_steps_with_images(self) -> None:
        assert len(HOW_IT_WORKS_STEPS) == 3
        assert all(isinstance(step, HowItWorksStep) for step in HOW_IT_WORKS_STEPS)
        assert [step.image_path.name for step in HOW_IT_WORKS_STEPS] == [
            'add_dish.png',
            'planning.png',
            'shopping_list.png',
        ]
        assert all(isinstance(step.image_path, Path) for step in HOW_IT_WORKS_STEPS)

    def test_how_it_works_step_texts_are_ordered(self) -> None:
        assert HOW_IT_WORKS_STEPS[0].text.startswith('1. Добавьте блюда')
        assert HOW_IT_WORKS_STEPS[1].text.startswith('2. Запланируйте готовку')
        assert HOW_IT_WORKS_STEPS[2].text.startswith('3. Получите список покупок')

    def test_help_has_short_menu_and_topics(self) -> None:
        assert HELP_MESSAGE == 'С чем помочь?'
        assert all(isinstance(topic, HelpTopic) for topic in HELP_TOPICS)
        assert [topic.title for topic in HELP_TOPICS] == [
            'Как начать пользоваться',
            'Как добавить блюдо',
            'Как работает список покупок',
            'Подписка и пробный период',
        ]


class TestBotOnboardingKeyboards:
    def test_start_keyboard_has_primary_action_and_explanation(self) -> None:
        primary_button = START_KEYBOARD.inline_keyboard[0][0]
        explanation_button = START_KEYBOARD.inline_keyboard[1][0]

        assert primary_button.text == OPEN_APP_BUTTON_TEXT
        assert primary_button.web_app is not None
        assert explanation_button.text == 'Как это работает'
        assert explanation_button.callback_data == HOW_IT_WORKS_START_CALLBACK
        assert [button.text for button in START_KEYBOARD.inline_keyboard[2]] == ['Помощь', 'Связаться с нами']
        assert START_KEYBOARD.inline_keyboard[2][0].callback_data == HELP_START_CALLBACK
        contact_button = START_KEYBOARD.inline_keyboard[2][1]
        assert contact_button.url is None
        assert contact_button.copy_text is not None
        assert contact_button.copy_text.text == SUPPORT_EMAIL

    def test_open_app_keyboard_has_only_primary_action(self) -> None:
        assert len(OPEN_APP_KEYBOARD.inline_keyboard) == 1
        assert len(OPEN_APP_KEYBOARD.inline_keyboard[0]) == 1
        assert OPEN_APP_KEYBOARD.inline_keyboard[0][0].text == OPEN_APP_BUTTON_TEXT

    def test_first_how_it_works_keyboard_has_next_and_open_app_actions(self) -> None:
        keyboard = get_how_it_works_keyboard(step_index=0, total_steps=3)

        assert keyboard.inline_keyboard[0][0].text == 'Дальше'
        assert keyboard.inline_keyboard[0][0].callback_data == HOW_IT_WORKS_NEXT_CALLBACK
        assert keyboard.inline_keyboard[1][0].text == OPEN_APP_BUTTON_TEXT

    def test_middle_how_it_works_keyboard_has_back_next_and_open_app_actions(self) -> None:
        keyboard = get_how_it_works_keyboard(step_index=1, total_steps=3)

        assert [button.text for button in keyboard.inline_keyboard[0]] == ['Назад', 'Дальше']
        assert [button.callback_data for button in keyboard.inline_keyboard[0]] == [
            HOW_IT_WORKS_BACK_CALLBACK,
            HOW_IT_WORKS_NEXT_CALLBACK,
        ]
        assert keyboard.inline_keyboard[1][0].text == OPEN_APP_BUTTON_TEXT

    def test_last_how_it_works_keyboard_has_back_and_open_app_actions(self) -> None:
        keyboard = get_how_it_works_keyboard(step_index=2, total_steps=3)

        assert keyboard.inline_keyboard[0][0].text == 'Назад'
        assert keyboard.inline_keyboard[0][0].callback_data == HOW_IT_WORKS_BACK_CALLBACK
        assert keyboard.inline_keyboard[1][0].text == OPEN_APP_BUTTON_TEXT

    def test_help_keyboard_has_topic_actions_and_contact(self) -> None:
        keyboard = get_help_keyboard()

        assert [row[0].text for row in keyboard.inline_keyboard[:-1]] == [topic.title for topic in HELP_TOPICS]
        assert [row[0].callback_data for row in keyboard.inline_keyboard[:-1]] == [
            topic.callback_data for topic in HELP_TOPICS
        ]
        assert keyboard.inline_keyboard[-1][0].text == 'Связаться с нами'
        contact_button = keyboard.inline_keyboard[-1][0]
        assert contact_button.url is None
        assert contact_button.copy_text is not None
        assert contact_button.copy_text.text == SUPPORT_EMAIL

    def test_help_topic_keyboard_has_open_back_and_contact_actions(self) -> None:
        keyboard = get_help_topic_keyboard()

        assert keyboard.inline_keyboard[0][0].text == OPEN_APP_BUTTON_TEXT
        assert keyboard.inline_keyboard[1][0].callback_data == HELP_BACK_CALLBACK
        assert keyboard.inline_keyboard[2][0].text == 'Связаться с нами'


class TestBotOnboardingState:
    def test_start_callback_resets_step_index(self) -> None:
        assert get_how_it_works_step_index(HOW_IT_WORKS_START_CALLBACK, current_step_index=2) == 0

    def test_back_callback_does_not_go_below_first_step(self) -> None:
        assert get_how_it_works_step_index(HOW_IT_WORKS_BACK_CALLBACK, current_step_index=0) == 0

    def test_next_callback_does_not_go_after_last_step(self) -> None:
        last_step_index = len(HOW_IT_WORKS_STEPS) - 1

        assert (
            get_how_it_works_step_index(HOW_IT_WORKS_NEXT_CALLBACK, current_step_index=last_step_index)
            == last_step_index
        )

    def test_get_help_topic_returns_topic_by_callback_data(self) -> None:
        topic = HELP_TOPICS[0]

        assert get_help_topic(topic.callback_data) == topic
