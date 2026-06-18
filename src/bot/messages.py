from dataclasses import dataclass
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent / 'assets'
HOW_IT_WORKS_IMAGES_DIR = ASSETS_DIR / 'how_it_works'


@dataclass(frozen=True, slots=True)
class HowItWorksStep:
    text: str
    image_path: Path


@dataclass(frozen=True, slots=True)
class HelpTopic:
    callback_data: str
    title: str
    text: str


START_MESSAGE = (
    'Привет! Это Еделя - приложение для планирования домашнего питания.\n\n'
    'Чтобы не думать каждый вечер, что приготовить: сохраняйте блюда, планируйте готовку на неделю, '
    'а Еделя соберет список продуктов.\n\n'
    'Первые 14 дней доступны бесплатно.'
)

HOW_IT_WORKS_STEPS = (
    HowItWorksStep(
        text=(
            '1. Добавьте блюда\n\n'
            'Сохраните любимый рецепт вручную или поручите AI разобрать текст рецепта, идею блюда '
            'или продукты, которые уже есть дома.'
        ),
        image_path=HOW_IT_WORKS_IMAGES_DIR / 'add_dish.png',
    ),
    HowItWorksStep(
        text=(
            '2. Запланируйте готовку\n\n'
            'Выберите, что и в какой день будете готовить. Так меню на неделю видно заранее, '
            'а не придумывается каждый вечер.'
        ),
        image_path=HOW_IT_WORKS_IMAGES_DIR / 'planning.png',
    ),
    HowItWorksStep(
        text=(
            '3. Получите список покупок\n\n'
            'Еделя соберет продукты из запланированных блюд. Останется только отметить, что уже куплено.'
        ),
        image_path=HOW_IT_WORKS_IMAGES_DIR / 'shopping_list.png',
    ),
)

HELP_MESSAGE = 'С чем помочь?'
CONTACT_MESSAGE = 'Напишите нам на почту:\n\n{email}'

HELP_TOPICS = (
    HelpTopic(
        callback_data='help:getting_started',
        title='Как начать пользоваться',
        text=(
            'Чтобы начать:\n\n'
            '1. Добавьте хотя бы одно блюдо.\n'
            '2. Выберите день, когда хотите его приготовить.\n'
            '3. Создайте список покупок по плану.\n\n'
            'После этого можно отмечать продукты, которые уже купили.'
        ),
    ),
    HelpTopic(
        callback_data='help:add_dish',
        title='Как добавить блюдо',
        text=(
            'Откройте Еделю и добавьте блюдо вручную: название, ингредиенты и описание приготовления.\n\n'
            'Если доступно AI-добавление, можно вставить текст рецепта, идею блюда или список продуктов.'
        ),
    ),
    HelpTopic(
        callback_data='help:shopping_list',
        title='Как работает список покупок',
        text=(
            'Список покупок собирается из блюд, которые добавлены в план питания.\n\n'
            'Выберите период, создайте список - Еделя объединит одинаковые ингредиенты '
            'и посчитает нужное количество.'
        ),
    ),
    HelpTopic(
        callback_data='help:subscription',
        title='Подписка и пробный период',
        text=(
            'Первые 14 дней доступны бесплатно.\n\n'
            'В Базовом тарифе доступны блюда, планирование питания и списки покупок.\n\n'
            'В тарифе Про дополнительно доступно AI-добавление блюд.'
        ),
    ),
)
