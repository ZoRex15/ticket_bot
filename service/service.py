from aiogram.types import Message, PollAnswer
import sqlite3
import random
from lexicon.lexicon import PHRASES
import json


def _create_poll(message_or_poll: Message, question_number: int, test_number: int):
    answer = Options.get_option(test=test_number, question=question_number)
    if isinstance(message_or_poll, PollAnswer):
        return message_or_poll.bot.send_poll(chat_id=message_or_poll.user.id,
                                    correct_option_id=answer,
                                    options=['a)', 'b)', 'c)'],
                                    question='Выберите один из вариантов',
                                    type='quiz',
                                    is_anonymous=False)
    return message_or_poll.bot.send_poll(chat_id=message_or_poll.from_user.id,
                                    correct_option_id=answer,
                                    options=['a)', 'b)', 'c)'],
                                    question='Выберите один из вариантов',
                                    type='quiz',
                                    is_anonymous=False)

def _create_poll_text(test_number: int, question_number: int) -> str:
    question = Tests.get_question(test=test_number, question=question_number)
    answers = Answers.get_answers(ticket=test_number, question=question_number)
    return question + '\nВарианты ответа\n' + '\n'.join(answers)

def _create_text_menu() -> str:
    return random.choice(PHRASES)

class Tests:
    with open('tests/tests.json', 'r', encoding='U8') as file:
        __TESTS = json.load(file)

    @classmethod
    def get_question(cls, test, question):
        return cls.__TESTS[f'ticket {test}'][f'question {question}']
    
    @classmethod
    def update_question(cls, test, question, new_question):
        with open('tests/tests.json', 'w') as file:
            cls.__TESTS[f'ticket {test}'][f'question {question}'] = new_question
            with open('tests/tests.json', 'w', encoding='U8') as file:
                json.dump(cls.__TESTS, file, indent=3, ensure_ascii=False)

class Answers:
    with open('tests/answers.json', 'r', encoding='U8') as file:
        __ANSWERS = json.load(file)

    @classmethod
    def get_answers(cls, ticket: int, question: int) -> list:
        return cls.__ANSWERS[f'ticket {ticket}'][f'question {question}']
    
    @classmethod
    def update_answer(cls, ticket: int, question: int, possible_answer: str, text: str):
        cls.__ANSWERS[f'ticket {ticket}'][f'question {question}'][possible_answer] = possible_answer + ' ' + text
        with open('tests/answers.json', 'w', encoding='U8') as file:
            json.dump(cls.__ANSWERS, file, indent=3, ensure_ascii=False)

class Options:
    with open('tests/options.json', 'r') as file:
        __OPTIONS = json.load(file)

    @classmethod
    def get_option(cls, test, question):
        return cls.__OPTIONS[f'ticket {test}'][f'question {question}']
    
    @classmethod
    def update_option(cls, test, question, new_option):
        _ = ('a)', 'b)', 'c)')
        with open('tests/options.json', 'w') as file:
            cls.__OPTIONS[f'ticket {test}'][f'question {question}'] = _.index(new_option)
            json.dump(cls.__OPTIONS, file)

class Database:
    __DATABASE = 'users.db'

    @classmethod
    def create_users_table(cls):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER,
            ticket_language TEXT DEFAULT 'RU',
            test INTEGER DEFAULT 0,
            number_of_correct_answers INTEGER DEFAULT 0,
            PRIMARY KEY(user_id)
            )''')
            
    @classmethod
    def set_user_id(cls, user_id: int):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            if not result:
                cursor.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
    
    @classmethod
    def set_ticket_language(cls, ticket_language: str, user_id: int):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('UPDATE users SET ticket_language = ? WHERE user_id = ?', (ticket_language, user_id))
        
    @classmethod
    def set_test_number(cls, test_number: int, user_id: int):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('UPDATE users SET test = ? WHERE user_id = ?', (test_number, user_id))
    
    @classmethod
    def get_test_number(cls, user_id):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            return result[2]
    
    @classmethod
    def get_ticket_language(cls, user_id):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            return result[1]
    
    @classmethod
    def append_to_crrect_answers(cls, user_id):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            cursor.execute('UPDATE users SET number_of_correct_answers = ? WHERE user_id = ?', (result[3] + 1, user_id))

    @classmethod
    def recet_and_get_a_correct_answers(cls, user_id):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            cursor.execute('UPDATE users SET number_of_correct_answers = ? WHERE user_id = ?', (0, user_id))
            return result[3]
        
    @classmethod
    def create_admin_table(cls):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS admins (
                           admin_id INTEGER,
                           ticket INTEGER DEFAULT 0,
                           question INTEGER DEFAULT 0,
                           possible_answer INTEGER DEFAULT 0,
                           PRIMARY KEY(admin_id)
            )''')

    @classmethod
    def add_admin(cls, admin_id):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT * FROM admins WHERE admin_id = ?', (admin_id,))
            result = cursor.fetchone()
            if not result:
                cursor.execute('INSERT INTO admins (admin_id) VALUES (?)', (admin_id,))

    @classmethod
    def set_test_admin(cls, admin_id: int, test: int):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('UPDATE admins SET ticket = ? WHERE admin_id = ?', (test, admin_id))
    
    @classmethod
    def set_question_admin(cls, admin_id: int, question: int):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('UPDATE admins SET question = ? WHERE admin_id = ?', (question, admin_id))

    @classmethod
    def set_possible_answer(cls, admin_id: int, possible_answer: int):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('UPDATE admins SET possible_answer = ? WHERE admin_id = ?', (possible_answer, admin_id))

    @classmethod
    def get_admin_data(cls, admin_id):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT * FROM admins WHERE admin_id = ?', (admin_id,))
            return cursor.fetchone()
