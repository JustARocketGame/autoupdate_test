import tkinter as tk
from tkinter import messagebox
import requests
import os
import sys
import subprocess
import shutil
import time
import threading
import logging

# Настройка логирования
logging.basicConfig(filename="app.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Конфигурация
CURRENT_VERSION = "1.0.5"  # Текущая версия приложения
VERSION_URL = "https://raw.githubusercontent.com/JustARocketGame/autoupdate_test/main/version.txt"  # URL файла с версией
UPDATE_URL = "https://raw.githubusercontent.com/JustARocketGame/autoupdate_test/main/main.py"  # URL нового файла
APP_NAME = "main.py"  # Имя текущего приложения
TEMP_NAME = "main_new.py"  # Временное имя загруженного файла

class UpdateWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Проверка обновлений")
        self.root.geometry("300x100")
        self.root.resizable(False, False)

        # Центрируем окно
        self.root.eval('tk::PlaceWindow . center')

        self.label = tk.Label(root, text="Проверка на обновления...", font=("Arial", 14))
        self.label.pack(pady=30)

        logging.info("Запуск проверки обновлений")
        # Запускаем проверку обновлений в отдельном потоке
        threading.Thread(target=self.check_for_update, daemon=True).start()

    def check_for_update(self):
        """Проверяет наличие обновлений."""
        try:
            logging.info(f"Проверка версии по URL: {VERSION_URL}")
            response = requests.get(VERSION_URL, timeout=5)
            response.raise_for_status()
            latest_version = response.text.strip()
            has_update = latest_version > CURRENT_VERSION
            logging.info(f"Текущая версия: {CURRENT_VERSION}, последняя версия: {latest_version}, обновление: {has_update}")

            if has_update:
                self.label.config(text="Обновление...")
                self.root.update()
                if self.download_update():
                    self.apply_update()
                else:
                    logging.error("Не удалось загрузить обновление")
                    messagebox.showerror("Ошибка", "Не удалось загрузить обновление.")
                    self.open_main_menu()
            else:
                logging.info("Обновления не найдены")
                self.open_main_menu()
        except requests.RequestException as e:
            logging.error(f"Ошибка проверки обновлений: {e}")
            messagebox.showerror("Ошибка", f"Ошибка проверки обновлений: {e}")
            self.open_main_menu()

    def download_update(self):
        """Загружает новую версию приложения."""
        try:
            logging.info(f"Загрузка обновления с {UPDATE_URL}")
            response = requests.get(UPDATE_URL, timeout=10)
            response.raise_for_status()
            with open(TEMP_NAME, "wb") as f:
                f.write(response.content)
            logging.info(f"Обновление загружено в {TEMP_NAME}")
            return True
        except requests.RequestException as e:
            logging.error(f"Ошибка загрузки обновления: {e}")
            return False

    def apply_update(self):
        """Применяет обновление и перезапускает приложение."""
        try:
            logging.info("Применение обновления")
            time.sleep(1)  # Ждем завершения записи файла
            shutil.move(TEMP_NAME, APP_NAME)
            logging.info(f"Файл {TEMP_NAME} перемещен в {APP_NAME}")

            # Перезапускаем приложение
            logging.info(f"Запуск нового процесса: {sys.executable} {APP_NAME}")
            subprocess.Popen([sys.executable, APP_NAME], creationflags=subprocess.DETACHED_PROCESS if os.name == 'nt' else 0)
            self.root.destroy()
            logging.info("Текущий процесс завершается")
            sys.exit(0)
        except Exception as e:
            logging.error(f"Ошибка установки обновления: {e}")
            messagebox.showerror("Ошибка", f"Ошибка установки обновления: {e}")
            self.open_main_menu()

    def open_main_menu(self):
        """Открывает основное меню."""
        logging.info("Открытие основного меню")
        self.root.destroy()  # Закрываем окно проверки
        main_menu_root = tk.Tk()
        MainMenu(main_menu_root)
        main_menu_root.mainloop()

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Основное меню")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        # Центрируем окно
        self.root.eval('tk::PlaceWindow . center')

        # Создаем меню
        tk.Label(root, text="Добро пожаловать в приложение!", font=("Arial", 16)).pack(pady=20)

        tk.Button(root, text="Действие 1", font=("Arial", 12), command=self.action1).pack(pady=10)
        tk.Button(root, text="Действие 2", font=("Arial", 12), command=self.action2).pack(pady=10)
        tk.Button(root, text="Выход", font=("Arial", 12), command=self.root.destroy).pack(pady=10)

        logging.info("Главное меню инициализировано")

    def action1(self):
        messagebox.showinfo("Действие 1", "Вы нажали на первую кнопку!")
        logging.info("Выполнено действие 1")

    def action2(self):
        messagebox.showinfo("Действие 2", "Вы нажали на вторую кнопку!")
        logging.info("Выполнено действие 2")

if __name__ == "__main__":
    logging.info("Запуск приложения")
    root = tk.Tk()
    app = UpdateWindow(root)
    root.mainloop()
