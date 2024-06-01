import os

from aiogram import F, Router, types


ADMINS: list = [int(id) for id in os.getenv("ADMINS").split(",")]

callback_router = Router()


@callback_router.callback_query(F.data == 'backup_sql')
async def backup(call: types.CallbackQuery):
    if call.from_user.id in ADMINS:
        await call.message.edit_text('Начался backup файлов')
    else:
        await call.message.edit_text('У вас нет прав на это')
