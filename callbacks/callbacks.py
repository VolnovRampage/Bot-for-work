import os

from aiogram import F, Router, types
from archiving.archiving import create_archive, extract_archive, delete_archive


ADMINS: list = [int(id) for id in os.getenv("ADMINS").split(",")]

callback_router = Router()


@callback_router.callback_query(F.data == 'backup_sql')
async def backup(call: types.CallbackQuery):
    if call.from_user.id in ADMINS:
        await call.message.edit_text('Начинаю архивацию файлов')
        await create_archive()
        await call.message.edit_text('Архивация закончена')
        await extract_archive()
        await call.message.edit_text('Распаковка закончена')
        await delete_archive()
    else:
        await call.message.edit_text('У вас нет прав на это')
