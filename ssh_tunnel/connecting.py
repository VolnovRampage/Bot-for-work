import asyncssh
import asyncio
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
# Получение значений переменных окружения
IP_SERVER = os.getenv('IP_SERVER')
PORT_SSH = os.getenv('PORT_SSH')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')

# Отладочная печать переменных окружения
print(f"IP_SERVER: {IP_SERVER}")
print(f"PORT_SSH: {PORT_SSH}")
print(f"USER: {USER}")
print(f"PASSWORD: {PASSWORD}")

async def connect_via_ssh():
    try:
        print("Попытка подключения к серверу...")
        async with asyncssh.connect(host=IP_SERVER, port=int(PORT_SSH), username=USER, password=PASSWORD) as conn:
            print("Подключение успешно. Выполнение команды...")

            # Команда для создания папки на рабочем столе Windows
            create_folder_command = r'mkdir "c:\Users\karpovicha\Desktop\TEST"'  # Используем сырые строки (raw strings), чтобы избежать экранирования обратных слешей

            # Выполнение команды для создания папки
            result = await conn.run(create_folder_command, check=True)
            print("Команда выполнена успешно. Результат:")
            print(result.stdout)
    except asyncssh.PermissionDenied:
        print("Permission denied: Проверьте правильность имени пользователя и пароля")
    except asyncssh.Error as e:
        print(f"Ошибка SSH: {e}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")

asyncio.run(connect_via_ssh())
