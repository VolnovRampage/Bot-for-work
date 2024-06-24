import asyncssh
import os
import asyncio

from itertools import zip_longest
from load_data import (IP_SERVERS, PORTS_SSH, USERS, PASSWORDS,
                       PATHS_TO_SOURCE, PATHS_TO_DESTINATION, ARCHIVE_NAMES)



async def merge_data():
    for ip, port, user, password, path_source, archive_name, path_dest in zip_longest(
        IP_SERVERS, PORTS_SSH, USERS, PASSWORDS, PATHS_TO_SOURCE,
        ARCHIVE_NAMES, PATHS_TO_DESTINATION, fillvalue=None
    ):
        yield ip, port, user, password, path_source, archive_name, path_dest


def get_path_to_archive(path_to_source: str, archive_name: str):
    return os.path.join(os.path.dirname(path_to_source), archive_name)


async def create_archive(conn: asyncssh.SSHClientConnection, path_to_source: str, archive_name: str):
    path_to_archive: str = get_path_to_archive(path_to_source=path_to_source, archive_name=archive_name)
    print(path_to_archive)
    create_archive = f"7z a -tzip -mx1 {path_to_archive} {path_to_source}"
    await conn.run(create_archive, check=True)
    return conn


async def send_archive(conn: asyncssh.SSHClientConnection, path_to_source, path_to_destination: str, archive_name: str):
    async with conn.start_sftp_client() as sftp:
        remote_path = get_path_to_archive(
            path_to_source=path_to_source, archive_name=archive_name
        ).replace("\\", "/")
        local_path = os.path.join(path_to_destination, archive_name)
        await sftp.get(remote_path, local_path)


def get_file_size() -> float:
    file_size = os.path.getsize(
        os.path.join(PATH_TO_DESTINATION, ARCHIVE_NAME)
    )
    return file_size / (1024**3)


async def remove_archive(conn: asyncssh.SSHClientConnection, path_to_source: str, archive_name: str):
    path_to_archive: str = get_path_to_archive(path_to_source=path_to_source, archive_name=archive_name)
    await conn.run(f"del {path_to_archive}")
    return True


async def connect_via_ssh():
    async for data in merge_data():
        try:
            async with asyncssh.connect(
                host=data[0], port=data[1], username=data[2], password=data[3]
            ) as conn:
                await create_archive(conn=conn, path_to_source=data[4], archive_name=data[5])
                await send_archive(conn=conn, path_to_source=data[4], path_to_destination=data[6], archive_name=data[5])
                await remove_archive(conn=conn, path_to_source=data[4], archive_name=data[5])
                return True
        except asyncssh.PermissionDenied:
            print("<b>Permission denied:</b>\n<i>Проверьте правильность имени пользователя и пароля</i>")
        except asyncssh.Error as e:
            print(f"<b>Ошибка SSH:</b>\n<i>{e}</i>")
        except Exception as e:
            print(f"<b>Ошибка подключения:</b>\n<i>{e}</i>")


if __name__ == "__main__":
    asyncio.run(connect_via_ssh())
