import asyncssh
import os
import asyncio

from itertools import zip_longest
from data.load_data import (IP_SERVERS, PORTS_SSH, USERS, PASSWORDS, PATHS_TO_SOURCE,
                            PATH_TO_ARCHIVE, PATHS_TO_DESTINATION, ARCHIVE_NAMES, OPERATING_SYSTEM)



async def merge_data():
    for (ip, port, user, password, path_source, path_to_archive,
        archive_name, path_dest, operating_sys) in zip_longest(
        IP_SERVERS, PORTS_SSH, USERS, PASSWORDS, PATHS_TO_SOURCE,
        PATH_TO_ARCHIVE, ARCHIVE_NAMES, PATHS_TO_DESTINATION, OPERATING_SYSTEM, fillvalue=None
    ):
        yield (ip, port, user, password, path_source, path_to_archive,
               archive_name, path_dest, operating_sys)


async def create_archive(conn: asyncssh.SSHClientConnection,
                         path_to_source: str,
                         path_to_archive: str):
    create_archive = f"7z a -tzip -mx1 {path_to_archive} {path_to_source}"
    await conn.run(create_archive, check=True)
    return conn


async def send_archive(conn: asyncssh.SSHClientConnection,
                       path_to_archive: str,
                       path_to_destination: str,
                       archive_name: str):
    async with conn.start_sftp_client() as sftp:
        remote_path = path_to_archive.replace("\\", "/")
        local_path = os.path.join(path_to_destination, archive_name)
        await sftp.get(remote_path, local_path)


# def get_file_size() -> float:
#     file_size = os.path.getsize(
#         os.path.join(PATH_TO_DESTINATION, ARCHIVE_NAME)
#     )
#     return file_size / (1024**3)


async def remove_archive(conn: asyncssh.SSHClientConnection,
                         path_to_archive: str,
                         operating_sys: str):
    command: str = 'del' if operating_sys == 'Windows' else 'rm'
    await conn.run(f"{command} {path_to_archive}")
    return True


async def connect_via_ssh():
    async for data in merge_data():
        try:
            async with asyncssh.connect(
                host=data[0], port=data[1], username=data[2], password=data[3]
            ) as conn:
                await create_archive(conn=conn,
                                     path_to_source=data[4],
                                     path_to_archive=data[5])
                await send_archive(conn=conn,
                                   path_to_archive=data[5],
                                   path_to_destination=data[7],
                                   archive_name=data[6])
                await remove_archive(conn=conn,
                                     path_to_archive=data[5],
                                     operating_sys=data[8])
                # return True
        except asyncssh.PermissionDenied:
            print("<b>Permission denied:</b>\n<i>Проверьте правильность имени пользователя и пароля</i>")
        except asyncssh.Error as e:
            print(f"<b>Ошибка SSH:</b>\n<i>{e}</i>")
        except Exception as e:
            print(f"<b>Ошибка подключения:</b>\n<i>{e}</i>")
