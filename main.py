from config.config import Config, load_config
import asyncio
from aiogram import Bot, Dispatcher
from handlers import *
from aiogram.fsm.storage.redis import Redis, RedisStorage
from keyboards.set_menu import set_menu
from database.requests import Database


async def main():
    await Database.create_tables()
    config: Config = load_config() 
    bot: Bot = Bot(config.tg_bot.token, parse_mode='HTML')
    redis: Redis = Redis(host='localhost')
    storage: RedisStorage = RedisStorage(redis=redis)
    dp: Dispatcher = Dispatcher(storage=storage)
    dp.include_routers(
                        user_message.router,
                        user_poll.router, 
                        user_callback.router,
                        user_commands.router
                        )
    dp.include_routers(
                        admin_message.router,
                        admin_callback.router,
                        admin_commands.router
                        )
    await set_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())
