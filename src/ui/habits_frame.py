import customtkinter as ctk
from src.services.habit_service import HabitService
from src.services.ai_service import AIService
from src.patterns.observer import Observer

class HabitsFrame(ctk.CTkFrame, Observer):
    """
    Фрейм для управления привычками
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.habit_service = HabitService()
        self.ai_service = AIService()

        # Подписываемся на уведомления
        self.habit_service.notification_manager.attach(self)

        self.create_widgets()

    def create_widgets(self):
        """Создание элементов интерфейса"""
        # Заголовок
        title = ctk.CTkLabel(self, text="Трекер привычек", font=("Roboto", 24))
        title.pack(pady=20)

        # Форма добавления привычки
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="x", padx=10, pady=5)

        self.habit_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Название привычки"
        )
        self.habit_entry.pack(side="left", fill="x", expand=True, padx=5)

        # Выбор частоты
        self.frequency_var = ctk.StringVar(value="daily")
        frequency_menu = ctk.CTkOptionMenu(
            form_frame,
            values=["daily", "weekly", "monthly"],
            variable=self.frequency_var
        )
        frequency_menu.pack(side="left", padx=5)

        # Выбор времени напоминания
        self.time_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="ЧЧ:ММ"
        )
        self.time_entry.pack(side="left", padx=5)

        # Кнопка добавления
        add_button = ctk.CTkButton(
            form_frame,
            text="Добавить",
            command=self.add_habit
        )
        add_button.pack(side="left", padx=5)

        # Кнопка получения идеи дня
        idea_button = ctk.CTkButton(
            form_frame,
            text="Идея дня",
            command=self.show_daily_idea
        )
        idea_button.pack(side="left", padx=5)

        # Список привычек
        self.habits_frame = ctk.CTkScrollableFrame(self)
        self.habits_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Обновляем список привычек
        self.refresh_habits()

    def add_habit(self):
        """Добавление новой привычки"""
        name = self.habit_entry.get()
        frequency = self.frequency_var.get()
        reminder_time = self.time_entry.get()

        if not name:
            return

        current_user = self.controller.auth_service.get_current_user()
        if not current_user:
            return

        self.habit_service.create_habit(
            user_id=current_user.id,
            name=name,
            frequency=frequency,
            reminder_time=reminder_time
        )

        self.habit_entry.delete(0, "end")
        self.time_entry.delete(0, "end")
        self.refresh_habits()

    def create_habit_widget(self, habit):
        """Создание виджета для привычки"""
        frame = ctk.CTkFrame(self.habits_frame)
        frame.pack(fill="x", padx=5, pady=2)

        # Название привычки
        name_label = ctk.CTkLabel(frame, text=habit.name)
        name_label.pack(side="left", padx=5)

        # Частота
        frequency_label = ctk.CTkLabel(
            frame,
            text=f"Частота: {habit.frequency}"
        )
        frequency_label.pack(side="left", padx=5)

        # Время напоминания
        if habit.reminder_time:
            time_label = ctk.CTkLabel(
                frame,
                text=f"Напоминание: {habit.reminder_time}"
            )
            time_label.pack(side="left", padx=5)

        # Кнопка AI-анализа
        ai_button = ctk.CTkButton(
            frame,
            text="🤖",
            width=30,
            command=lambda: self.show_ai_recommendation(habit)
        )
        ai_button.pack(side="right", padx=5)

        # Кнопка удаления
        delete_button = ctk.CTkButton(
            frame,
            text="Удалить",
            command=lambda: self.delete_habit(habit.id)
        )
        delete_button.pack(side="right", padx=5)

    def show_ai_recommendation(self, habit):
        """Показать AI рекомендации для привычки"""
        recommendation = self.ai_service.suggest_habit_improvement(habit.name)

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
        close_button = ctk.CTkButton(
            popup,
            text="Закрыть",
            command=popup.destroy
        )
        close_button.pack(pady=10)

    def show_daily_idea(self):
        """Показать идею дня от AI"""
        idea = self.ai_service.generate_daily_idea()

        # Создаем всплывающее окно
        popup = ctk.CTkToplevel(self)
        popup.title("Идея дня")
        popup.geometry("400x300")

        # Добавляем текст идеи
        text = ctk.CTkTextbox(popup, wrap="word")
        text.pack(padx=20, pady=20, fill="both", expand=True)
        text.insert("1.0", idea)
        text.configure(state="disabled")

        # Кнопка закрытия
        close_button = ctk.CTkButton(
            popup,
            text="Закрыть",
            command=popup.destroy
        )
        close_button.pack(pady=10)

    def refresh_habits(self):
        """Обновление списка привычек"""
        # Очистка текущего списка
        for widget in self.habits_frame.winfo_children():
            widget.destroy()

        current_user = self.controller.auth_service.get_current_user()
        if not current_user:
            return

        # Получение и отображение привычек
        habits = self.habit_service.get_user_habits(current_user.id)
        for habit in habits:
            self.create_habit_widget(habit)

    def delete_habit(self, habit_id: int):
        """Удаление привычки"""
        self.habit_service.delete_habit(habit_id)
        self.refresh_habits()

    def update(self, message: str):
        """
        Обработка уведомлений (реализация интерфейса Observer)
        """
        notification = ctk.CTkToplevel(self)
        notification.geometry("300x100")
        notification.title("Напоминание")

        label = ctk.CTkLabel(notification, text=message)
        label.pack(pady=20)

        button = ctk.CTkButton(
            notification,
            text="OK",
            command=notification.destroy
        )
        button.pack()