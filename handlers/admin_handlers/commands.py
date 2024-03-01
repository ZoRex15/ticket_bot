from aiogram import Router
from aiogram.types import Message
from aiogram.filters import StateFilter, Command
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from lexicon.lexicon import LEXICON
from FSM.state import FSMAdminState
from database.requests import Database
from config.config import Config, load_config
from filters.filters import IsAdmin
from keyboards.inline_keyboard import admin_menu


router = Router()
config: Config = load_config()

@router.message(Command(commands=['admin_menu']), StateFilter(default_state), IsAdmin(config.tg_bot.admin_ids))
async def send_admin_menu(message: Message, state: FSMContext):
    await Database.add_admin(admin_id=message.from_user.id)
    await message.answer(LEXICON['admin_menu'], reply_markup=admin_menu)
    await state.set_state(FSMAdminState.in_admin_menu)