import customtkinter as ctk
from datetime import datetime, timedelta
import calendar
from src.services.task_service import TaskService
from src.services.habit_service import HabitService
from typing import Dict, Any

class CalendarFrame(ctk.CTkFrame):
    """
    Фрейм для отображения календаря с задачами и привычками
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.task_service = TaskService()
        self.habit_service = HabitService()

        # Текущая дата
        self.current_date = datetime.now()

        # Словарь для хранения ячеек календаря
        self.calendar_cells: Dict[tuple, Dict[str, Any]] = {}

        self.create_widgets()

    def create_widgets(self):
        """Создание элементов интерфейса календаря"""
        # Верхняя панель с навигацией
        nav_frame = ctk.CTkFrame(self)
        nav_frame.pack(fill="x", padx=10, pady=5)

        # Кнопка предыдущего месяца
        prev_button = ctk.CTkButton(
            nav_frame,
            text="←",
            width=30,
            command=self.previous_month
        )
        prev_button.pack(side="left", padx=5)

        # Метка с текущим месяцем и годом
        self.month_label = ctk.CTkLabel(
            nav_frame,
            text=self.get_month_year_string(),
            font=("Roboto", 16, "bold")
        )
        self.month_label.pack(side="left", padx=20)

        # Кнопка следующего месяца
        next_button = ctk.CTkButton(
            nav_frame,
            text="→",
            width=30,
            command=self.next_month
        )
        next_button.pack(side="left", padx=5)

        # Создание сетки календаря
        calendar_frame = ctk.CTkFrame(self)
        calendar_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Названия дней недели
        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        for i, day in enumerate(days):
            label = ctk.CTkLabel(
                calendar_frame,
                text=day,
                font=("Roboto", 12, "bold")
            )
            label.grid(row=0, column=i, padx=2, pady=2, sticky="nsew")

        # Создание ячеек календаря
        for row in range(6):
            for col in range(7):
                cell_frame = ctk.CTkFrame(calendar_frame)
                cell_frame.grid(row=row+1, column=col, padx=2, pady=2, sticky="nsew")

                # Метка для даты
                date_label = ctk.CTkLabel(cell_frame, text="")
                date_label.pack(anchor="nw", padx=2, pady=2)

                # Область для событий
                events_text = ctk.CTkTextbox(cell_frame, height=80)
                events_text.pack(fill="both", expand=True, padx=2, pady=2)

                self.calendar_cells[(row, col)] = {
                    "frame": cell_frame,
                    "date_label": date_label,
                    "events_text": events_text
                }

        # Настройка сетки
        for i in range(7):
            calendar_frame.grid_columnconfigure(i, weight=1)
        for i in range(7):
            calendar_frame.grid_rowconfigure(i, weight=1)

        # Панель деталей
        details_frame = ctk.CTkFrame(self)
        details_frame.pack(fill="x", padx=10, pady=5)

        self.details_label = ctk.CTkLabel(
            details_frame,
            text="Выберите дату для просмотра деталей",
            font=("Roboto", 12)
        )
        self.details_label.pack(pady=5)

        # Обновление календаря
        self.update_calendar()

    def get_month_year_string(self) -> str:
        """Получение строки с названием месяца и годом"""
        months = [
            "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
            "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
        ]
        return f"{months[self.current_date.month - 1]} {self.current_date.year}"

    def update_calendar(self):
        """Обновление отображения календаря"""
        # Обновление заголовка
        self.month_label.configure(text=self.get_month_year_string())

        # Получение календарной информации
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)

        # Очистка всех ячеек
        for cell in self.calendar_cells.values():
            cell["date_label"].configure(text="")
            cell["events_text"].delete("1.0", "end")
            cell["frame"].configure(fg_color=("gray90", "gray13"))

        # Получение данных пользователя
        current_user = self.controller.auth_service.get_current_user()
        if not current_user:
            return

        # Получение задач и привычек
        tasks = self.task_service.get_user_tasks(current_user.id)
        habits = self.habit_service.get_user_habits(current_user.id)

        # Заполнение календаря
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                if day != 0:
                    cell = self.calendar_cells[(week_num, day_num)]

                    # Установка даты
                    cell["date_label"].configure(text=str(day))

                    # Проверка текущего дня
                    if (day == datetime.now().day and 
                        self.current_date.month == datetime.now().month and
                        self.current_date.year == datetime.now().year):
                        cell["frame"].configure(fg_color=("lightblue", "darkblue"))

                    # Добавление задач и привычек
                    events_text = ""

                    # Проверка задач на этот день
                    day_date = datetime(
                        self.current_date.year,
                        self.current_date.month,
                        day
                    )

                    for task in tasks:
                        if not isinstance(task.created_at, str):
                            task_date = task.created_at
                        else:
                            task_date = datetime.strptime(task.created_at, "%Y-%m-%d %H:%M:%S")

                        if task_date.date() == day_date.date() and task.status != "completed":
                            events_text += f"• {task.title}\n"

                    # Проверка привычек
                    for habit in habits:
                        if habit.frequency == "daily":
                            events_text += f"□ {habit.name}\n"
                        elif habit.frequency == "weekly" and day_date.weekday() == 0:
                            events_text += f"□ {habit.name} (нед.)\n"
                        elif habit.frequency == "monthly" and day == 1:
                            events_text += f"□ {habit.name} (мес.)\n"

                    cell["events_text"].delete("1.0", "end")
                    cell["events_text"].insert("1.0", events_text)

    def previous_month(self):
        """Переход к предыдущему месяцу"""
        self.current_date = self.current_date.replace(day=1)
        self.current_date = self.current_date - timedelta(days=1)
        self.current_date = self.current_date.replace(day=1)
        self.update_calendar()

    def next_month(self):
        """Переход к следующему месяцу"""
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(
                year=self.current_date.year + 1,
                month=1,
                day=1
            )
        else:
            self.current_date = self.current_date.replace(
                month=self.current_date.month + 1,
                day=1
            )
        self.update_calendar()