import asyncio
from aiogram import Bot, Dispatcher
from config import load_config, Config
from handlers import command_handlers, other_handlers

async def main():
    config: Config = load_config()
    bot: Bot = Bot(config.tg_bot.token)
    dp: Dispatcher = Dispatcher()
    dp.include_router(command_handlers.router)
    dp.include_router(other_handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
