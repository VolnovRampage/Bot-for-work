import os
import time

from datetime import datetime
from aiogram import F, Router, types
from ssh_tunnel.connecting import connect_via_ssh, get_file_size

from keyboards.inline_keyboards import inline_kb

ADMINS: list = [int(id) for id in os.getenv("ADMINS").split(",")]

callback_router = Router()


def get_date():
    return datetime.now().strftime("%H:%M:%S  |  %d/%m/%Y")


@callback_router.callback_query(F.data == "backup_sql")
async def backup(call: types.CallbackQuery):
    if call.from_user.id in ADMINS:
        initial_text = "Начинается BackUp sql файлов"
        if call.message.text != initial_text:
            await call.message.edit_text(text=initial_text)
        start_time = time.time()
        result = await connect_via_ssh()
        if result is True:
            spent_time = (time.time() - start_time) / 60
            current_date = get_date()
            file_size = get_file_size()
            await call.message.delete()
            text: str = "<b>BackUp выполнен.</b>\n" \
                f"<b>Затрачено времени:</b>  {spent_time:.2f} минут.\n" \
                f"<b>Передано по проводу:</b>  {file_size:.3f} Гб.\n" \
                f"<b>Время и дата:</b>  {current_date}."
            await call.message.answer(text=text, reply_markup=inline_kb.as_markup())
        else:
            current_date = get_date()
            await call.message.edit_text(
                text=f"{result}\n<b>Время и дата:</b>  {current_date}"
            )

    else:
        await call.message.edit_text("У вас нет прав на это")
