from aiogram import types, Router, F
from aiogram.filters import CommandStart

from keyboards.inline_keyboards import inline_kb


private_chat_router: Router = Router()


@private_chat_router.message(CommandStart)
async def start_command(message: types.Message):
    await message.answer(text='Вот для создания BackUp sql файлов', reply_markup=inline_kb.as_markup())
