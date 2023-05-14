from aiogram import Router, types
from aiogram.types import FSInputFile
from ticket_bot import Bot
from path import ticket_bel_dict, ticket_dict


router: Router = Router()



@router.message()
async def ticket(message: types.Message):
    if str(message.text).lower() in ticket_dict:
        media = FSInputFile(path=ticket_dict[message.text.lower()])
        await message.answer_document(document=media)
    else:
        if str(message.text).lower() in ticket_bel_dict:
            media = FSInputFile(path=ticket_bel_dict[message.text.lower()])
            await message.answer_document(document=media)