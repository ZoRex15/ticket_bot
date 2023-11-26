from aiogram.fsm.state import State, StatesGroup


class FSMSettings(StatesGroup):
    language_selection = State()

class FSMTakeTheTicket(StatesGroup):
    ticket_choice = State()

class FSMTakeTheTest(StatesGroup):
    question_1 = State()
    question_2 = State()
    question_3 = State()
    question_4 = State()
    question_5 = State()
    end_poll = State()

class FSMAdminState(StatesGroup):
    in_admin_menu = State()