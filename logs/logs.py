import aiofiles
import os


LOG_PATH = os.path.join(os.path.join(os.getcwd(), "logs"), "backup_log.txt")


async def write_log(text: str, mode: str):
    async with aiofiles.open(LOG_PATH, mode=mode, encoding='utf-8') as log_file:
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
        return f"<b>Нет записей в логе.</b>"


def make_text(ip=None, current_time=None, spent_time=None,
              file_size=None, text=None, err=None):
    if not err:
        text = f"<b>IP:</b> {ip}\n" \
                    f"<b>Время:</b> {current_time}\n" \
                    f"<b>Время затраченное на копирование:</b> {spent_time}\n" \
                    f"<b>Размер файла:</b> {file_size} Gb\n"
        return text
    text =  f"<b>IP:</b>  {ip}\n" \
                 f"<b>{text}:</b> {err}\n"
    return text
