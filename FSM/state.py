from aiogram.fsm.state import State, StatesGroup

class FSMSettings(StatesGroup):
    language_selection = State()

class FSMTakeTheTest(StatesGroup):
    question_1 = State()
    question_2 = State()
    question_3 = State()
    question_4 = State()
    question_5 = State()
    end_poll = State()

class FSMAdminState(StatesGroup):
    in_admin_menu = State()

class FSMUpdateQuestion(StatesGroup):
    request_test = State()
    request_question = State()
    request_new_question = State()

class FSMUpdateOption(StatesGroup):
    request_test = State()
    request_question = State()
    request_new_option = State()

class FSMUpdateAnswerText(StatesGroup):
    request_test = State()
    request_question = State()
    request_possible_answer = State()
    request_answer_text = State()





