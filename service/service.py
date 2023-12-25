from aiogram.types import Message, PollAnswer
import sqlite3
import json
import aio_pika
from path.path import path_ticket_ru_txt, path_ticket_by_txt


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

def _create_poll_text(user_language : str, test_number: int, question_number: int, mode: str) -> str:
    question = Tests.get_question(test=test_number, question=question_number, mode=mode)
    answers = Answers.get_answers(ticket=test_number, question=question_number, mode=mode)
    return f'<b>{question_number}. </b>' + question + ("\nВарианты ответа:\n", "\nВарыянты адказу:\n")[user_language == "BY"] + '\n'.join(answers)

def _create_text_menu(user_id: int, user_name: str) -> str:
    user_id, language, read_mode = Database.get_user_data(user_id=user_id)
    text_menu = f'''👤 Добро пожаловать, {user_name} 
├Ваш ID: {user_id}
├Язык: {('🇧🇾', '🇷🇺')[language == 'RU']}
├Режим чтения: {("✈️", "💾")[read_mode == "file"]}'''
    return text_menu

def _create_test_result_page(user_id: int, page: int):
    result = Database.get_test_results(user_id)[1:]
    test_number = [_ for _ in range(1, 26)]
    return '\n'.join([f'📄Тест {i}: {result}/5' for result, i in zip(result[5 * (page - 1):5 * page], test_number[5 * (page - 1):5 * page])])

def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    end_signs = ',.!:;?<>'
    counter = 0
    if len(text) < start + size:
        size = len(text) - start
        text = text[start:start + size]
    else:
        if text[start + size] == '.' and text[start + size - 1] in end_signs:
            text = text[start:start + size - 2]
            size -= 2
        else:
            text = text[start:start + size]
        for i in range(size - 1, 0, -1):
            if text[i] in end_signs:
                break
            counter = size - i
    page_text = text[:size - counter]
    page_size = size - counter
    return page_text, page_size

def prepare_ticket(path: str, page_size: int) -> dict:
    ticket = {}
    with open(path, 'r', encoding='utf-8') as file:
        obj = file.read()
        start, page = 0, 0
        while len(obj) > 0:
            text, lens = _get_part_text(start=start, size=page_size, text=obj)
            page += 1
            obj = obj[lens:]
            ticket[page] = text.lstrip()
    return ticket

class RabbitMQ:
    __HOST = 'amqp://guest:guest@localhost/'

    @classmethod
    async def send_message_spam_queue(cls, chat_id: int, message_id: int) -> None:
        connect = await aio_pika.connect(cls.__HOST)
        user_ids = Database.get_users_ids()
        async with connect:
            channel = await connect.channel()
            for user_id in user_ids:
                message = aio_pika.Message(
                    body=f'{user_id}:{chat_id}:{message_id}'.encode('ASCII')
                )
                await channel.default_exchange.publish(
                    message=message,
                    routing_key='spam_queue'
                )
        await connect.close()

class Tickets:
    _instance = None
    __PAGE_SIZE = 1050

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        self.tickets_ru: dict[str, dict[int, str]] = {}
        self.tickets_by: dict[str, dict[int, str]] = {}
        for ticket in range(1, 26):
            self.tickets_ru[f'ticket {ticket}'] = prepare_ticket(
                path=path_ticket_ru_txt[f'билет {ticket}'],
                page_size=self.__PAGE_SIZE
            )
            self.tickets_by[f'ticket {ticket}'] = prepare_ticket(
                path=path_ticket_by_txt[f'билет {ticket}'],
                page_size=self.__PAGE_SIZE
            )

    def get_ticket_page(self, ticket, page, user_language):
        return self.tickets_ru[f'ticket {ticket}'][page] if user_language == 'RU' else self.tickets_by[f'ticket {ticket}'][page]
    
    def get_count_pages_in_ticket(self, ticket, language):
        return len(self.tickets_ru[f'ticket {ticket}'].keys()) if language == 'RU' else len(self.tickets_by[f'ticket {ticket}'].keys())
    
class Tests:
    with open('tests/tests.json', 'r', encoding='U8') as file:
        __TESTS_RU = json.load(file)
    
    with open('tests/tests_by.json', 'r', encoding='U8') as file:
        __TESTS_BY = json.load(file)

    @classmethod
    def get_question(cls, test: int, question: int, mode: str) -> str:
        if mode == 'BY':
            return cls.__TESTS_BY[f'ticket {test}'][f'question {question}']
        elif mode == 'RU':
            return cls.__TESTS_RU[f'ticket {test}'][f'question {question}']
        else:
            raise AttributeError()

