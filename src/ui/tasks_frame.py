import customtkinter as ctk
from src.services.task_service import TaskService
from src.services.ai_service import AIService
from src.config import Config

class TasksFrame(ctk.CTkFrame):
    """
    Фрейм для управления задачами
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.task_service = TaskService()
        self.ai_service = AIService()

        # Параметры фильтрации и сортировки
        self.current_status = None
        self.current_sort_by = "priority"
        self.current_sort_order = "desc"

        self.create_widgets()
        self.tasks = []

    def create_widgets(self):
        """Создание элементов интерфейса"""
        # Статистика
        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.pack(fill="x", padx=10, pady=5)
        self.create_stats_widgets()

        # Верхняя панель
        top_panel = ctk.CTkFrame(self)
        top_panel.pack(fill="x", padx=10, pady=5)

        # Поле поиска
        self.search_entry = ctk.CTkEntry(
            top_panel,
            placeholder_text="Поиск задач..."
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_tasks())

        # Сортировка
        sort_label = ctk.CTkLabel(top_panel, text="Сортировать по:")
        sort_label.pack(side="left", padx=5)

        self.sort_var = ctk.StringVar(value="priority")
        sort_menu = ctk.CTkOptionMenu(
            top_panel,
            values=["priority", "created_at"],
            variable=self.sort_var,
            command=lambda _: self.refresh_tasks()
        )
        sort_menu.pack(side="left", padx=5)

        # Порядок сортировки
        self.order_var = ctk.StringVar(value="desc")
        order_menu = ctk.CTkOptionMenu(
            top_panel,
            values=["desc", "asc"],
            variable=self.order_var,
            command=lambda _: self.refresh_tasks()
        )
        order_menu.pack(side="left", padx=5)

        # Поле для новой задачи
        task_panel = ctk.CTkFrame(self)
        task_panel.pack(fill="x", padx=10, pady=5)

        self.task_entry = ctk.CTkEntry(
            task_panel,
            placeholder_text="Новая задача"
        )
        self.task_entry.pack(side="left", fill="x", expand=True, padx=5)

        # Описание задачи
        self.description_entry = ctk.CTkEntry(
            task_panel,
            placeholder_text="Описание (опционально)"
        )
        self.description_entry.pack(side="left", fill="x", expand=True, padx=5)

        # Кнопки для типов задач
        ctk.CTkButton(
            task_panel,
            text="Простая",
            command=lambda: self.add_task("simple")
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            task_panel,
            text="Срочная",
            command=lambda: self.add_task("urgent")
        ).pack(side="left", padx=5)

        # Список задач
        self.tasks_frame = ctk.CTkScrollableFrame(self)
        self.tasks_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Фильтры по статусу
        self.create_status_filters()

    def create_stats_widgets(self):
        """Создание виджетов статистики"""
        self.stats_labels = {
            "total": ctk.CTkLabel(self.stats_frame, text="Всего: 0"),
            "completed": ctk.CTkLabel(self.stats_frame, text="Завершено: 0"),
            "in_progress": ctk.CTkLabel(self.stats_frame, text="В работе: 0"),
            "completion_rate": ctk.CTkLabel(self.stats_frame, text="Выполнено: 0%")
        }

        for label in self.stats_labels.values():
            label.pack(side="left", padx=10)

    def create_status_filters(self):
        """Создание фильтров по статусу"""
        filter_frame = ctk.CTkFrame(self)
        filter_frame.pack(fill="x", padx=10, pady=5)

        statuses = [None, "new", "in_progress", "completed", "cancelled"]
        status_names = ["Все", "Новые", "В работе", "Завершённые", "Отменённые"]

        for status, name in zip(statuses, status_names):
            ctk.CTkButton(
                filter_frame,
                text=name,
                command=lambda s=status: self.set_status_filter(s),
                width=100
            ).pack(side="left", padx=2)

    def set_status_filter(self, status):
        """Установка фильтра по статусу"""
        self.current_status = status
        self.refresh_tasks()

    def update_stats(self):
        """Обновление статистики"""
        current_user = self.controller.auth_service.get_current_user()
        if not current_user:
            return

        stats = self.task_service.get_task_statistics(current_user.id)

        self.stats_labels["total"].configure(text=f"Всего: {stats['total']}")
        self.stats_labels["completed"].configure(text=f"Завершено: {stats['completed']}")
        self.stats_labels["in_progress"].configure(text=f"В работе: {stats['in_progress']}")
        self.stats_labels["completion_rate"].configure(
            text=f"Выполнено: {stats['completion_rate']:.1f}%"
        )

    def add_task(self, task_type: str):
        """Добавление новой задачи"""
        title = self.task_entry.get()
        description = self.description_entry.get()

        if not title:
            return

        current_user = self.controller.auth_service.get_current_user()
        if not current_user:
            return

        task = self.task_service.create_task(
            user_id=current_user.id,
            title=title,
            description=description,
            task_type=task_type
        )

        self.task_entry.delete(0, "end")
        self.description_entry.delete(0, "end")
        self.refresh_tasks()

    def create_task_widget(self, task):
        """Создание виджета для задачи"""
        frame = ctk.CTkFrame(self.tasks_frame)
        frame.pack(fill="x", padx=5, pady=2)

        # Статус
        status_btn = ctk.CTkButton(
            frame,
            text="✓" if task.status == "completed" else "○",
            width=30,
            command=lambda: self.toggle_task_status(task)
        )
        status_btn.pack(side="left", padx=5)

        # Название и описание
        info_frame = ctk.CTkFrame(frame, fg_color="transparent")
        info_frame.pack(side="left", padx=5, fill="x", expand=True)

        title = ctk.CTkLabel(
            info_frame,
            text=task.title,
            fg_color=task.color if task.color else "transparent"
        )
        title.pack(anchor="w")

        if task.description:
            description = ctk.CTkLabel(
                info_frame,
                text=task.description,
                text_color=("gray60", "gray70")
            )
            description.pack(anchor="w")

        # AI анализ
        ai_btn = ctk.CTkButton(
            frame,
            text="🤖",
            width=30,
            command=lambda: self.show_ai_recommendation(task)
        )
        ai_btn.pack(side="right", padx=2)

        # Кнопки управления
        ctk.CTkButton(
            frame,
            text="↑",
            width=30,
            command=lambda: self.change_priority(task, 1)
        ).pack(side="right", padx=2)

        ctk.CTkButton(
            frame,
            text="↓",
            width=30,
            command=lambda: self.change_priority(task, -1)
        ).pack(side="right", padx=2)

        ctk.CTkButton(
            frame,
            text="✕",
            width=30,
            command=lambda: self.delete_task(task)
        ).pack(side="right", padx=2)

    def show_ai_recommendation(self, task):
        """Показать AI рекомендации для задачи"""
        recommendation = self.ai_service.analyze_task(task.title)

        # Создаем всплывающее окно
        popup = ctk.CTkToplevel(self)
        popup.title("AI Рекомендации")
        popup.geometry("400x300")

        # Добавляем текст рекомендации
        text = ctk.CTkTextbox(popup, wrap="word")
        text.pack(padx=20, pady=20, fill="both", expand=True)
        text.insert("1.0", recommendation)
        text.configure(state="disabled")

        # Кнопка закрытия
        ctk.CTkButton(
            popup,
            text="Закрыть",
            command=popup.destroy
        ).pack(pady=10)

    def refresh_tasks(self):
        """Обновление списка задач"""
        # Очистка текущего списка
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        # Получение текущего пользователя
        current_user = self.controller.auth_service.get_current_user()
        if not current_user:
            return

        # Получение параметров фильтрации и сортировки
        search_query = self.search_entry.get() if hasattr(self, 'search_entry') else None
        sort_by = self.sort_var.get() if hasattr(self, 'sort_var') else "priority"
        sort_order = self.order_var.get() if hasattr(self, 'order_var') else "desc"

        # Получение и отображение задач
        tasks = self.task_service.get_user_tasks(
            current_user.id,
            status=self.current_status,
            search_query=search_query,
            sort_by=sort_by,
            sort_order=sort_order
        )

        for task in tasks:
            self.create_task_widget(task)

        # Обновление статистики
        self.update_stats()

    def toggle_task_status(self, task):
        """Переключение статуса задачи"""
        new_status = "completed" if task.status != "completed" else "new"
        self.task_service.update_task_status(task.id, new_status)
        self.refresh_tasks()

    def change_priority(self, task, delta):
        """Изменение приоритета задачи"""
        new_priority = task.priority + delta
        if 0 <= new_priority <= 3:
            self.task_service.update_task_priority(task.id, new_priority)
            self.refresh_tasks()

    def delete_task(self, task):
        """Удаление задачи"""
        self.task_service.delete_task(task.id)
        self.refresh_tasks()

    def apply_filters(self):
        """Применение фильтров"""
        self.refresh_tasks()