import hashlib
import sqlite3
from datetime import datetime
from typing import Optional
from src.db.database import Database
from src.db.models import User

class AuthService:
    """
    Сервис аутентификации пользователей (Singleton)
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.db = Database()
            cls._instance.current_user = None
        return cls._instance

    def __init__(self):
        """
        __new__ уже инициализировал все необходимые атрибуты
        """
        pass

    def _hash_password(self, password: str) -> str:
        """Хеширование пароля"""
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username: str, password: str) -> bool:
        """
        Регистрация нового пользователя
        """
        if not username or not password:
            return False

        try:
            if not self.db.connect():
                return False

            self.db.begin_transaction()
            password_hash = self._hash_password(password)

            result = self.db.execute(
                'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                (username, password_hash)
            )

            if result:
                self.db.commit()
                return True
            return False

        except sqlite3.IntegrityError:
            print(f"Пользователь {username} уже существует")
            self.db.rollback()
            return False
        except Exception as e:
            print(f"Ошибка при регистрации: {e}")
            self.db.rollback()
            return False
        finally:
            self.db.close()

    def login(self, username: str, password: str) -> bool:
        """
        Аутентификация пользователя
        """
        try:
            if not self.db.connect():
                return False

            password_hash = self._hash_password(password)
            result = self.db.execute(
                'SELECT * FROM users WHERE username = ? AND password_hash = ?',
                (username, password_hash)
            )

            if not result:
                return False

            user_data = result.fetchone()
            if user_data:
                self.current_user = User(
                    id=user_data[0],
                    username=user_data[1],
                    password_hash=user_data[2],
                    created_at=datetime.strptime(user_data[3], '%Y-%m-%d %H:%M:%S')
                )
                print(f"Пользователь {username} успешно вошел в систему")
                return True
            return False

        except Exception as e:
            print(f"Ошибка при входе: {e}")
            return False
        finally:
            self.db.close()

    def logout(self):
        """
        Выход пользователя из системы
        """
        if self.current_user:
            print(f"Пользователь {self.current_user.username} вышел из системы")
        self.current_user = None

    def get_current_user(self) -> Optional[User]:
        """
        Получение текущего пользователя
        """
        return self.current_user

    def is_authenticated(self) -> bool:
        """
        Проверка аутентификации пользователя
        """
        return self.current_user is not None