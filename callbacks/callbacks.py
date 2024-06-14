import os
import time

from datetime import datetime
from aiogram import F, Router, types
from ssh_tunnel.connecting import connect_via_ssh, get_file_size

from keyboards.inline_keyboards import inline_kb
from logs.logs import write_log, read_log

ADMINS: list = [int(id) for id in os.getenv("ADMINS").split(",")]

callback_router = Router()


def get_date() -> str:
    return datetime.now().strftime("%H:%M:%S  |  %d/%m/%Y")


def make_text(spent_time: float, file_size: float, backup_date: str) -> str:
    text: str = (
        "<b>Backup выполнен:</b>\n"
        f"<i>  -  Затрачено времени:  {spent_time:.2f} минут.</i>\n"
        f"<i>  -  Передано по проводу:  {file_size:.3f} Гб.</i>\n"
        f"<i>  -  Время и дата:  {backup_date}.</i>"
    )
    return text


async def backup():
    start_time = time.time()
    result = await connect_via_ssh()
    backup_date = get_date()
    if not isinstance(result, str):
        spent_time = (time.time() - start_time) / 60
        file_size = get_file_size()
        text: str = make_text(spent_time=spent_time, file_size=file_size, backup_date=backup_date)
    else:
        text: str = f"{result}\n<b>Время и дата:</b>  {backup_date}"
    await write_log(text=text)
    return text



@callback_router.callback_query(F.data == "backup_sql")
async def backup_sql(call: types.CallbackQuery):
    if call.from_user.id in ADMINS:
        await call.message.edit_text(text="Начинается BackUp sql файлов")
        text = await backup()
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
