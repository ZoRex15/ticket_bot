from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import StateFilter, Command
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext


from lexicon.lexicon import LEXICON
from FSM.state import FSMAdminState, FSMSpam
from service.service import Database, RabbitMQ
from config.config import Config, load_config
from filters.filters import IsAdmin
from keyboards.inline_keyboard import admin_menu, confirmation_of_the_newsletter


router = Router()
config: Config = load_config()

@router.message(Command(commands=['admin_menu']), StateFilter(default_state), IsAdmin(config.tg_bot.admin_ids))
async def send_admin_menu(message: Message, state: FSMContext):
    Database.create_admin_table()
    Database.add_admin(message.from_user.id)
    await message.answer(LEXICON['admin_menu'], reply_markup=admin_menu)
    await state.set_state(FSMAdminState.in_admin_menu)

@router.callback_query(F.data == 'the_number_of_users', IsAdmin(config.tg_bot.admin_ids))
async def the_number_of_users(callback: CallbackQuery, state: FSMContext):
    the_number_of_users = Database.get_the_number_of_users()
    await callback.message.answer(text=f'Количество пользователей: {the_number_of_users}')
    await state.clear()

@router.callback_query(F.data == 'start_spam', IsAdmin(config.tg_bot.admin_ids))
async def start_spam(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(LEXICON['start_spam'])
    await state.set_state(FSMSpam.the_text_of_the_blower)

@router.message(StateFilter(FSMSpam.the_text_of_the_blower), IsAdmin(config.tg_bot.admin_ids))
async def the_text_of_the_blower(message: Message, state: FSMContext):
    Database.set_chat_id(admin_id=message.from_user.id,
                         chat_id=message.chat.id,)
    Database.set_message_id(admin_id=message.from_user.id,
                            message_id=message.message_id)
    await message.answer(
        text='Вы точно хотите это разослать?',
        reply_markup=confirmation_of_the_newsletter
    )
    await state.set_state(FSMSpam.confirmation_of_the_newsletter)

@router.callback_query(F.data == 'yes', StateFilter(FSMSpam.confirmation_of_the_newsletter), IsAdmin(config.tg_bot.admin_ids))
async def сonfirmation_of_the_newsletter(callback: CallbackQuery, state: FSMContext):
    chat_id = Database.get_chat_id(callback.from_user.id)
    message_id = Database.get_message_id(callback.from_user.id)
    await callback.message.answer(
        text='Запускаю рассылку!'
    )
    await RabbitMQ.send_message_spam_queue(
        chat_id=chat_id, 
        message_id=message_id
    )
    Database.clear_spam_settings(callback.from_user.id)
    await state.clear()

@router.callback_query(F.data == 'no', StateFilter(FSMSpam.confirmation_of_the_newsletter), IsAdmin(config.tg_bot.admin_ids))
async def сonfirmation_of_the_newsletter(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text='Отменяю'
    )
    Database.clear_spam_settings(callback.from_user.id)
    await state.clear()