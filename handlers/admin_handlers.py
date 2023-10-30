from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import StateFilter, Command
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from lexicon.lexicon import LEXICON
from FSM.state import FSMAdminState, FSMUpdateQuestion, FSMUpdateOption, FSMUpdateAnswerText
from service.service import Database, Tests, Answers, Options
from keyboards.keyboard import keyboard_request_new_option, create_tests_keyboard, create_question_keyboard

router = Router()

@router.callback_query(F.data == 'update_question', StateFilter(FSMAdminState.in_admin_menu))
async def update_question(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text=LEXICON['request_test'], reply_markup=create_tests_keyboard())
    await state.set_state(FSMUpdateQuestion.request_test)

@router.message(StateFilter(FSMUpdateQuestion.request_test))
async def update_question_request_test(message: Message, state: FSMContext):
    tests_number = int(message.text.split()[1])
    if 1 <= tests_number <= 25:
        Database.set_test_admin(admin_id=message.from_user.id, test=tests_number)
        await message.answer(LEXICON['request_question'], reply_markup=create_question_keyboard())
        await state.set_state(FSMUpdateQuestion.request_question)

@router.message(StateFilter(FSMUpdateQuestion.request_question))
async def update_question_request_question(message: Message, state: FSMContext):
    question_number = int(message.text.split()[1])
    if 1 <= question_number <= 5:
        Database.set_question_admin(admin_id=message.from_user.id, question=question_number)
        await message.answer(LEXICON['request_new_question'], reply_markup=ReplyKeyboardRemove())
        await state.set_state(FSMUpdateQuestion.request_new_question)

@router.message(StateFilter(FSMUpdateQuestion.request_new_question))
async def update_question_request_new_question(message: Message, state: FSMContext):
    admin_data = Database.get_admin_data(message.from_user.id)
    Tests.update_question(test=admin_data[1],
                          question=admin_data[2],
                          new_question=f'<b>{message.text}</b>')
    await message.answer(LEXICON['the_issue_is_settled'])
    await state.clear()

@router.callback_query(F.data == 'update_option', StateFilter(FSMAdminState.in_admin_menu))
async def update_option(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(LEXICON['request_test'], reply_markup=create_tests_keyboard())
    await state.set_state(FSMUpdateOption.request_test)

@router.message(StateFilter(FSMUpdateOption.request_test))
async def update_option_request_test(message: Message, state: FSMContext):
    tests_number = int(message.text.split()[1])
    if 1 <= tests_number <= 25:
        Database.set_test_admin(admin_id=message.from_user.id, test=tests_number)
        await message.answer(LEXICON['request_question'], reply_markup=create_question_keyboard())
        await state.set_state(FSMUpdateOption.request_question)

@router.message(StateFilter(FSMUpdateOption.request_question))
async def update_option_request_question(message: Message, state: FSMContext):
    question_number = int(message.text.split()[1])
    if 1 <= question_number <= 5:
        Database.set_question_admin(admin_id=message.from_user.id, question=question_number)
        await message.answer(LEXICON['request_new_option'], reply_markup=keyboard_request_new_option)
        await state.set_state(FSMUpdateOption.request_new_option)

@router.message(StateFilter(FSMUpdateOption.request_new_option))
async def update_option_request_new_option(message: Message, state: FSMContext):
    admin_data = Database.get_admin_data(message.from_user.id)
    Options.update_option(test=admin_data[1],
                          question=admin_data[2],
                          new_option=message.text)
    await message.answer(LEXICON['answer_option_set'])
    await state.clear()

@router.callback_query(F.data == 'update_answer_text', StateFilter(FSMAdminState.in_admin_menu))
async def update_answer_text(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text=LEXICON['request_test'], reply_markup=create_tests_keyboard())
    await state.set_state(FSMUpdateAnswerText.request_test)

@router.message(StateFilter(FSMUpdateAnswerText.request_test))
async def update_answer_text_request_test(message: Message, state: FSMContext):
    tests_number = int(message.text.split()[1])
    if 1 <= tests_number <= 25:
        Database.set_test_admin(admin_id=message.from_user.id, test=tests_number)
        await message.answer(LEXICON['request_question'], reply_markup=create_question_keyboard())
        await state.set_state(FSMUpdateAnswerText.request_question)

@router.message(StateFilter(FSMUpdateAnswerText.request_question))
async def update_answer_text_request_question(message: Message, state: FSMContext):
    question_number = int(message.text.split()[1])
    if 1 <= question_number <= 5:
        Database.set_question_admin(admin_id=message.from_user.id, question=question_number)
        await message.answer(LEXICON['request_answer_text'], reply_markup=ReplyKeyboardRemove())
        await state.set_state(FSMUpdateAnswerText.request_possible_answer)
    
@router.message(StateFilter(FSMUpdateAnswerText.request_possible_answer))
async def update_answer_text_request_possible_answer(message: Message, state: FSMContext):
    Database.set_possible_answer(admin_id=message.from_user.id, possible_answer=message.text)
    await message.answer(text=LEXICON['request_answer_text'])
    await state.set_state(FSMUpdateAnswerText.request_answer_text)

@router.message(StateFilter(FSMUpdateAnswerText.request_answer_text))
async def update_answer_text_request_answer_text(message: Message, state: FSMContext):
    admin_data = Database.get_admin_data(message.from_user.id)
    Answers.update_answer(
        ticket=admin_data[1],
        question=admin_data[2],
        possible_answer=admin_data[3],
        text=message.text
    )
    state.clear()
#'<b>Когда произошло заселение территории, которая сейчас является Беларусью, древними людьми?</b>'
#b)
#a) Примерно в 15 веке н.э."
    
     