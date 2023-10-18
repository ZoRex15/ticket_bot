from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardRemove
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext


from lexicon.lexicon import LEXICON
from keyboards.keyboard import start_setting, create_ticket_keyboard, keyboard_menu
from keyboards.inline_keyboard import languages, help_menu, menu
from FSM.state import FSMSettings, FSMTakeTheTest
from path.path import path_ticket_by, path_ticket_ru
from service.service import Database, create_text_menu


router: Router = Router()

@router.message(CommandStart(), StateFilter(default_state))
async def start(message: Message, state: FSMContext):
    Database.create_users_table()
    Database.set_user_id(message.from_user.id)
    await message.answer(LEXICON['/start'].format(
        name=message.from_user.full_name
    ),
    reply_markup=start_setting)

@router.message(Command(commands=['help']), StateFilter(default_state))
async def help(message: Message, state: FSMContext):
    await message.answer(LEXICON['/help'], reply_markup=help_menu)

@router.message(Command(commands=['menu']), StateFilter(default_state))
async def send_menu(message: Message, state: FSMContext):
    await message.answer(text=create_text_menu(), reply_markup=menu)

@router.message(Command(commands=['cancel']), StateFilter(FSMTakeTheTest))
async def cancel(message: Message, state: FSMContext):
    await message.answer(LEXICON['cancel'], reply_markup=keyboard_menu)
    await state.clear()

@router.message(F.text == '🔧Настройки⚙️', StateFilter(default_state))
async def start_settings(message: Message, state: FSMContext):
    await state.set_state(FSMSettings.language_selection)
    await message.answer(LEXICON['settings'], reply_markup=languages)

@router.message(F.text == 'Меню', StateFilter(default_state))
async def send_menu(message: Message, state: FSMContext):
    await message.answer(text=create_text_menu(), reply_markup=menu)

@router.callback_query(F.data == 'ru', StateFilter(FSMSettings.language_selection))
async def set_ru_language(callback: CallbackQuery, state: FSMContext):
    Database.set_ticket_language('RU', callback.from_user.id)
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(text=LEXICON['set_ru_language'], reply_markup=keyboard_menu)

@router.callback_query(F.data == 'by', StateFilter(FSMSettings.language_selection))
async def set_by_language(callback: CallbackQuery, state: FSMContext):
    Database.set_ticket_language('BY', callback.from_user.id)
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(text=LEXICON['set_by_language'], reply_markup=keyboard_menu)

@router.callback_query(F.data == 'get_a_ticket', StateFilter(default_state))
async def get_a_ticket(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON['how_to_get_a_ticket'])

@router.callback_query(F.data == 'available_commands', StateFilter(default_state))
async def available_commands(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(LEXICON['available_commands'])

@router.callback_query(F.data == 'go_to_ticket', StateFilter(default_state))
async def go_to_ticket(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text=LEXICON['go_to_ticket'], reply_markup=create_ticket_keyboard())

@router.callback_query(F.data == 'go_to_tests', StateFilter(default_state))
async def go_to_tests(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text=LEXICON['go_to_tests'], reply_markup=create_ticket_keyboard())
    await state.set_state(FSMTakeTheTest.question_1)

@router.callback_query(F.data == 'settings', StateFilter(default_state))
async def settings(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(LEXICON['settings'], reply_markup=languages)
    await state.set_state(FSMSettings.language_selection)

@router.message(StateFilter(default_state))
async def send_ticket(message: Message, state: FSMContext):
    ticket_language = Database.get_ticket_language(message.from_user.id)
    if ticket_language == 'RU' and message.text.lower() in path_ticket_ru:
        media: FSInputFile = FSInputFile(path=path_ticket_ru[message.text.lower()])
        await message.answer_document(document=media)
    elif ticket_language == 'BY' and message.text.lower() in path_ticket_by:
        media: FSInputFile = FSInputFile(path=path_ticket_by[message.text.lower()])
        await message.answer_document(document=media)