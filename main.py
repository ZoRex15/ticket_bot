from config.config import Config, load_config
import asyncio
from aiogram import Bot, Dispatcher
from handlers import user_handlers, test_handlers
from aiogram.fsm.storage.redis import Redis, RedisStorage
from keyboards.set_menu import set_menu

async def main():
    config: Config = load_config() 
    bot: Bot = Bot(config.tg_bot.token, parse_mode='HTML')
    redis: Redis = Redis(host='localhost')
    storage: RedisStorage = RedisStorage(redis=redis)
    dp: Dispatcher = Dispatcher(storage=storage)
    dp.include_router(user_handlers.router)
    dp.include_router(test_handlers.router)
    await set_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
