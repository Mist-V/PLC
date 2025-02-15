from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic
from src.db.database import Database
from src.db.models import Task, Habit, Book, Note
from datetime import datetime

T = TypeVar('T')

class Repository(ABC, Generic[T]):
    """
    Абстрактный базовый класс для репозиториев
    """
    def __init__(self):
        self.db = Database()

    @abstractmethod
    def create(self, item: T) -> Optional[T]:
        """Создает новый элемент"""
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        """Получает элемент по ID"""
        pass

    @abstractmethod
    def get_all(self, user_id: int) -> List[T]:
        """Получает все элементы для пользователя"""
        pass

    @abstractmethod
    def update(self, item: T) -> bool:
        """Обновляет элемент"""
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        """Удаляет элемент"""
        pass

class TaskRepository(Repository[Task]):
    """
    Репозиторий для работы с задачами
    """
    def create(self, task: Task) -> Optional[Task]:
        try:
            if not self.db.connect():
                return None

            cursor = self.db.cursor
            cursor.execute('''
                INSERT INTO tasks (user_id, title, description, status, priority, color, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (task.user_id, task.title, task.description, task.status, 
                  task.priority, task.color, task.created_at.strftime('%Y-%m-%d %H:%M:%S')))

            task_id = cursor.lastrowid
            self.db.conn.commit()

            task.id = task_id
            return task
        except Exception as e:
            print(f"Ошибка при создании задачи: {e}")
            return None
        finally:
            self.db.close()

    def get_by_id(self, id: int) -> Optional[Task]:
        try:
            if not self.db.connect():
                return None

            cursor = self.db.cursor
            cursor.execute('SELECT * FROM tasks WHERE id = ?', (id,))
            task_data = cursor.fetchone()

            if task_data:
                return Task(
                    id=task_data[0],
                    user_id=task_data[1],
                    title=task_data[2],
                    description=task_data[3],
                    status=task_data[4],
                    priority=task_data[5],
                    color=task_data[6],
                    created_at=datetime.strptime(task_data[7], '%Y-%m-%d %H:%M:%S')
                )
            return None
        except Exception as e:
            print(f"Ошибка при получении задачи: {e}")
            return None
        finally:
            self.db.close()

    def get_all(self, user_id: int) -> List[Task]:
        try:
            if not self.db.connect():
                return []

            cursor = self.db.cursor
            cursor.execute('SELECT * FROM tasks WHERE user_id = ?', (user_id,))

            tasks = []
            for row in cursor.fetchall():
                tasks.append(Task(
                    id=row[0],
                    user_id=row[1],
                    title=row[2],
                    description=row[3],
                    status=row[4],
                    priority=row[5],
                    color=row[6],
                    created_at=datetime.strptime(row[7], '%Y-%m-%d %H:%M:%S')
                ))
            return tasks
        except Exception as e:
            print(f"Ошибка при получении задач: {e}")
            return []
        finally:
            self.db.close()

    def update(self, task: Task) -> bool:
        try:
            if not self.db.connect():
                return False

            cursor = self.db.cursor
            cursor.execute('''
                UPDATE tasks 
                SET title = ?, description = ?, status = ?, priority = ?, color = ?
                WHERE id = ?
            ''', (task.title, task.description, task.status, 
                  task.priority, task.color, task.id))

            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка при обновлении задачи: {e}")
            return False
        finally:
            self.db.close()

    def delete(self, id: int) -> bool:
        try:
            if not self.db.connect():
                return False

            cursor = self.db.cursor
            cursor.execute('DELETE FROM tasks WHERE id = ?', (id,))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка при удалении задачи: {e}")
            return False
        finally:
            self.db.close()