class Answers:
    with open('tests/answers.json', 'r', encoding='utf-8') as file:
        __ANSWERS_RU = json.load(file)

    with open('tests/answers_by.json', 'r', encoding='utf-8') as file:
        __ANSWERS_BY = json.load(file)

    @classmethod
    def get_answers(cls, ticket: int, question: int, mode: str) -> list:
        if mode == 'BY':
            return cls.__ANSWERS_BY[f'ticket {ticket}'][f'question {question}']
        elif mode == 'RU':
            return cls.__ANSWERS_RU[f'ticket {ticket}'][f'question {question}']
        else:
            raise AttributeError()

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
            language TEXT DEFAULT 'RU',
            test INTEGER,
            number_of_correct_answers INTEGER DEFAULT 0,
            page INTEGER DEFAULT 1,
            read_mode TEXT DEFAULT 'telegram',
            ticket INTEGER,
            PRIMARY KEY (user_id)
        )
        ''')
        cls.create_test_results_table(cls.__DATABASE)

    @classmethod
    def get_user_data(cls, user_id: int) -> tuple:
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT user_id, language, read_mode FROM users WHERE user_id = ?', (user_id,))
        return cursor.fetchall()[-1]
    
    @classmethod
    def user_knock_page(cls, user_id: int) -> None:
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('UPDATE users SET page = ? WHERE user_id = ?', (1, user_id))

    @classmethod
    def set_ticket_number(cls, user_id: int, ticket_number: int) -> None:
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('UPDATE users SET ticket = ? WHERE user_id = ?', (ticket_number, user_id))

    @classmethod
    def set_read_mode(cls, user_id: int, read_mode: str):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('UPDATE users SET read_mode = ? WHERE user_id = ?', (read_mode, user_id))

    @classmethod
    def get_user_ticket(cls, user_id: int) -> int:
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT ticket FROM users WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()[-1]
        return result

    @classmethod
    def get_user_settings(cls, user_id: int) -> dict:
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT language, read_mode FROM users WHERE user_id = ?', (user_id,))
            result = {i:j for i, j in zip(('language', 'read_mode'), cursor.fetchone())}
        return result

    @classmethod
    def get_the_number_of_users(cls):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT * FROM users')
            result = cursor.fetchall()
            return len(result)

    @classmethod
    def get_test_number(cls, user_id):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            return result[2]

    @classmethod
    def get_user_page(cls, user_id: int):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            return result[4]
        
    @classmethod
    def update_page(cls, user_id: int, new_page: int):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('UPDATE users SET page = ? WHERE user_id = ?', (new_page, user_id))
        
    @classmethod
    def update_test_result(cls, user_id: int, test_number: int, test_result: int):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute(f'UPDATE test_results SET test_{test_number} = ? WHERE user_id = ?', (test_result, user_id))
            
    @classmethod
    def get_test_results(cls, user_id: int):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute(f'SElECT * FROM test_results WHERE user_id = ?', (user_id,))
            return cursor.fetchone()

    @classmethod
    def set_user_id(cls, user_id: int):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            if not result:
                cursor.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
                cursor.execute('INSERT INTO test_results (user_id) VALUES (?)', (user_id,))
    
    @classmethod
    def set_ticket_language(cls, ticket_language: str, user_id: int):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('UPDATE users SET language = ? WHERE user_id = ?', (ticket_language, user_id))
        
    @classmethod
    def set_test_number(cls, test_number: int, user_id: int):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('UPDATE users SET test = ? WHERE user_id = ?', (test_number, user_id))
    
    @classmethod
    def get_test_number(cls, user_id: int):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT test FROM users WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            return result[-1]
        
    @classmethod
    def get_user_read_mode(cls, user_id: int):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT read_mode FROM users WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            return result[-1]
    
    @classmethod
    def get_user_language(cls, user_id: int):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            return result[-1]
    
    @classmethod
    def append_to_crrect_answers(cls, user_id: int):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            cursor.execute('UPDATE users SET number_of_correct_answers = ? WHERE user_id = ?', (result[3] + 1, user_id))

    @classmethod
    def recet_and_get_a_correct_answers(cls, user_id: int):
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
                           message_id INTEGER,
                           chat_id INTEGER,
                           PRIMARY KEY(admin_id)
            )''')

    @classmethod
    def add_admin(cls, admin_id: int):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT * FROM admins WHERE admin_id = ?', (admin_id,))
            result = cursor.fetchone()
            if not result:
                cursor.execute('INSERT INTO admins (admin_id) VALUES (?)', (admin_id,))

    @classmethod
    def set_message_id(cls, admin_id: int, message_id: int):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('UPDATE admins SET message_id = ? WHERE admin_id = ?', (message_id, admin_id))

    @classmethod
    def set_chat_id(cls, admin_id: int, chat_id: int):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('UPDATE admins SET chat_id = ? WHERE admin_id = ?', (chat_id, admin_id))

    @classmethod
    def get_message_id(cls, admin_id: int):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT message_id FROM admins WHERE admin_id = ?', (admin_id,))
            spam_text = cursor.fetchone()[0]
            return spam_text
        
    @classmethod
    def get_chat_id(cls, admin_id: int):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT chat_id FROM admins WHERE admin_id = ?', (admin_id,))
            chat_id = cursor.fetchone()[0]
            return chat_id
        
    @classmethod
    def clear_spam_settings(cls, admin_id: int) -> None:
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('DELETE FROM admins WHERE admin_id = ?', (admin_id,))

    @staticmethod
    def create_test_results_table(database):
        colum = [f'test_{index} INTEGER DEFAULT 0' for index in range(1, 26)]
        with sqlite3.connect(database) as connect:
            cursor = connect.cursor()
            request = 'CREATE TABLE IF NOT EXISTS test_results (user_id INTEGER, ' + ', '.join(colum) + ', FOREIGN KEY (user_id) REFERENCES users(user_id))'
            cursor.execute(request)

    @classmethod
    def get_users_ids(cls):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT * FROM users')
            return (i[0] for i in cursor.fetchall())

    @classmethod
    def is_there_any_data_in_line(cls):
        with sqlite3.connect(cls.__DATABASE) as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT COUNT(*) FROM users_queue')
            return True if cursor.fetchall() != [(0,)] else False


