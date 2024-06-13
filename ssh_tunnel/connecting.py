import asyncssh
import os
import asyncio
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
# Получение значений переменных окружения
IP_SERVER = os.getenv("IP_SERVER")
PORT_SSH = os.getenv("PORT_SSH")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
PATH_TO_SOURCE = os.getenv("PATH_TO_SOURCE")
PATH_TO_ARCHIVE = os.getenv("PATH_TO_ARCHIVE")
PATH_TO_DESTINATION = os.getenv("PATH_TO_DESTINATION")


async def create_archive(conn: asyncssh.SSHClientConnection):
    create_archive = f"7z a {PATH_TO_ARCHIVE} {PATH_TO_SOURCE}"
    await conn.run(create_archive, check=True)
    return conn


async def send_archive(conn: asyncssh.SSHClientConnection):
    async with conn.start_sftp_client() as sftp:
        remote_path = PATH_TO_ARCHIVE.replace("\\", "/")
        local_path = os.path.join(
            PATH_TO_DESTINATION, os.path.basename(PATH_TO_ARCHIVE)
        ).replace("\\", "/")
        await sftp.get(remote_path, local_path)


def get_file_size():
    file_size = os.path.getsize(
        os.path.join(PATH_TO_DESTINATION, os.path.basename(PATH_TO_ARCHIVE))
    )
    return file_size / (1024**3)


async def remove_archive(conn: asyncssh.SSHClientConnection):
    await conn.run(f"del {PATH_TO_ARCHIVE}")
    return True


async def connect_via_ssh():
    try:
        async with asyncssh.connect(
            host=IP_SERVER, port=int(PORT_SSH), username=USER, password=PASSWORD
        ) as conn:
            await create_archive(conn=conn)
            await send_archive(conn=conn)
            await remove_archive(conn=conn)
            return True
    except asyncssh.PermissionDenied:
        return "<b>Permission denied:</b> Проверьте правильность имени пользователя и пароля"
    except asyncssh.Error as e:
        return f"<b>Ошибка SSH:</b> {e}"
    except Exception as e:
        return f"<b>Ошибка подключения:</b> {e}"


asyncio.run(connect_via_ssh())
