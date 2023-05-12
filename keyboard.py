from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [KeyboardButton(text='Билет 1'), KeyboardButton(text='Билет 2'), KeyboardButton(text='Билет 3')],
    [KeyboardButton(text='Билет 4'), KeyboardButton(text='Билет 5'), KeyboardButton(text='Билет 6')],
    [KeyboardButton(text='Билет 7'), KeyboardButton(text='Билет 8'), KeyboardButton(text='Билет 9')],
    [KeyboardButton(text='Билет 10'), KeyboardButton(text='Билет 11'), KeyboardButton(text='Билет 12')],
    [KeyboardButton(text='Билет 13'), KeyboardButton(text='Билет 14'), KeyboardButton(text='Билет 15')],
    [KeyboardButton(text='Билет 16'), KeyboardButton(text='Билет 17'), KeyboardButton(text='Билет 18')],
    [KeyboardButton(text='Билет 19'), KeyboardButton(text='Билет 20'), KeyboardButton(text='Билет 21')],
    [KeyboardButton(text='Билет 22'), KeyboardButton(text='Билет 23'), KeyboardButton(text='Билет 24')],
    [KeyboardButton(text='Билет 25')]
    
])

kb_bel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [KeyboardButton(text='Билет 1 Б'), KeyboardButton(text='Билет 2 Б'), KeyboardButton(text='Билет 3 Б')],
    [KeyboardButton(text='Билет 4 Б'), KeyboardButton(text='Билет 5 Б'), KeyboardButton(text='Билет 6 Б')],
    [KeyboardButton(text='Билет 7 Б'), KeyboardButton(text='Билет 8 Б'), KeyboardButton(text='Билет 9 Б')],
    [KeyboardButton(text='Билет 10 Б'), KeyboardButton(text='Билет 11 Б'), KeyboardButton(text='Билет 12 Б')],
    [KeyboardButton(text='Билет 13 Б'), KeyboardButton(text='Билет 14 Б'), KeyboardButton(text='Билет 15 Б')],
    [KeyboardButton(text='Билет 16 Б'), KeyboardButton(text='Билет 17 Б'), KeyboardButton(text='Билет 18 Б')],
    [KeyboardButton(text='Билет 19 Б'), KeyboardButton(text='Билет 20 Б'), KeyboardButton(text='Билет 21 Б')],
    [KeyboardButton(text='Билет 22 Б'), KeyboardButton(text='Билет 23 Б'), KeyboardButton(text='Билет 24 Б')],
    [KeyboardButton(text='Билет 25 Б')]
])






ikb = InlineKeyboardMarkup(row_width=2,inline_keyboard=[
    [InlineKeyboardButton(text='Сайт',
                          url='https://adu.by/ru/homepage/okonchanie-uchebnogo-goda-2022-2023/405-pedagogam/okonchanie-uchebnogo-goda-2022-2023/bank-prakticheskikh-zadanij-dlya-ekzamena/6782-bank-prakticheskikh-zadanij-dlya-ekzamena.html',
                          )]
])
