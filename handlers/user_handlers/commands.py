from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from lexicon.lexicon import LEXICON
from keyboards.keyboard import keyboard_menu
from keyboards.inline_keyboard import help_menu, menu, to_settings
from service.service import _create_text_menu
from database.requests import Database


router: Router = Router()

@router.message(CommandStart(), StateFilter(default_state))
async def start(message: Message, state: FSMContext):
    await Database.add_user(message.from_user.id)
    await message.answer(LEXICON['/start'].format(
        name=message.from_user.full_name
    ),
    reply_markup=to_settings)

@router.message(Command(commands=['help']), StateFilter(default_state))
async def help(message: Message, state: FSMContext):
    await message.answer(LEXICON['/help'], reply_markup=help_menu)

@router.message(Command(commands=['menu']), StateFilter(default_state))
async def send_menu(message: Message, state: FSMContext):
    user = await Database.get_user_data(user_id=message.from_user.id)
    await message.answer(text=_create_text_menu
                         (user=user,
                           user_name=message.from_user.full_name
                            ),
                            reply_markup=menu)

@router.message(Command(commands=['cancel']), ~StateFilter(default_state))
async def cancel(message: Message, state: FSMContext):
    Database.update_user_data(user_id=message.from_user.id,
                              number_of_correct_answers=0)
    await message.answer(LEXICON['cancel'], reply_markup=keyboard_menu)
    await state.clear()
