from aiogram.types import Message, PollAnswer
import sqlite3
import json
import aio_pika
from path.path import path_ticket_ru_txt, path_ticket_by_txt
from database.requests import Database
from database.models import User

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

def _create_text_menu(user: User, user_name: str) -> str:
    text_menu = f'''👤 Добро пожаловать, {user_name} 
├Ваш ID: {user.user_id}
├Язык: {('🇧🇾', '🇷🇺')[user.language == 'RU']}
├Режим чтения: {("✈️", "💾")[user.read_mode == "file"]}'''
    return text_menu

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
        user_ids = await Database.get_user_ids()
        async with connect:
            channel = await connect.channel()
            for user_id in user_ids:
                message = aio_pika.Message(
                    body=f'{user_id[0]}:{chat_id}:{message_id}'.encode('ASCII')
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