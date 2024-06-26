import asyncssh
import os
from datetime import datetime

from itertools import zip_longest
from data.load_data import (IP_SERVERS, PORTS_SSH, USERS, PASSWORDS, PATHS_TO_SOURCE,
                            PATH_TO_ARCHIVE, PATHS_TO_DESTINATION, ARCHIVE_NAMES, OPERATING_SYSTEM)
from logs.logs import make_text



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
    create_archive = f"7za a -tzip -mx1 {path_to_archive} {path_to_source}"
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


async def remove_archive(conn: asyncssh.SSHClientConnection,
                         path_to_archive: str,
                         operating_sys: str):
    command: str = 'del' if operating_sys == 'Windows' else 'rm'
    await conn.run(f"{command} {path_to_archive}")
    return True


def get_file_size(path_to_destination: str,
                  archive_name: str) -> float:
    file_size = os.path.getsize(os.path.join(path_to_destination, archive_name))
    file_size = file_size / (1024**3)
    return f'{file_size:.3f}'


def get_time(start: datetime):
    elapsed = datetime.now() - start
    hours, remainder = divmod(elapsed.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{int(hours):02}:{int(minutes):02}:{int(seconds):02}'



async def connect_via_ssh():
    result_connecting: list[str] = []
    async for data in merge_data():
        current_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        start = datetime.now()
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
                file_size = get_file_size(path_to_destination=data[7],
                                                 archive_name=data[6])
                spend_time = get_time(start=start)
        except asyncssh.PermissionDenied as err:
            text: str = 'Отсутствует разрешение'
            result = make_text(ip=data[0], text=text, err=err)
        except asyncssh.Error as err:
            text: str = 'Ошибка SSH:'
            result = make_text(ip=data[0], text=text, err=err)
        except Exception as err:
            text: str = 'Ошибка подключения'
            result = make_text(ip=data[0], text=text, err=err)
        else:
            result = make_text(ip=data[0],
                      current_time=current_time,
                      spent_time=spend_time,
                      file_size=file_size)
        result_connecting.append(result)
    return result_connecting
