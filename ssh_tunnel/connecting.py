import os
import asyncio
import asyncssh
import logging

logging.basicConfig(level=logging.INFO)

# Получаем параметры из окружения
IP_SERVER = os.getenv('IP_SERVER')
PORT_SSH = int(os.getenv('PORT_SSH', '22'))
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
LOCAL_PORT = int(os.getenv('LOCAL_PORT', '22'))
REMOTE_PORT = int(os.getenv('REMOTE_PORT', '80'))

async def forward_tunnel(local_port, remote_host, remote_port, ssh_host, ssh_port, ssh_user, ssh_password):
    async with asyncssh.connect(
            ssh_host, port=ssh_port, username=ssh_user, password=ssh_password
    ) as conn:
        # Создаём туннель
        forwarder = await conn.forward_local_port('', local_port, remote_host, remote_port)
        try:
            await forwarder.wait_closed()
        except Exception as e:
            logging.error(f"Error occurred in tunnel: {e}")

async def main():
    await forward_tunnel(
        LOCAL_PORT,  # Локальный порт
        '127.0.0.1', # Удалённый хост
        REMOTE_PORT, # Удалённый порт
        IP_SERVER,   # SSH сервер
        PORT_SSH,    # SSH порт
        USER,        # SSH пользователь
        PASSWORD     # SSH пароль
    )

if __name__ == '__main__':
    asyncio.run(main())