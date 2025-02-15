import sqlite3
from src.config import Config
import os

class Database:
    """
    Класс для работы с базой данных SQLite
    """
    def __init__(self):
        self.db_path = Config.DB_PATH
        self.conn = None
        self.cursor = None
        self._ensure_db_directory()

    def _ensure_db_directory(self):
        """Проверка и создание директории для базы данных"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)

    def connect(self):
        """Установка соединения с базой данных"""
        if self.conn is not None:
            return True

        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            # Включаем поддержку внешних ключей
            self.cursor.execute("PRAGMA foreign_keys = ON")
            return True
        except sqlite3.Error as e:
            print(f"Ошибка при подключении к БД: {e}")
            self.close()
            return False

    def close(self):
        """Закрытие соединения с базой данных"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            try:
                self.conn.close()
            except sqlite3.Error:
                pass
        self.cursor = None
        self.conn = None

    def begin_transaction(self):
        """Начало транзакции"""
        if self.conn:
            self.conn.execute("BEGIN")

    def commit(self):
        """Подтверждение транзакции"""
        if self.conn:
            try:
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Ошибка при подтверждении транзакции: {e}")
                self.conn.rollback()

    def rollback(self):
        """Откат транзакции"""
        if self.conn:
            self.conn.rollback()

    def execute(self, sql, parameters=None):
        """Выполнение SQL запроса"""
        if not self.connect():
            print("Не удалось установить соединение с базой данных")
            return None

        try:
            if parameters:
                return self.cursor.execute(sql, parameters)
            return self.cursor.execute(sql)
        except sqlite3.Error as e:
            print(f"Ошибка при выполнении запроса: {e}")
            print(f"SQL: {sql}")
            print(f"Параметры: {parameters}")
            return None

    def initialize(self):
        """Инициализация структуры базы данных"""
        if not self.connect():
            return False

        try:
            self.begin_transaction()
            # Создание таблиц
            self.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            self.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT,
                    priority INTEGER,
                    color TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')

            self.execute('''
                CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    name TEXT NOT NULL,
                    frequency TEXT,
                    reminder_time TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')

            self.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    title TEXT NOT NULL,
                    author TEXT,
                    file_path TEXT,
                    current_page INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')

            self.execute('''
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER,
                    page_number INTEGER,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (book_id) REFERENCES books (id)
                )
            ''')

            self.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка при инициализации БД: {e}")
            self.rollback()
            return False
        finally:
            self.close()