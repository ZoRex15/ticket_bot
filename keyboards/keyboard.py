from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

start_setting: ReplyKeyboardMarkup = ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
    [KeyboardButton(text='🔧Настройки⚙️')]
])

keyboard_menu = ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
    [KeyboardButton(text='Меню')]
])

keyboard_request_new_option = ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
    [KeyboardButton(text='a)'), KeyboardButton(text='b)'), KeyboardButton(text='c)')]
])

def create_ticket_keyboard():
    bilder = ReplyKeyboardBuilder()
    for index in range(1, 26):
        bilder.add(KeyboardButton(text=f'Билет {index}'))
    bilder.adjust(3)
    return bilder.as_markup(resize_keyboard=True)

def create_tests_keyboard():
    bilder = ReplyKeyboardBuilder()
    for index in range(1, 26):
        bilder.add(KeyboardButton(text=f'Тест {index}'))
    bilder.adjust(3)
    return bilder.as_markup(resize_keyboard=True)

def create_question_keyboard():
    bilder = ReplyKeyboardBuilder()
    for index in range(1, 6):
        bilder.add(KeyboardButton(text=f'Вопрос {index}'))
    bilder.adjust(1)
    return bilder.as_markup(resize_keyboard=True)
