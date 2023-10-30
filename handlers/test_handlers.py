from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, ReplyKeyboardRemove, PollAnswer
from aiogram.fsm.context import FSMContext

from FSM.state import FSMTakeTheTest
from lexicon.lexicon import LEXICON
from service.service import _create_poll, Database, _create_poll_text, Options
from keyboards.keyboard import keyboard_menu


router = Router()

@router.message(StateFilter(FSMTakeTheTest.question_1))
async def test_selection(message: Message, state: FSMContext):
    result = int(message.text.split(' ')[1])
    Database.set_test_number(result, message.from_user.id)
    await message.answer(text=_create_poll_text(test_number=result, question_number=1), reply_markup=ReplyKeyboardRemove())
    await _create_poll(message_or_poll=message, question_number=1, test_number=Database.get_test_number(message.from_user.id))
    await state.set_state(FSMTakeTheTest.question_2)
    
@router.poll_answer(StateFilter(FSMTakeTheTest.question_2))
async def send_question_2(poll: PollAnswer, state: FSMContext):
    test_number = Database.get_test_number(poll.user.id)
    if poll.option_ids[-1] == Options.get_option(test=test_number, question=1):
        Database.append_to_crrect_answers(poll.user.id)
    await poll.bot.send_message(chat_id=poll.user.id, text=_create_poll_text(test_number=test_number, question_number=2))
    await _create_poll(message_or_poll=poll, question_number=2, test_number=test_number)
    await state.set_state(FSMTakeTheTest.question_3)

@router.poll_answer(StateFilter(FSMTakeTheTest.question_3))
async def send_question_3(poll: PollAnswer, state: FSMContext):
    test_number = Database.get_test_number(poll.user.id)
    if poll.option_ids[-1] == Options.get_option(test=test_number, question=2):
        Database.append_to_crrect_answers(poll.user.id)
    await poll.bot.send_message(chat_id=poll.user.id, text=_create_poll_text(test_number=test_number, question_number=3))
    await _create_poll(message_or_poll=poll, question_number=3, test_number=test_number)
    await state.set_state(FSMTakeTheTest.question_4)

@router.poll_answer(StateFilter(FSMTakeTheTest.question_4))
async def send_question_4(poll: PollAnswer, state: FSMContext):
    test_number = Database.get_test_number(poll.user.id)
    if poll.option_ids[-1] == Options.get_option(test=test_number, question=3):
        Database.append_to_crrect_answers(poll.user.id)
    await poll.bot.send_message(chat_id=poll.user.id, text=_create_poll_text(test_number=test_number, question_number=4))
    await _create_poll(message_or_poll=poll, question_number=4, test_number=test_number)
    await state.set_state(FSMTakeTheTest.question_5)   

@router.poll_answer(StateFilter(FSMTakeTheTest.question_5))
async def send_last_question(poll: PollAnswer, state: FSMContext):
    test_number = Database.get_test_number(poll.user.id)
    if poll.option_ids[-1] == Options.get_option(test=test_number, question=4):
        Database.append_to_crrect_answers(poll.user.id)
    await poll.bot.send_message(chat_id=poll.user.id, text=_create_poll_text(test_number=test_number, question_number=5))
    await _create_poll(message_or_poll=poll, question_number=5, test_number=test_number)
    await state.set_state(FSMTakeTheTest.end_poll)

@router.poll_answer(StateFilter(FSMTakeTheTest.end_poll))
async def end_poll(poll: PollAnswer, state: FSMContext):
    test_number = Database.get_test_number(poll.user.id)
    if poll.option_ids[-1] == Options.get_option(test=test_number, question=5):
        Database.append_to_crrect_answers(poll.user.id)
    await poll.bot.send_message(chat_id=poll.user.id, text=LEXICON['end_poll'].format(result=Database.recet_and_get_a_correct_answers(poll.user.id)), reply_markup=keyboard_menu)
    await state.clear()
