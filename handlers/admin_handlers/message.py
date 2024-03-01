from aiogram import Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext


from FSM.state import FSMSpam
from config.config import Config, load_config
from filters.filters import IsAdmin
from keyboards.inline_keyboard import confirmation_of_the_newsletter
from database.requests import Database


router = Router()
config: Config = load_config()

@router.message(StateFilter(FSMSpam.the_text_of_the_blower), IsAdmin(config.tg_bot.admin_ids))
async def the_text_of_the_blower(message: Message, state: FSMContext):
    await Database.update_admin_data(
        admin_id=message.from_user.id,
        message_id=message.message_id,
        chat_id=message.chat.id
    )
    await message.answer(
        text='Вы точно хотите это разослать?',
        reply_markup=confirmation_of_the_newsletter
    )
    await state.set_state(FSMSpam.confirmation_of_the_newsletter)