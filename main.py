import tkinter as tk
from tkinter import messagebox
import requests
import os
import sys
import subprocess
import shutil
import time
import threading

# Конфигурация
CURRENT_VERSION = "1.0.4"  # Текущая версия приложения
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

        # Запускаем проверку обновлений в отдельном потоке
        threading.Thread(target=self.check_for_update, daemon=True).start()

    def check_for_update(self):
        """Проверяет наличие обновлений."""
        try:
            response = requests.get(VERSION_URL, timeout=5)
            response.raise_for_status()
            latest_version = response.text.strip()
            has_update = latest_version > CURRENT_VERSION

            if has_update:
                self.label.config(text="Обновление...")
                self.root.update()
                if self.download_update():
                    self.apply_update()
                else:
                    messagebox.showerror("Ошибка", "Не удалось загрузить обновление.")
                    self.open_main_menu()
            else:
                self.open_main_menu()
        except requests.RequestException as e:
            messagebox.showerror("Ошибка", f"Ошибка проверки обновлений: {e}")
            self.open_main_menu()

    def download_update(self):
        """Загружает новую версию приложения."""
        try:
            response = requests.get(UPDATE_URL, timeout=10)
            response.raise_for_status()
            with open(TEMP_NAME, "wb") as f:
                f.write(response.content)
            return True
        except requests.RequestException:
            return False

    def apply_update(self):
        """Применяет обновление и перезапускает приложение."""
        try:
            time.sleep(1)  # Ждем завершения записи файла
            shutil.move(TEMP_NAME, APP_NAME)
            subprocess.Popen([sys.executable, APP_NAME])
            self.root.destroy()
            sys.exit(0)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка установки обновления: {e}")
            self.open_main_menu()

    def open_main_menu(self):
        """Открывает основное меню."""
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

    def action1(self):
        messagebox.showinfo("Действие 1", "Вы нажали на первую кнопку!")

    def action2(self):
        messagebox.showinfo("Действие 2", "Вы нажали на вторую кнопку!")

if __name__ == "__main__":
    root = tk.Tk()
    app = UpdateWindow(root)
    root.mainloop()
