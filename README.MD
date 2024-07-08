# Telegram bot для backup по SSH

Bot создает защищённое подключение по SSH с серверами находящимися в одной локальной сети, архивирует критично важные данные для дальнейшей передаче.

# Перечень файлов

## Исходные файлы

- `TelegramBot_SSH_BackUp/main.py` - точка входа в бота.

- `TelegramBot_SSH_BackUp/callbacks/callbacks.py` - Обработчики inline кнопок.

- `TelegramBot_SSH_BackUp/data/data.example.json` - Пример файла с конфигурациями для подключения по SSH.

- `TelegramBot_SSH_BackUp/data/load_data.py` - Файл с подгруженными переменными для бота.

- `TelegramBot_SSH_BackUp/handlers/private_chat.py` - Список команд, которые отлавливает бот в чате.

- `TelegramBot_SSH_BackUp/keyboards/inline_keyboards.py` - Inline клавиатуры.

- `TelegramBot_SSH_BackUp/logs/logs.py` - Чтение и запись в файл текстовой информации о подключении и backup через ssh.

- `TelegramBot_SSH_BackUp/logs/backup_log.txt` - Текстовый файл для записи результатов последнего backup.

- `TelegramBot_SSH_BackUp/ssh_tunnel/connecting.py` - Подключение по ssh, создание архива с дальнейшей передачей на сервер, на котором запущен бот, удаление архива с удаленного сервера.

- `TelegramBot_SSH_BackUp/.gitignore` - Список папок и файлов, которые не должны попасть в GitHub.

- `TelegramBot_SSH_BackUp/README.md` - Руководство.

- `TelegramBot_SSH_BackUp/requirements.txt` - Список зависимотей приложения.

- `TelegramBot_SSH_BackUp/start.sh` - Скрипт запуска бота.

## Скрипты

- `start.bash` — Bash-скрипт, который делает следующее:
    - Обнавляет Ubuntu
    - Устанавливает python и его модуль для создания виртуального окружения
    - Создает виртуальное окружение
    - Активирует созданное виртуальное окружение
    - Устанавливает все зависимости из файла `requirements.txt`
    - Запускает файл main.py.

# Инсталляция

## Системные требования

1. OS Linux Ubuntu.
2. [Python](https://www.python.org/downloads/release/python-3123/) версии >= 3.12.
3. Система контроля версий [Git](https://git-scm.com/).
4. [Ngrok](https://ngrok.com/download/). Для запуска бота необходимо:
    - Скачать и установить утилиту с официального сайта
    - Зарегистрироваться на сайте
    - Получить token
    - Скопировать команду и вставить в терминал.
5. OpenSSH server для удаленного компьютера
7. [7Zip](https://www.7-zip.org/download.html) standalone console version:
    - Скачать 7Zip.
    - Разархивировать в `C:\Program files\7zip`
    - Добавить путь к 7za `C:\Program files\7zip` в Path


# Использование

1. Клонируйте репозиторий на Ubuntu командой `git clone https://github.com/VolnovRampage/TelegramBot_SSH_BackUp.git`.

2. Перейдите в папку `./TelegramBot_SSH_BackUp/data/`.

3. Создайте файл `data.json`.

4. Скопируйте все из файла `data.example.json` и вставьте в `data.json`.

5. Запустите Ngrok командой `ngrok http 2250`.

6. Скопируйте URI предоставленный Ngrok.

7. Вставьте URL в файл `data.json`.

8. Создайте bot в телеграм канале [BotFather](https://t.me/botfather/).

9. Скопируйте ссылку на вашего бота, предоставленную [BotFather](https://t.me/botfather/).

10. Вставьте ссылку в файл `data.json`.

11. Замените все остальные данные под ваши требования в данном файле. Данные необходимо вносить в блок SSH через запятую.

12. Находясь в папке `./TelegramBot_SSH_BackUp`, введите `bash start.bash`.

13. Введите пароль от учетной записи.

14. Бот запущен.

# Автор

Автор: Вольнов Артур.

# Связь

Замечания и предложения можно присылать на адрес @VolnovRampage.
