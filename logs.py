import json
import aiofiles


async def write_log(spent_time, file_size, current_date):
    log_filename = "backup_logs.json"
    log_entry = {
        "backup_time": current_date,
        "spent_time_minutes": f"{spent_time:.2f}",
        "transferred_data_gb": f"{file_size:.3f}",
    }

    try:
        async with aiofiles.open(log_filename, mode="a") as log_file:
            await log_file.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"Ошибка при записи в лог: {e}")


async def read_log():
    log_filename = "backup_logs.json"
    logs = []

    try:
        async with aiofiles.open(log_filename, mode="r") as log_file:
            async for line in log_file:
                logs.append(json.loads(line.strip()))
    except Exception as e:
        return f"Ошибка при чтении логов: {e}"

    return logs[-5:]
