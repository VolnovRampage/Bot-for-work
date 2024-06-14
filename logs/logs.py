import aiofiles
import os


LOG_PATH = os.path.join(os.path.join(os.getcwd(), "logs"), "backup_log.txt")


async def write_log(text:str):
    async with aiofiles.open(LOG_PATH, mode="w", encoding='utf-8') as log_file:
        await log_file.write(text)


async def read_log():
    if os.path.exists(LOG_PATH):
        async with aiofiles.open(LOG_PATH, mode="r", encoding='utf-8') as log_file:
            log = await log_file.readlines()
        text: str = ''
        for line in log:
            text += line
        return text
    else:
        return f"Нет записей в логе."
