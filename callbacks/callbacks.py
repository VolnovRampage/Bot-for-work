import os

from aiogram import F, Router, types
from archiving.archiving import create_archive
from ssh_tunnel.connecting import connect_ssh



ADMINS: list = [int(id) for id in os.getenv("ADMINS").split(",")]

callback_router = Router()


@callback_router.callback_query(F.data == 'backup_sql')
async def backup(call: types.CallbackQuery):
    if call.from_user.id in ADMINS:
        await call.message.edit_text('Начинаю архивировать папку.')
        await create_archive()
        await call.message.edit_text('Архивация закончена.\nОтправляю архив на сервер.')
        sending: str | bool = await connect_ssh()
        if not isinstance(sending, str):
            await call.message.edit_text('Файл успешно отправлен')
        else:
            await call.message.edit_text(text=sending)
    else:
        await call.message.edit_text('У вас нет прав на это')
