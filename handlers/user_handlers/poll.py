from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, ReplyKeyboardRemove, PollAnswer, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state


from FSM.state import FSMTakeTheTest
from lexicon.lexicon import LEXICON
from service.service import _create_poll, Database, _create_poll_text, Options
from keyboards.keyboard import keyboard_menu, create_ticket_keyboard
from database.requests import Database


router = Router()

@router.poll_answer(StateFilter(FSMTakeTheTest.question_2))
async def send_question_2(poll: PollAnswer, state: FSMContext):
    user = await Database.get_user_data(user_id=poll.user.id)
    if poll.option_ids[-1] == Options.get_option(test=user.test, question=1):
        await Database.update_user_data(
            user_id=poll.user.id,
            number_of_correct_answers=user.number_of_correct_answers + 1
        )
    await poll.bot.send_message(chat_id=poll.user.id, text=_create_poll_text(user_language=user.language, test_number=user.test, question_number=2, mode=user.language))
    await _create_poll(message_or_poll=poll, question_number=2, test_number=user.test)
    await state.set_state(FSMTakeTheTest.question_3)

@router.poll_answer(StateFilter(FSMTakeTheTest.question_3))
async def send_question_3(poll: PollAnswer, state: FSMContext):
    user = await Database.get_user_data(user_id=poll.user.id)
    if poll.option_ids[-1] == Options.get_option(test=user.test, question=2):
        await Database.update_user_data(
            user_id=poll.user.id,
            number_of_correct_answers=user.number_of_correct_answers + 1
        )
    await poll.bot.send_message(chat_id=poll.user.id, text=_create_poll_text(user_language=user.language, test_number=user.test, question_number=3, mode=user.language))
    await _create_poll(message_or_poll=poll, question_number=3, test_number=user.test)
    await state.set_state(FSMTakeTheTest.question_4)

@router.poll_answer(StateFilter(FSMTakeTheTest.question_4))
async def send_question_4(poll: PollAnswer, state: FSMContext):
    user = await Database.get_user_data(user_id=poll.user.id)
    if poll.option_ids[-1] == Options.get_option(test=user.test, question=3):
        await Database.update_user_data(
            user_id=poll.user.id,
            number_of_correct_answers=user.number_of_correct_answers + 1
        )
    await poll.bot.send_message(chat_id=poll.user.id, text=_create_poll_text(user_language=user.language, test_number=user.test, question_number=4, mode=user.language))
    await _create_poll(message_or_poll=poll, question_number=4, test_number=user.test)
    await state.set_state(FSMTakeTheTest.question_5)   

@router.poll_answer(StateFilter(FSMTakeTheTest.question_5))
async def send_last_question(poll: PollAnswer, state: FSMContext):
    user = await Database.get_user_data(user_id=poll.user.id)
    if poll.option_ids[-1] == Options.get_option(test=user.test, question=4):
        await Database.update_user_data(
            user_id=poll.user.id,
            number_of_correct_answers=user.number_of_correct_answers + 1
        )
    await poll.bot.send_message(chat_id=poll.user.id, text=_create_poll_text(user_language=user.language, test_number=user.test, question_number=5, mode=user.language))
    await _create_poll(message_or_poll=poll, question_number=5, test_number=user.test)
    await state.set_state(FSMTakeTheTest.end_poll)

@router.poll_answer(StateFilter(FSMTakeTheTest.end_poll))
async def end_poll(poll: PollAnswer, state: FSMContext):
    user = await Database.get_user_data(user_id=poll.user.id)
    if poll.option_ids[-1] == Options.get_option(test=user.test, question=5):
         await Database.update_user_data(
            user_id=poll.user.id,
            number_of_correct_answers=user.number_of_correct_answers + 1
        )
    user = await Database.get_user_data(user_id=poll.user.id)     
    test_result = user.number_of_correct_answers
    await Database.add_or_update_test_result(
        user_id=poll.user.id,
        test_number=user.test,
        grade=test_result
    )
    await Database.update_user_data(
        user_id=poll.user.id,
        number_of_correct_answers=0
    )
    await poll.bot.send_message(chat_id=poll.user.id, text=LEXICON['end_poll'].format(result=test_result), reply_markup=keyboard_menu)
    await state.clear()
