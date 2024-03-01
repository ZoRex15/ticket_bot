from sqlalchemy import String, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, declared_attr
from typing import List


class Base(DeclarativeBase, AsyncAttrs):
    ...

class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True)
    language: Mapped[str] = mapped_column(default='RU')
    test: Mapped[int] = mapped_column(nullable=True)
    number_of_correct_answers: Mapped[int] = mapped_column(default=0)
    page: Mapped[int] = mapped_column(default=1)
    read_mode: Mapped[str] = mapped_column(default='telegram')
    ticket: Mapped[int] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f'''User(user_id: {self.user_id!r}, language: {self.language!r}, test: {self.test!r}, 
        number_of_correct_answers: {self.number_of_correct_answers!r}, page: {self.page!r},
        read_mode: {self.read_mode!r}, ticket: {self.ticket!r})'''
    
class TestResult(Base):
    __tablename__ = 'test_results'
    
    user_id: Mapped[int] = mapped_column(primary_key=True)
    test_number: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    grade: Mapped[int] = mapped_column(nullable=False)

    
    def __repr__(self) -> str:
        return f'TestResult(user_id: {self.user_id!r}, test_number: {self.test_number!r}, grade: {self.grade!r})'

class Admin(Base):
    __tablename__ = 'admins'

    admin_id: Mapped[int] = mapped_column(primary_key=True)
    message_id: Mapped[int] = mapped_column(nullable=False)
    chat_id: Mapped[int] = mapped_column(nullable=False)

    def __repr__(self):
        return f'Admin(admin_id: {self.admin_id!r}, message_id: {self.message_id!r}, chat_id: {self.chat_id!r})'