from aiogram.types import BotCommand
from aiogram import Bot
from lexicon.lexicon import COMMANDS

async def set_menu(bot: Bot):
    menu: list = [BotCommand(
        command=command,
        description=description)
        for command, description in COMMANDS.items()
    ]
    await bot.set_my_commands(menu)