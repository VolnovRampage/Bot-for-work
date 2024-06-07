import asyncssh
import asyncio
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
IP_SERVER = os.getenv('IP_SERVER')
PORT_SSH = int(os.getenv('PORT_SSH'))  # Замените на ваш порт
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
# DESTINATIO = os.getenv('DESTINATIO')
# ARCHIVE_NAME = os.getenv('ARCHIVE_NAME')
# PATH = os.getenv('PATH')


async def connect_via_ssh():
    async with asyncssh.connect(host=IP_SERVER, port=PORT_SSH, username=USER) as conn:
        result = await conn.run('ls -ls')
        print(result)

asyncio.run(connect_via_ssh())
