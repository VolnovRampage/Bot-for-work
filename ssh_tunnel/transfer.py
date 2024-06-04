import asyncssh


async def transfer_file(conn, local_path, remote_path):
    try:
        async with conn.start_sftp_client() as sftp:
            await sftp.put(local_path, remote_path)
            return True
    except (OSError, asyncssh.Error) as exc:
        return f'Ошибка передачи файла: {exc}'