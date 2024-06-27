import asyncio
from aiogram import F, Router, types
from ssh_tunnel.connecting import connect_via_ssh

from keyboards.inline_keyboards import inline_kb
from logs.logs import write_log, read_log

from data.load_data import ADMINS


callback_router = Router()
backup_lock: bool = False


async def backup():
    if not backup_lock:
        set_backup_lock()
        result = await connect_via_ssh()
        mode: str = ''
        for index, text in enumerate(result):
            if index == 0:
                mode = 'w'
            else:
                mode = 'a'
            await write_log(text=text, mode=mode)
        set_backup_lock()
        return result


def set_backup_lock():
    global backup_lock
    if backup_lock:
        backup_lock = False
    else:
        backup_lock = True


async def start_backup(call: types.CallbackQuery):
    if backup_lock:
        await call.message.edit_text("Backup уже запущен ⚠️")
    else:
        await call.message.edit_text(text="Начинается BackUp sql файлов 🔄")
        try:
            text = await backup()
            text = '\n'.join(text)
            await call.message.edit_text(text=text, reply_markup=inline_kb.as_markup())
        except Exception as e:
            await call.message.edit_text(text=f"Ошибка во время backup: {e}")


@callback_router.callback_query(F.data == "backup_sql")
async def backup_sql(call: types.CallbackQuery):
    if call.from_user.id in ADMINS:
        asyncio.create_task(start_backup(call))
    else:
        await call.message.edit_text("У вас нет прав на это ⛔️")


@callback_router.callback_query(F.data == "info")
async def view_info(call: types.CallbackQuery):
    if call.from_user.id in ADMINS:
        await call.message.edit_text(text='Ищю информацию о последнем backup.')
        text = await read_log()
        await call.message.edit_text(text=text, reply_markup=inline_kb.as_markup())
    else:
        await call.message.edit_text("У вас нет прав на это.")
