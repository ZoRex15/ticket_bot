
from aiogram import Bot, Router, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.types import CallbackQuery
from aiogram.filters import Command
import datetime
from keyboard import kb, ikb
from config import Config, load_config

config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token



BOT: Bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher()


ticket_dict = {'билет 1':'ticket/Билет 1.pdf', 'билет 2': 'ticket/Билет 2.pdf',
                'билет 3':'ticket/Билет 3.pdf', 'билет 4':'ticket/Билет 4.pdf',
                'билет 5':'ticket/Билет 5.pdf', 'билет 6':'ticket/Билет 6.pdf',
                'билет 7':'ticket/Билет 7.pdf', 'билет 8':'ticket/Билет 8.pdf',
                'билет 9':'ticket/Билет 9.pdf', 'билет 10':'ticket/Билет 10.pdf',
                'билет 11':'ticket/Билет 11.pdf', 'билет 12':'ticket/Билет 12.pdf',
                'билет 13':'ticket/Билет 13.pdf', 'билет 14':'ticket/Билет 14.pdf',
                'билет 15':'ticket/Билет 15.pdf', 'билет 16':'ticket/Билет 16.pdf',
                'билет 17':'ticket/Билет 17.pdf', 'билет 18':'ticket/Билет 18.pdf',
                'билет 19':'ticket/Билет 19.pdf', 'билет 20':'ticket/Билет 20.pdf',
                'билет 21':'ticket/Билет 21.pdf', 'билет 22':'ticket/Билет 22.pdf',
                'билет 23':'ticket/Билет 23.pdf', 'билет 24':'ticket/Билет 24.pdf',
                'билет 25':'ticket/Билет 25.pdf'} 

help_text = '''
Бот скидывает билеты по истории 
если ему написать Билет (номер билета)
пример: Билет 1
также допустимо БиЛет 1
результат будет тот же'''

commands_text = '''
<b>/help</b> - <em>Инструкция по использыванию бота</em>
<b>/commands</b> - <em>Список команд</em>
<b>/start</b> - <em>начать работу с ботом</em>
<b>/website</b> - <em>Ссылка на сайт с тестами</em>
<b>/time</b> - <em>Узнать сколько дней осталось до экзамена</em>
'''



def choose_plural(amount,declensions):
    if amount % 10 == 1 and amount % 100 != 11:
        return f'{amount} {declensions[0]}'
    elif amount % 10 >= 2 and amount % 10 <= 4 and (amount % 100 < 10 or amount % 100 >= 20):
        return f'{amount} {declensions[1]}'
    else:
        return f'{amount} {declensions[2]}'

@dp.message(Command(commands=['commands']))
async def send_command(message: types.Message):
    await BOT.send_message(chat_id=message.chat.id, text=commands_text, parse_mode='HTML')

@dp.message(Command(commands=['website']))
async def send_website(message: types.Message):
    await BOT.send_message(chat_id=message.chat.id, text='Сайт с тестами',reply_markup=ikb)

@dp.message(Command(commands=['help']))
async def send_help(message: types.Message):
    await BOT.send_message(chat_id=message.from_user.id, text=help_text)
    await message.delete()

@dp.message(Command(commands=['start']))
async def send_start(message: types.Message):
    await BOT.send_message(chat_id=message.chat.id,text='Добро пожаловать в наш телеграм бот!', reply_markup=kb)


@dp.message(Command(commands=['time']))
async def send_time(message: types.Message):
    second = datetime.datetime.now()
    data = datetime.datetime(year=2023, month=6, day=3)
    result = data - second 
    await BOT.send_message(chat_id=message.chat.id, text=f'До экзамена по истории осталось {choose_plural(int(result.days),("день","дня","дней"))}')
    

@dp.message()
async def ticket(message: types.Message):
    if str(message.text).lower() in ticket_dict:
        media = FSInputFile(path=ticket_dict[message.text.lower()])
        await BOT.send_document(chat_id=message.chat.id, document=media)


    
if __name__ == '__main__':
    dp.run_polling(BOT)
    
