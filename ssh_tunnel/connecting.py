import asyncssh
import os


IP_SERVER = os.getenv('IP_SERVER')
PORT_SSH = int(os.getenv('PORT_SSH'))  # Замените на ваш порт
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DISK = os.getenv('DISK')
ARCHIVE_NAME = os.getenv('ARCHIVE_NAME')
PATH = os.getenv('PATH')


async def connect_ssh():
    try:
        async with asyncssh.connect(host=IP_SERVER, port=PORT_SSH, username=USER, password=PASSWORD) as conn:
            result = await conn.run(f'{DISK}', check=True)
            print(result)
            result = await conn.run(f'7z a {ARCHIVE_NAME} {PATH}', check=True)
            print(result)
    except (OSError, asyncssh.Error) as exc:
        return f'Ошибка подключения: {exc}'
