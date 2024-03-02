from aiogram import Router, F
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from lexicon.lexicon import LEXICON
from keyboards.keyboard import keyboard_menu
from keyboards.inline_keyboard import menu, create_pagination_inline_keyboard, create_settings_inline_keyboard
from FSM.state import FSMSettings, FSMTakeTheTicket, FSMReadTicket, FSMTakeTheTest
from path.path import path_ticket_by, path_ticket_ru
from service.service import _create_text_menu, Tickets, _create_poll, _create_poll_text
from database.requests import Database


router = Router()

@router.message(F.text == '🔧Настройки⚙️', StateFilter(default_state))
async def start_settings(message: Message, state: FSMContext):
    await state.set_state(FSMSettings.choise_settings)
    await message.answer(LEXICON['settings'], reply_markup=create_settings_inline_keyboard(user_id=message.from_user.id))

@router.message(F.text == '🏠Меню🏠', StateFilter(default_state))
async def send_menu(message: Message, state: FSMContext):
    user = await Database.get_user_data(user_id=message.from_user.id)
    r = await message.answer(text='.', reply_markup=ReplyKeyboardRemove())
    await r.delete()
    await message.answer(text=_create_text_menu
        (
        user=user,
        user_name=message.from_user.full_name
        ),
        reply_markup=menu)
    
@router.message(StateFilter(FSMTakeTheTest.question_1))
async def test_selection(message: Message, state: FSMContext):
    result = int(message.text.split(' ')[1])
    user = await Database.update_user_data(
        user_id=message.from_user.id,
        test=result
    )
    await message.answer(text=_create_poll_text(user_language=user.language, test_number=result, question_number=1, mode=user.language), reply_markup=ReplyKeyboardRemove())
    await _create_poll(message_or_poll=message, question_number=1, test_number=user.test)
    await state.set_state(FSMTakeTheTest.question_2)
    
@router.message(StateFilter(FSMTakeTheTicket.ticket_choice))
async def send_ticket(message: Message, state: FSMContext):
    ticket_number = int(message.text.split()[-1])
    user = await Database.update_user_data(
        user_id=message.from_user.id,
        ticket=ticket_number
    )
    tickets = Tickets()
    if user.read_mode == 'file':
        if user.language == 'RU' and message.text.lower() in path_ticket_ru:
            media: FSInputFile = FSInputFile(path=path_ticket_ru[message.text.lower()])
            await message.answer_document(document=media, reply_markup=keyboard_menu)
        elif user.language == 'BY' and message.text.lower() in path_ticket_by:
            media: FSInputFile = FSInputFile(path=path_ticket_by[message.text.lower()])
            await message.answer_document(document=media, reply_markup=keyboard_menu)
        await state.clear()
    elif user.read_mode == 'telegram':
        await state.set_state(FSMReadTicket.read_ticket)
        user_ticket = int(message.text.split()[-1])
        _ = await message.answer(text='.', reply_markup=ReplyKeyboardRemove())
        await _.delete()
        await message.answer(
            text=tickets.get_ticket_page(ticket=user_ticket, page=user.page, user_language=user.language),
            reply_markup=create_pagination_inline_keyboard(page=user.page, max_pages=tickets.get_count_pages_in_ticket(ticket=user_ticket, language=user.language))
        )