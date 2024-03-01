from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.models import User


to_settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔧Настройки⚙️', callback_data='settings')]
]
)

languages = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🇷🇺Русский🇷🇺', callback_data='ru')],
    [InlineKeyboardButton(text='🇧🇾Белорусский🇧🇾', callback_data='by')]
])

help_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Как я могу получить содержание билетов?', callback_data='get_a_ticket')],
    [InlineKeyboardButton(text='Как я могу пройти тест для закрепления материала?', callback_data='how_tests_pass')],
    [InlineKeyboardButton(text='Показать доступные команды', callback_data='available_commands')]
])

menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📜Перейти к билетам📜', callback_data='go_to_ticket')],
    [InlineKeyboardButton(text='📄Перейти к тестам📄', callback_data='go_to_tests')],
    [InlineKeyboardButton(text='📊Результаты тестов📊', callback_data='test_results_list')],
    [InlineKeyboardButton(text='🔧Настройки⚙️', callback_data='settings')]
])

admin_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Количество пользователей', callback_data='the_number_of_users')],
    [InlineKeyboardButton(text='Начать рыссылку', callback_data='start_spam')]
])

confirmation_of_the_newsletter = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='yes'), InlineKeyboardButton(text='Нет', callback_data='no')]
])

def create_settings_inline_keyboard(user: User) -> InlineKeyboardMarkup:
    
    bilder = InlineKeyboardBuilder()
    buttons = {
        f'Язык: {("🇷🇺", "🇧🇾")[user.language == "BY"]}': 'switch_language',
        f'Режим чтения: {("✈️", "💾")[user.read_mode == "file"]}': 'switch_read_mode',
        f'🏠Меню🏠': 'menu'
    }
    for text, callback_data in buttons.items():
        bilder.add(InlineKeyboardButton(text=text, callback_data=callback_data))
    bilder.adjust(1, 1, 1)
    return bilder.as_markup()

def create_pagination_inline_keyboard(page: int, max_pages: int = 5) -> InlineKeyboardMarkup:
    bilder = InlineKeyboardBuilder()
    buttons = {
        '<<': 'back',
        f'{page}/{max_pages}': 'empoty',
        '>>': 'forward',
         f'🏠Меню🏠': 'menu'
    }
    for text, callback_data in buttons.items():
        bilder.add(InlineKeyboardButton(text=text, callback_data=callback_data))
    bilder.adjust(3, 1)
    return bilder.as_markup()

