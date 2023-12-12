from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


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

def create_pagination_inline_keyboard(page):
    bilder = InlineKeyboardBuilder()
    buttons = {
        '<<': 'back',
        f'{page}/5': 'empoty',
        '>>': 'forward'
    }
    for text, callback_data in buttons.items():
        bilder.add(InlineKeyboardButton(text=text, callback_data=callback_data))
    bilder.adjust(3)
    return bilder.as_markup()

