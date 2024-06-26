import time


from datetime import datetime
from aiogram import F, Router, types
from ssh_tunnel.connecting import connect_via_ssh, get_file_size

from keyboards.inline_keyboards import inline_kb
from logs.logs import write_log, read_log

from data.load_data import ADMINS


callback_router = Router()


async def backup():
    result = await connect_via_ssh()
    mode: str = ''
    for index, text in enumerate(result):
        if index == 0:
            mode = 'w'
        else:
            mode = 'a'
        await write_log(text=text, mode=mode)
    return result


@callback_router.callback_query(F.data == "backup_sql")
async def backup_sql(call: types.CallbackQuery):
    if call.from_user.id in ADMINS:
        await call.message.edit_text(text="Начинается BackUp sql файлов")
        text = await backup()
        text = '\n'.join(text)
        await call.message.edit_text(text=text, reply_markup=inline_kb.as_markup())
    else:
        await call.message.edit_text("У вас нет прав на это.")


@callback_router.callback_query(F.data == "info")
async def view_info(call: types.CallbackQuery):
    if call.from_user.id in ADMINS:
        await call.message.edit_text(text='Ищю информацию о последнем backup.')
        text = await read_log()
        await call.message.edit_text(text=text, reply_markup=inline_kb.as_markup())
    else:
        await call.message.edit_text("У вас нет прав на это.")
