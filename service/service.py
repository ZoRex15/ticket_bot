from aiogram.types import Message, PollAnswer
import sqlite3
from service.options import option_dict
import random
from lexicon.lexicon import PHRASES




def create_poll(message_or_poll: Message, question_number: int, test_number: int):
    if isinstance(message_or_poll, PollAnswer):
        answer = option_dict[f'ticket {test_number}'][f'question {question_number}']
        return message_or_poll.bot.send_poll(chat_id=message_or_poll.user.id,
                                    correct_option_id=answer,
                                    options=['a)', 'b)', 'c)'],
                                    question='Выберите один из вариантов',
                                    type='quiz',
                                    is_anonymous=False)
    answer = option_dict[f'ticket {test_number}'][f'question {question_number}']
    return message_or_poll.bot.send_poll(chat_id=message_or_poll.from_user.id,
                                    correct_option_id=answer,
                                    options=['a)', 'b)', 'c)'],
                                    question='Выберите один из вариантов',
                                    type='quiz',
                                    is_anonymous=False)

def create_text_menu() -> str:
    return random.choice(PHRASES)


class Database:
    __DATABASE = 'users.db'

    @classmethod
    def create_users_table(cls):
        connection = sqlite3.connect(cls.__DATABASE)
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER,
        ticket_language TEXT DEFAULT 'RU',
        test INTEGER DEFAULT 0,
        number_of_correct_answers INTEGER DEFAULT 0,
        PRIMARY KEY(user_id)
        )''')
        connection.commit()
        connection.close()

    @classmethod
    def set_user_id(cls, user_id: int):
        connection = sqlite3.connect(cls.__DATABASE)
        cursor = connection.cursor()
        current_id = cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
        
        # Если пользователя ещё нет в БД
        if not current_id:
            cursor.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
        connection.commit()
        connection.close()

    @classmethod
    def set_ticket_language(cls, ticket_language: str, user_id: int):
        connection = sqlite3.connect(cls.__DATABASE)
        cursor = connection.cursor()
        cursor.execute('REPLACE INTO users (ticket_language, user_id) VALUES (?, ?)', (ticket_language, user_id))
        connection.commit()
        connection.close()

    @classmethod
    def set_test_number(cls, test_number: int, user_id: int):
        connection = sqlite3.connect(cls.__DATABASE)
        cursor = connection.cursor()
        cursor.execute('REPLACE INTO users (test, user_id) VALUES (?, ?)', (test_number, user_id))
        connection.commit()
        connection.close()
    
    @classmethod
    def get_test_number(cls, user_id):
        connection = sqlite3.connect(cls.__DATABASE)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        connection.commit()
        connection.close()
        return result[2]
    
    @classmethod
    def get_ticket_language(cls, user_id):
        connection = sqlite3.connect(cls.__DATABASE)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        connection.close()
        return result[1]
    
    @classmethod
    def append_to_crrect_answers(cls, user_id):
        connection = sqlite3.connect(cls.__DATABASE)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        cursor.execute('UPDATE users SET number_of_correct_answers = ? WHERE user_id = ?', (result[3] + 1, user_id))
        connection.commit()
        connection.close()

    @classmethod
    def recet_and_get_a_correct_answers(cls, user_id):
        connection = sqlite3.connect(cls.__DATABASE)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        cursor.execute('REPLACE INTO users (number_of_correct_answers, user_id) VALUES (?, ?)', (0, user_id))
        connection.commit()
        connection.close()
        return result[3]
    


