from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from lexicon.lexicon import LEXICON
from keyboards.keyboard import create_ticket_keyboard
from keyboards.inline_keyboard import menu, create_pagination_inline_keyboard, create_settings_inline_keyboard
from FSM.state import FSMSettings, FSMTakeTheTicket, FSMReadTicket, FSMTakeTheTest
from service.service import _create_text_menu,  Tickets
from database.requests import Database


router: Router = Router()

@router.callback_query(F.data == 'switch_language', StateFilter(FSMSettings.choise_settings))
async def switch_language(callback: CallbackQuery, state: FSMContext):
    user = await Database.get_user_data(user_id=callback.from_user.id)
    await Database.update_user_data(
        user_id=callback.from_user.id,
        language=('RU', 'BY')[user.language == 'RU']
    )
    user = await Database.get_user_data(user_id=callback.from_user.id)
    await callback.message.edit_text(
        text=LEXICON['settings'],
        reply_markup=create_settings_inline_keyboard(user=user)
    )

@router.callback_query(F.data == 'switch_read_mode', StateFilter(FSMSettings.choise_settings))
async def switch_read_mode(callback: CallbackQuery, state: FSMContext):
    user = await Database.get_user_data(user_id=callback.from_user.id)
    user = await Database.update_user_data(
        user_id=callback.from_user.id,
        read_mode=('file', 'telegram')[user.read_mode == 'file']
    )
    await callback.message.edit_text(
        text=LEXICON['settings'],
        reply_markup=create_settings_inline_keyboard(user=user)
    ) 

@router.callback_query(F.data == 'menu', StateFilter(FSMSettings.choise_settings, FSMReadTicket.read_ticket))
async def return_to_menu(callback: CallbackQuery, state: FSMContext):
    user = await Database.update_user_data(
        user_id=callback.from_user.id,
        page=1
        )
    await callback.message.delete()
    await callback.message.answer(text=_create_text_menu
        (
        user_name=callback.from_user.full_name,
        user=user
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
    user = await Database.get_user_data(user_id=callback.from_user.id)
    await callback.message.delete()
    await callback.message.answer(LEXICON['settings'], reply_markup=create_settings_inline_keyboard(
        user=user))
    await state.set_state(FSMSettings.choise_settings)

@router.callback_query(F.data == 'test_results_list', StateFilter(default_state))
async def send_test_results_list(callback: CallbackQuery, state: FSMContext):
    user = await Database.get_user_data(user_id=callback.from_user.id)
    await callback.message.delete()
    test_result_page = await Database.get_test_result_page(page=user.page, user_id=user.user_id)
    await callback.message.answer(text=test_result_page,
    reply_markup=create_pagination_inline_keyboard(user.page))
    await state.set_state(FSMSettings.choise_settings)


@router.callback_query(F.data == 'forward', StateFilter(FSMSettings.choise_settings))
async def forward(callback: CallbackQuery, state: FSMContext):
    user = await Database.get_user_data(user_id=callback.from_user.id)
    if user.page == 5:
        await callback.answer(LEXICON['forward_error'])
    else:
        user = await Database.update_user_data(user_id=callback.from_user.id, page=user.page + 1)
        test_result_page = await Database.get_test_result_page(page=user.page, user_id=user.user_id)
        await callback.message.edit_text(text=test_result_page,
        reply_markup=create_pagination_inline_keyboard(page=user.page))

@router.callback_query(F.data == 'back', StateFilter(FSMSettings.choise_settings))
async def forward(callback: CallbackQuery, state: FSMContext):
    user = await Database.get_user_data(user_id=callback.from_user.id)
    if user.page == 1:
        await callback.answer(LEXICON['back_error'])
    else:
        user = await Database.update_user_data(user_id=callback.from_user.id, page=user.page - 1)
        test_result_page = await Database.get_test_result_page(page=user.page, user_id=user.user_id)
        await callback.message.edit_text(text=test_result_page,
                            reply_markup=create_pagination_inline_keyboard(page=user.page))

@router.callback_query(F.data == 'forward', StateFilter(FSMReadTicket.read_ticket))
async def forward(callback: CallbackQuery, state: FSMContext):
    user = await Database.get_user_data(user_id=callback.from_user.id)
    tickets = Tickets()
    max_pages = tickets.get_count_pages_in_ticket(user.ticket, language=user.language)
    if user.page == max_pages:
        await callback.answer(LEXICON['forward_error'])
    else:
        user = await Database.update_user_data(
            user_id=callback.from_user.id,
            page=user.page + 1
        )
        await callback.message.edit_text(
            text=tickets.get_ticket_page(ticket=user.ticket, page=user.page, user_language=user.language),
            reply_markup=create_pagination_inline_keyboard(page=user.page, max_pages=max_pages)
            )

@router.callback_query(F.data == 'back', StateFilter(FSMReadTicket.read_ticket))
async def forward(callback: CallbackQuery, state: FSMContext):
    user = await Database.get_user_data(user_id=callback.from_user.id)
    tickets = Tickets()
    if user.page == 1:
        await callback.answer(LEXICON['back_error'])
    else:
        user = await Database.update_user_data(
            user_id=callback.from_user.id, 
            page=user.page)
        await callback.message.edit_text(
            text=tickets.get_ticket_page(
                ticket=user.ticket, 
                page=user.page,
                user_language=user.language),
            reply_markup=create_pagination_inline_keyboard(
                page=user.page,
                max_pages=tickets.get_count_pages_in_ticket(user.ticket, language=user.language)),
            )
        
@router.callback_query(F.data == 'go_to_tests', StateFilter(default_state))
async def go_to_tests(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text=LEXICON['go_to_tests'], reply_markup=create_ticket_keyboard())
    await state.set_state(FSMTakeTheTest.question_1)
