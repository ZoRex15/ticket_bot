from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardRemove
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext


from lexicon.lexicon import LEXICON
from keyboards.keyboard import start_setting, create_ticket_keyboard, keyboard_menu
from keyboards.inline_keyboard import help_menu, menu, create_pagination_inline_keyboard, create_settings_inline_keyboard, to_settings
from FSM.state import FSMSettings, FSMTakeTheTicket, FSMReadTicket
from path.path import path_ticket_by, path_ticket_ru
from service.service import Database, _create_text_menu, _create_test_result_page, Tickets


router: Router = Router()

@router.message(CommandStart(), StateFilter(default_state))
async def start(message: Message, state: FSMContext):
    Database.create_users_table()
    Database.set_user_id(message.from_user.id)
    await message.answer(LEXICON['/start'].format(
        name=message.from_user.full_name
    ),
    reply_markup=to_settings)

@router.message(Command(commands=['help']), StateFilter(default_state))
async def help(message: Message, state: FSMContext):
    await message.answer(LEXICON['/help'], reply_markup=help_menu)

@router.message(Command(commands=['menu']), StateFilter(default_state))
async def send_menu(message: Message, state: FSMContext):
    await message.answer(text=_create_text_menu
                         (user_id=message.from_user.id,
                           user_name=message.from_user.full_name
                            ),
                            reply_markup=menu)

@router.message(Command(commands=['cancel']), ~StateFilter(default_state))
async def cancel(message: Message, state: FSMContext):
    Database.recet_and_get_a_correct_answers(user_id=message.from_user.id)
    await message.answer(LEXICON['cancel'], reply_markup=keyboard_menu)
    await state.clear()

@router.message(F.text == '🔧Настройки⚙️', StateFilter(default_state))
async def start_settings(message: Message, state: FSMContext):
    await state.set_state(FSMSettings.choise_settings)
    await message.answer(LEXICON['settings'], reply_markup=create_settings_inline_keyboard(user_id=message.from_user.id))

@router.message(F.text == '🏠Меню🏠', StateFilter(default_state))
async def send_menu(message: Message, state: FSMContext):
    r = await message.answer(text='.', reply_markup=ReplyKeyboardRemove())
    await r.delete()
    await message.answer(text=_create_text_menu
        (
        user_name=message.from_user.full_name,
        user_id=message.from_user.id
        ),
        reply_markup=menu)

@router.callback_query(F.data == 'switch_language', StateFilter(FSMSettings.choise_settings))
async def switch_language(callback: CallbackQuery, state: FSMContext):
    user_language = Database.get_user_language(user_id=callback.from_user.id)
    Database.set_ticket_language(ticket_language=('RU', 'BY')[user_language == 'RU'],
                                 user_id=callback.from_user.id)
    await callback.message.edit_text(
        text=LEXICON['settings'],
        reply_markup=create_settings_inline_keyboard(user_id=callback.from_user.id)
    )

@router.callback_query(F.data == 'switch_read_mode', StateFilter(FSMSettings.choise_settings))
async def switch_read_mode(callback: CallbackQuery, state: FSMContext):
    user_read_mode = Database.get_user_read_mode(user_id=callback.from_user.id)
    Database.set_read_mode(user_id=callback.from_user.id,
                           read_mode=('file', 'telegram')[user_read_mode == 'file'])
    await callback.message.edit_text(
        text=LEXICON['settings'],
        reply_markup=create_settings_inline_keyboard(user_id=callback.from_user.id)
    )

@router.callback_query(F.data == 'menu', StateFilter(FSMSettings.choise_settings, FSMReadTicket.read_ticket))
async def return_to_menu(callback: CallbackQuery, state: FSMContext):
    Database.user_knock_page(user_id=callback.from_user.id)
    await callback.message.delete()
    await callback.message.answer(text=_create_text_menu
        (
        user_name=callback.from_user.full_name,
        user_id=callback.from_user.id
        ),
        reply_markup=menu)
    await state.clear()
    
@router.callback_query(F.data == 'how_tests_pass', StateFilter(default_state))
async def get_a_ticket(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON['how_tests_pass'])

@router.callback_query(F.data == 'get_a_ticket', StateFilter(default_state))
async def get_a_ticket(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON['how_to_get_a_ticket'])

