from typing import List
from src.db.models import Task
from src.patterns.task_factory import TaskFactory
from src.patterns.repository import TaskRepository
from datetime import datetime

class TaskService:
    """
    Сервис для работы с задачами
    """
    def __init__(self):
        self.repository = TaskRepository()
        self.task_factory = TaskFactory()

    def create_task(self, user_id: int, title: str, description: str = None,
                   task_type: str = "simple") -> Task:
        """
        Создание новой задачи
        """
        creator = self.task_factory.get_task_creator(task_type)
        task = creator.create_task(user_id, title, description)
        return self.repository.create(task)

    def get_user_tasks(self, user_id: int, status: str = None,
                      search_query: str = None,
                      sort_by: str = "priority",
                      sort_order: str = "desc") -> List[Task]:
        """
        Получение всех задач пользователя с фильтрацией и сортировкой

        Args:
            user_id: ID пользователя
            status: Статус для фильтрации (опционально)
            search_query: Поисковый запрос (опционально)
            sort_by: Поле для сортировки ('priority', 'created_at')
            sort_order: Порядок сортировки ('asc', 'desc')
        """
        tasks = self.repository.get_all(user_id)

        # Фильтрация по статусу
        if status:
            tasks = [task for task in tasks if task.status == status]

        # Поиск по названию
        if search_query:
            search_query = search_query.lower()
            tasks = [task for task in tasks if search_query in task.title.lower()]

        # Сортировка
        reverse = sort_order == "desc"
        if sort_by == "priority":
            tasks.sort(key=lambda x: x.priority, reverse=reverse)
        elif sort_by == "created_at":
            tasks.sort(key=lambda x: x.created_at, reverse=reverse)

        return tasks

    def update_task_status(self, task_id: int, new_status: str):
        """
        Обновление статуса задачи
        """
        task = self.repository.get_by_id(task_id)
        if task:
            task.status = new_status
            self.repository.update(task)

    def update_task_priority(self, task_id: int, new_priority: int):
        """
        Обновление приоритета задачи
        """
        task = self.repository.get_by_id(task_id)
        if task:
            task.priority = new_priority
            self.repository.update(task)

    def update_task_color(self, task_id: int, new_color: str):
        """
        Обновление цвета задачи
        """
        task = self.repository.get_by_id(task_id)
        if task:
            task.color = new_color
            self.repository.update(task)

    def update_task_description(self, task_id: int, new_description: str):
        """
        Обновление описания задачи
        """
        task = self.repository.get_by_id(task_id)
        if task:
            task.description = new_description
            self.repository.update(task)

    def delete_task(self, task_id: int):
        """
        Удаление задачи
        """
        self.repository.delete(task_id)

    def get_task_statistics(self, user_id: int) -> dict:
        """
        Получение статистики по задачам пользователя
        """
        tasks = self.get_user_tasks(user_id)
        total_tasks = len(tasks)

        if not total_tasks:
            return {
                "total": 0,
                "completed": 0,
                "in_progress": 0,
                "completion_rate": 0
            }

        completed = len([t for t in tasks if t.status == "completed"])
        in_progress = len([t for t in tasks if t.status == "in_progress"])

        return {
            "total": total_tasks,
            "completed": completed,
            "in_progress": in_progress,
            "completion_rate": (completed / total_tasks) * 100
        }