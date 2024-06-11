import os
import time

from datetime import datetime
from aiogram import F, Router, types
from ssh_tunnel.connecting import connect_via_ssh, measurement_file




ADMINS: list = [int(id) for id in os.getenv("ADMINS").split(",")]

callback_router = Router()


def get_date():
    return datetime.now().strftime("%H:%M:%S  |  %d/%m/%Y")


@callback_router.callback_query(F.data == 'backup_sql')
async def backup(call: types.CallbackQuery):
    if call.from_user.id in ADMINS:
        await call.message.edit_text(text='Запускаю BackUp')
        start_time = time.time()
        result = await connect_via_ssh()
        if result is True:
            spent_time = (time.time() - start_time) / 100
            current_date = get_date()
            file_size = measurement_file()
            await call.message.edit_text(
                text='<b>BackUp выполнен.</b>\n' \
                    f'<b>Затрачено времени:</b>  {spent_time:.2f} минут.\n' \
                    f'<b>Передано по проводу:</b>  {file_size:.2f} Гб.\n' \
                    f'<b>Время и дата:</b>  {current_date}.'
            )
        else:
            current_date = get_date()
            await call.message.edit_text(text=f'{result}\n<b>Время и дата:</b>  {current_date}')

    else:
        await call.message.edit_text('У вас нет прав на это')