@router.callback_query(F.data == 'available_commands', StateFilter(default_state))
async def available_commands(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(LEXICON['available_commands'])

@router.callback_query(F.data == 'go_to_ticket', StateFilter(default_state))
async def go_to_ticket(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(FSMTakeTheTicket.ticket_choice)
    await callback.message.answer(text=LEXICON['go_to_ticket'], reply_markup=create_ticket_keyboard())

@router.callback_query(F.data == 'settings', StateFilter(default_state))
async def settings(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(LEXICON['settings'], reply_markup=create_settings_inline_keyboard(
        user_id=callback.from_user.id))
    await state.set_state(FSMSettings.choise_settings)

@router.callback_query(F.data == 'test_results_list', StateFilter(default_state))
async def send_test_results_list(callback: CallbackQuery, state: FSMContext):
    page = Database.get_user_page(callback.from_user.id)
    await callback.message.delete()
    await callback.message.answer(text=_create_test_result_page(
        user_id=callback.from_user.id,
        page=page
    ),
    reply_markup=create_pagination_inline_keyboard(page))
    await state.set_state(FSMSettings.choise_settings)


@router.callback_query(F.data == 'forward', StateFilter(FSMSettings.choise_settings))
async def forward(callback: CallbackQuery, state: FSMContext):
    page = Database.get_user_page(callback.from_user.id)
    if page == 5:
        await callback.answer(LEXICON['forward_error'])
    else:
        Database.update_page(callback.from_user.id, page + 1)
        await callback.message.edit_text(text=_create_test_result_page(
            user_id=callback.from_user.id,
            page=page + 1
        ),
        reply_markup=create_pagination_inline_keyboard(page=page + 1))

@router.callback_query(F.data == 'back', StateFilter(FSMSettings.choise_settings))
async def forward(callback: CallbackQuery, state: FSMContext):
    page = Database.get_user_page(callback.from_user.id)
    if page == 1:
        await callback.answer(LEXICON['back_error'])
    else:
        Database.update_page(callback.from_user.id, page - 1)
        await callback.message.edit_text(text=_create_test_result_page(
            user_id=callback.from_user.id,
            page=page - 1,
        ),
        reply_markup=create_pagination_inline_keyboard(page=page - 1))

@router.callback_query(F.data == 'forward', StateFilter(FSMReadTicket.read_ticket))
async def forward(callback: CallbackQuery, state: FSMContext):
    tickets = Tickets()
    user_ticket = Database.get_user_ticket(user_id=callback.from_user.id)
    user_language = Database.get_user_language(user_id=callback.from_user.id)
    max_pages = tickets.get_count_pages_in_ticket(user_ticket, language=user_language)
    page = Database.get_user_page(callback.from_user.id)
    if page == max_pages:
        await callback.answer(LEXICON['forward_error'])
    else:
        Database.update_page(callback.from_user.id, page + 1)
        await callback.message.edit_text(
            text=tickets.get_ticket_page(ticket=user_ticket, page=page + 1, user_language=user_language),
            reply_markup=create_pagination_inline_keyboard(page=page + 1, max_pages=max_pages)
            )

@router.callback_query(F.data == 'back', StateFilter(FSMReadTicket.read_ticket))
async def forward(callback: CallbackQuery, state: FSMContext):
    tickets = Tickets()
    page = Database.get_user_page(callback.from_user.id)
    user_ticket = Database.get_user_ticket(user_id=callback.from_user.id)
    user_language = Database.get_user_language(user_id=callback.from_user.id)
    if page == 1:
        await callback.answer(LEXICON['back_error'])
    else:
        Database.update_page(callback.from_user.id, page - 1)
        await callback.message.edit_text(
            text=tickets.get_ticket_page(
                ticket=user_ticket, 
                page=page - 1,
                user_language=user_language),
            reply_markup=create_pagination_inline_keyboard(
                page=page - 1,
                max_pages=tickets.get_count_pages_in_ticket(user_ticket, language=user_language)),
            )

@router.message(StateFilter(FSMTakeTheTicket.ticket_choice))
async def send_ticket(message: Message, state: FSMContext):
    ticket_number = int(message.text.split()[-1])
    Database.set_ticket_number(user_id=message.from_user.id, ticket_number=ticket_number)
    user_language = Database.get_user_language(message.from_user.id)
    user_read_mode = Database.get_user_read_mode(message.from_user.id)
    tickets = Tickets()
    if user_read_mode == 'file':
        if user_language == 'RU' and message.text.lower() in path_ticket_ru:
            media: FSInputFile = FSInputFile(path=path_ticket_ru[message.text.lower()])
            await message.answer_document(document=media, reply_markup=keyboard_menu)
        elif user_language == 'BY' and message.text.lower() in path_ticket_by:
            media: FSInputFile = FSInputFile(path=path_ticket_by[message.text.lower()])
            await message.answer_document(document=media, reply_markup=keyboard_menu)
        await state.clear()
    elif user_read_mode == 'telegram':
        await state.set_state(FSMReadTicket.read_ticket)
        user_page = Database.get_user_page(user_id=message.from_user.id)
        user_ticket = int(message.text.split()[-1])
        _ = await message.answer(text='.', reply_markup=ReplyKeyboardRemove())
        await _.delete()
        await message.answer(
            text=tickets.get_ticket_page(ticket=user_ticket, page=user_page, user_language=user_language),
            reply_markup=create_pagination_inline_keyboard(page=user_page, max_pages=tickets.get_count_pages_in_ticket(ticket=user_ticket, language=user_language))
        )