from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from lexicon.lexicon import LEXICON
from FSM.state import FSMSpam
from service.service import RabbitMQ
from database.requests import Database
from config.config import Config, load_config
from filters.filters import IsAdmin


router = Router()
config: Config = load_config()

@router.callback_query(F.data == 'the_number_of_users', IsAdmin(config.tg_bot.admin_ids))
async def the_number_of_users(callback: CallbackQuery, state: FSMContext):
    the_number_of_users = await Database.get_count_users()
    await callback.message.answer(text=f'Количество пользователей: {the_number_of_users}')
    await state.clear()

@router.callback_query(F.data == 'start_spam', IsAdmin(config.tg_bot.admin_ids))
async def start_spam(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(LEXICON['start_spam'])
    await state.set_state(FSMSpam.the_text_of_the_blower)

@router.callback_query(F.data == 'yes', StateFilter(FSMSpam.confirmation_of_the_newsletter), IsAdmin(config.tg_bot.admin_ids))
async def сonfirmation_of_the_newsletter(callback: CallbackQuery, state: FSMContext):
    admin_data = await Database.get_admin_data(admin_id=callback.from_user.id)
    await callback.message.answer(
        text='Запускаю рассылку!'
    )
    await RabbitMQ.send_message_spam_queue(
        chat_id=admin_data.chat_id, 
        message_id=admin_data.message_id
    )
    await state.clear()

@router.callback_query(F.data == 'no', StateFilter(FSMSpam.confirmation_of_the_newsletter), IsAdmin(config.tg_bot.admin_ids))
async def сonfirmation_of_the_newsletter(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text='Отменяю'
    )
    await state.clear()