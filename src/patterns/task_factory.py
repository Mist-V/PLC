from abc import ABC, abstractmethod
from src.db.models import Task
from datetime import datetime
from typing import Optional

class TaskCreator(ABC):
    """
    Абстрактный класс создателя задач
    """
    @abstractmethod
    def create_task(self, user_id: int, title: str, description: Optional[str] = None) -> Task:
        """
        Создает новую задачу

        Args:
            user_id: ID пользователя
            title: Заголовок задачи
            description: Описание задачи (опционально)

        Returns:
            Task: Созданная задача
        """
        pass

class SimpleTaskCreator(TaskCreator):
    """
    Создатель простых задач
    """
    def create_task(self, user_id: int, title: str, description: Optional[str] = None) -> Task:
        return Task(
            id=None,
            user_id=user_id,
            title=title,
            description=description or "",
            status="new",
            priority=1,
            color=None,
            created_at=datetime.now()
        )

class UrgentTaskCreator(TaskCreator):
    """
    Создатель срочных задач
    """
    def create_task(self, user_id: int, title: str, description: Optional[str] = None) -> Task:
        return Task(
            id=None,
            user_id=user_id,
            title=title,
            description=description or "",
            status="new",
            priority=3,
            color="#ff0000",
            created_at=datetime.now()
        )

class TaskFactory:
    """
    Фабрика задач
    """
    @staticmethod
    def get_task_creator(task_type: str) -> TaskCreator:
        """
        Возвращает создателя задач нужного типа

        Args:
            task_type: Тип задачи ("simple" или "urgent")

        Returns:
            TaskCreator: Создатель задач соответствующего типа

        Raises:
            ValueError: Если указан неизвестный тип задачи
        """
        if task_type == "simple":
            return SimpleTaskCreator()
        elif task_type == "urgent":
            return UrgentTaskCreator()
        else:
            raise ValueError(f"Неизвестный тип задачи: {task_type}")