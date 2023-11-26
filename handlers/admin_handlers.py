from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import StateFilter, Command
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from lexicon.lexicon import LEXICON
from FSM.state import FSMAdminState
from service.service import Database
from config.config import Config, load_config
from filters.filters import IsAdmin
from keyboards.inline_keyboard import admin_menu


router = Router()
config: Config = load_config()

@router.message(Command(commands=['admin_menu']), StateFilter(default_state), IsAdmin(config.tg_bot.admin_ids))
async def send_admin_menu(message: Message, state: FSMContext):
    Database.create_admin_table()
    Database.add_admin(message.from_user.id)
    await message.answer(LEXICON['admin_menu'], reply_markup=admin_menu)
    await state.set_state(FSMAdminState.in_admin_menu)

@router.callback_query(F.data == 'the_number_of_users')
async def the_number_of_users(callback: CallbackQuery, state: FSMContext):
    the_number_of_users = Database.get_the_number_of_users()
    await callback.message.answer(text=f'Количество пользователей: {the_number_of_users}')
    await state.clear()