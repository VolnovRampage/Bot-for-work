import asyncssh
import os

from .transfer import transfer_file
from archiving.archiving import path_to_zip


IP_SERVER = os.getenv('IP_SERVER')
PORT_SSH = int(os.getenv('PORT_SSH'))  # Замените на ваш порт
USER = os.getenv('USER')
REMOTE_PATH: str = '/home/expert/Desktop/'


async def connect_ssh():
    try:
        # Подключение к серверу
        async with asyncssh.connect(host=IP_SERVER, port=PORT_SSH, username=USER) as conn:
            await transfer_file(conn=conn, local_path=path_to_zip, remote_path=REMOTE_PATH)
            return True
    except (OSError, asyncssh.Error) as exc:
        return f'Ошибка подключения: {exc}'
