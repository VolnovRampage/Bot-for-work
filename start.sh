#!/bin/bash

# Переменные
VENV="./venv"
REQUIREMENTS_FILE="./requirements.txt"

# Создание виртуального окружения, если оно не существует
if [ ! -d "$VENV" ]; then
    python3 -m venv "$VENV"
fi

# Активация виртуального окружения
source "$VENV/bin/activate"

# Установка зависимостей из requirements.txt
pip install -r "$REQUIREMENTS_FILE"

# Запуск main.py
python3 -u ./main.py
