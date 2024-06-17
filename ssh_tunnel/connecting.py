import asyncssh
import os


# Получение значений переменных окружения
IP_SERVER: str = os.getenv("IP_SERVER")
PORT_SSH: int = int(os.getenv("PORT_SSH"))
USER: str = os.getenv("USERNAME_FROM_SERVER")
PASSWORD: str = os.getenv("PASSWORD")
PATH_TO_SOURCE: str = os.getenv("PATH_TO_SOURCE")
PATH_TO_ARCHIVE: str = os.getenv("PATH_TO_ARCHIVE")
PATH_TO_DESTINATION: str = os.getenv("PATH_TO_DESTINATION")
ARCHIVE_NAME: str = os.path.basename(PATH_TO_ARCHIVE.replace("\\", "/"))


async def create_archive(conn: asyncssh.SSHClientConnection):
    create_archive = f"7z a -tzip -mx1 {PATH_TO_ARCHIVE} {PATH_TO_SOURCE}"
    await conn.run(create_archive, check=True)
    return conn


async def send_archive(conn: asyncssh.SSHClientConnection):
    async with conn.start_sftp_client() as sftp:
        remote_path = PATH_TO_ARCHIVE.replace("\\", "/")
        local_path = os.path.join(PATH_TO_DESTINATION, ARCHIVE_NAME)
        await sftp.get(remote_path, local_path)


def get_file_size() -> float:
    file_size = os.path.getsize(
        os.path.join(PATH_TO_DESTINATION, ARCHIVE_NAME)
    )
    return file_size / (1024**3)


async def remove_archive(conn: asyncssh.SSHClientConnection):
    await conn.run(f"del {PATH_TO_ARCHIVE}")
    return True


async def connect_via_ssh():
    try:
        async with asyncssh.connect(
            host=IP_SERVER, port=PORT_SSH, username=USER, password=PASSWORD
        ) as conn:
            await create_archive(conn=conn)
            await send_archive(conn=conn)
            await remove_archive(conn=conn)
            return True
    except asyncssh.PermissionDenied:
        return "<b>Permission denied:</b>\n<i>Проверьте правильность имени пользователя и пароля</i>"
    except asyncssh.Error as e:
        return f"<b>Ошибка SSH:</b>\n<i>{e}</i>"
    except Exception as e:
        return f"<b>Ошибка подключения:</b>\n<i>{e}</i>"
