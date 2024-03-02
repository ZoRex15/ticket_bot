from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy import select, update ,and_, func
from .models import Base, User, TestResult, Admin
from typing import List, Tuple


class Database:
    __engine = create_async_engine(url='sqlite+aiosqlite:///database/database.db', echo=True)
    __async_session = async_sessionmaker(__engine, expire_on_commit=False)

    @classmethod
    async def create_tables(cls) -> None:
        async with cls.__engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @classmethod
    async def add_user(cls, user_id: int) -> None:
        async with cls.__async_session() as session:
            user = await session.get(User, user_id)
            if not user:
                user = User(
                    user_id=user_id
                )
                session.add(user)
                await session.commit()

    @classmethod
    async def add_admin(cls, admin_id: int) -> None:
        async with cls.__async_session() as session:
            admin = await session.get(Admin, admin_id)
            if not admin_id:
                admin = Admin(
                    admin_id=admin_id
                )
                session.add(admin)
                await session.commit()

    @classmethod
    async def get_user_data(cls, user_id: int) -> User:
        async with cls.__async_session() as session:
            user = await session.get(User, user_id)
            return user
        
    @classmethod
    async def get_admin_data(cls, admin_id: int) -> Admin:
        async with cls.__async_session() as session:
            admin = session.get(Admin, admin_id)
            return admin
        
    @classmethod
    async def get_test_result_page(cls, page: int, user_id: int) -> str:
        page_res = ''
        async with cls.__async_session() as session:
            for test_number in range(5 * (page - 1), 5 * page):
                test_result = await session.get(TestResult, (user_id, test_number + 1))
                page_res +=  f'📄Тест {test_number + 1}: 0/5\n' if test_result is None else f'📄Тест {test_number + 1}: {test_result.grade}/5\n'
        return page_res.strip()

    @classmethod
    async def update_user_data(cls, 
                               user_id: int,
                               test: int = None,
                               language: str = None,
                               number_of_correct_answers: int = None,
                               page: int = None,
                               read_mode: str = None,
                               ticket: int = None
                               ) -> User:
        new_data = {
            'test': test,
            'language': language,
            'number_of_correct_answers': number_of_correct_answers,
            'page': page,
            'read_mode': read_mode,
            'ticket': ticket
        }
        async with cls.__async_session() as session:
            user = await session.get(User, user_id)
            for key, value in {key: value for key, value in new_data.items() if value is not None}.items():
                setattr(user, key, value)
            await session.commit()
            return user

    @classmethod
    async def update_admin_data(cls, 
                                admin_id: int,
                                message_id: int = None,
                                chat_id: int = None
                                ) -> Admin:
        new_data = {
            'message_id': message_id,
            'chat_id': chat_id
        }
        async with cls.__async_session() as session:
            admin = await session.get(Admin, admin_id)
            for key, value in {key: value for key, value in new_data if value is not None}.items():
                setattr(admin, key, value)
            await session.commit()
        
            return admin
    

    @classmethod
    async def add_or_update_test_result(cls,
                                 user_id: int,
                                 test_number: int,
                                 grade: int) -> None:
        async with cls.__async_session() as session:
            test_result = TestResult(
                    user_id=user_id,
                    test_number=test_number,
                    grade=grade
                )
            await session.merge(test_result)
            # test_result = await session.get(TestResult, (user_id, test_number))
            # if not test_result:
            #     test_result = TestResult(
            #         user_id=user_id,
            #         test_number=test_number,
            #         grade=grade
            #     )
            #     session.add(test_result)
            # else:
            #     test_result.grade = grade
            
            await session.commit()

    @classmethod
    async def get_count_users(cls) -> int:
        async with cls.__async_session() as session:
            count = await session.execute(select(func.count(User.user_id)))
        return count.scalar()
    
    @classmethod
    async def get_user_ids(cls) -> list[Tuple[int]]:
        async with cls.__async_session() as session:
            user_ids = await session.execute(select(User.user_id))
        return user_ids.all()











