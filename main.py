import requests
import os
import sys
import subprocess
import shutil
import time

# Конфигурация
CURRENT_VERSION = "1.0.0"  # Текущая версия приложения
VERSION_URL = "https://raw.githubusercontent.com/yourusername/yourrepo/main/version.txt"  # URL файла с версией
UPDATE_URL = "https://raw.githubusercontent.com/yourusername/yourrepo/main/app_new.py"  # URL нового файла приложения
APP_NAME = "app.py"  # Имя текущего приложения
TEMP_NAME = "app_new.py"  # Временное имя загруженного файла

def check_version():
    """Проверяет, есть ли новая версия на сервере."""
    try:
        response = requests.get(VERSION_URL, timeout=5)
        response.raise_for_status()
        latest_version = response.text.strip()
        return latest_version > CURRENT_VERSION, latest_version
    except requests.RequestException as e:
        print(f"Ошибка проверки версии: {e}")
        return False, None

def download_update():
    """Загружает новую версию приложения."""
    try:
        response = requests.get(UPDATE_URL, timeout=10)
        response.raise_for_status()
        with open(TEMP_NAME, "wb") as f:
            f.write(response.content)
        print("Обновление загружено.")
        return True
    except requests.RequestException as e:
        print(f"Ошибка загрузки обновления: {e}")
        return False

def apply_update():
    """Заменяет старое приложение новым и перезапускает."""
    try:
        # Ждем, чтобы убедиться, что файл записан
        time.sleep(1)
        # Копируем новый файл поверх старого
        shutil.move(TEMP_NAME, APP_NAME)
        print("Обновление установлено.")
        # Перезапускаем приложение
        subprocess.Popen([sys.executable, APP_NAME])
        sys.exit(0)  # Завершаем текущее приложение
    except Exception as e:
        print(f"Ошибка установки обновления: {e}")

def main():
    print(f"Текущая версия: {CURRENT_VERSION}")
    has_update, latest_version = check_version()
    
    if has_update:
        print(f"Доступна новая версия: {latest_version}")
        if download_update():
            apply_update()
    else:
        print("Обновления не найдены.")
    
    # Здесь продолжается основная логика приложения
    print("Запуск основного приложения...")
    # Пример: ваш код приложения
    while True:
        print("Приложение работает. Нажмите Ctrl+C для выхода.")
        time.sleep(5)

if __name__ == "__main__":
    main()
