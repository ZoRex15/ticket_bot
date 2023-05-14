from aiogram import types, Router
from aiogram.filters import Command
from keyboard import kb, kb_bel, ikb
from text import start_text, commands_text, help_text
import datetime

router: Router = Router()

def choose_plural(amount,declensions):
    if amount % 10 == 1 and amount % 100 != 11:
        return f'{amount} {declensions[0]}'
    elif amount % 10 >= 2 and amount % 10 <= 4 and (amount % 100 < 10 or amount % 100 >= 20):
        return f'{amount} {declensions[1]}'
    else:
        return f'{amount} {declensions[2]}'


@router.message(Command(commands=['by']))
async def BY_language(message: types.Message):
    await message.answer(
                            text='<b>Клавиатура была сменена для беларусских билетов.</b>',
                            reply_markup=kb_bel,
                            parse_mode='HTML')
    
@router.message(Command(commands=['ru']))
async def RU_language(message: types.Message):
    await message.answer(
        
        text='<b>Клавиатруа была сменена для русских билетов.</b>',
        reply_markup=kb,
        parse_mode='HTML'
    )

@router.message(Command(commands=['commands']))
async def send_command(message: types.Message):
    await message.answer(text=commands_text, parse_mode='HTML')

@router.message(Command(commands=['website']))
async def send_website(message: types.Message):
    await message.answer(text='Сайт с тестами',reply_markup=ikb)

@router.message(Command(commands=['help']))
async def send_help(message: types.Message):
    await message.answer(text=help_text)
    await message.delete()

@router.message(Command(commands=['start']))
async def send_start(message: types.Message):
    await message.answer(
                           reply_markup=kb,
                            parse_mode='HTML',
                           text=start_text.format(name=message.from_user.full_name))


@router.message(Command(commands=['time']))
async def send_time(message: types.Message):
    second = datetime.datetime.now()
    data = datetime.datetime(year=2023, month=6, day=3)
    result = data - second 
    await message.answer(text=f'До экзамена по истории осталось {choose_plural(int(result.days),("день","дня","дней"))}')
    