import customtkinter as ctk
from src.ui.auth_frame import AuthFrame
from src.ui.tasks_frame import TasksFrame
from src.ui.habits_frame import HabitsFrame
from src.ui.library_frame import LibraryFrame
from src.ui.calendar_frame import CalendarFrame
from src.services.auth_service import AuthService
from src.config import Config

class MainWindow(ctk.CTk):
    """
    Главное окно приложения
    """
    def __init__(self):
        print("Инициализация MainWindow...")
        super().__init__()

        # Инициализация сервиса аутентификации
        print("Создание сервиса аутентификации...")
        self.auth_service = AuthService()

        # Настройка окна
        self.title("Life Manager")
        self.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        self.minsize(800, 600)

        print("Создание навигационного фрейма...")
        # Создание контейнера для навигации
        self.navigation_frame = ctk.CTkFrame(
            self,
            corner_radius=Config.CORNER_RADIUS["regular"],
            width=250
        )
        self.navigation_frame.pack(
            side="left",
            fill="y",
            padx=Config.PADDING["regular"],
            pady=Config.PADDING["regular"]
        )
        self.navigation_frame.pack_propagate(False)  # Фиксированная ширина

        # Создаем кнопку переключения темы в навигационном фрейме
        self._setup_theme()

        print("Создание контейнера контента...")
        # Создание основного контейнера для контента
        self.content_frame = ctk.CTkFrame(
            self,
            corner_radius=Config.CORNER_RADIUS["regular"],
            fg_color=("gray95", "gray10")
        )
        self.content_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=Config.PADDING["regular"],
            pady=Config.PADDING["regular"]
        )

        # Создание навигационных кнопок
        self.create_navigation()

        # Инициализация фреймов
        self.frames = {}
        print("Настройка фреймов...")
        self.setup_frames()

        print("Отображение начального фрейма...")
        # Показываем соответствующий фрейм
        self._show_initial_frame()
        print("Инициализация MainWindow завершена")

    def _setup_theme(self):
        """Настройка темы приложения"""
        # Создаем контейнер для логотипа и кнопки темы
        header_frame = ctk.CTkFrame(
            self.navigation_frame,
            fg_color="transparent"
        )
        header_frame.pack(fill="x", padx=Config.PADDING["regular"], pady=Config.PADDING["regular"])

        # Логотип
        logo_label = ctk.CTkLabel(
            header_frame,
            text="Life Manager",
            font=(Config.FONT_FAMILY, Config.FONT_SIZES["large"], "bold")
        )
        logo_label.pack(side="left", padx=Config.PADDING["small"])

        # Кнопка переключения темы
        self.theme_button = ctk.CTkButton(
            header_frame,
            text="🌓",
            width=45,
            height=45,
            corner_radius=Config.CORNER_RADIUS["regular"],
            command=self._toggle_theme,
            fg_color="transparent",
            hover_color=("gray85", "gray20")
        )
        self.theme_button.pack(side="right", padx=Config.PADDING["small"])

    def _toggle_theme(self):
        """Переключение между темной и светлой темой"""
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")

    def create_navigation(self):
        """Создание навигационных кнопок"""
        print("Создание навигационных кнопок...")
        # Добавляем разделитель
        separator = ctk.CTkFrame(
            self.navigation_frame,
            height=2,
            fg_color=("gray85", "gray20")
        )
        separator.pack(fill="x", padx=Config.PADDING["regular"], pady=Config.PADDING["regular"])

        # Создаем кнопки навигации
        buttons = [
            ("Авторизация", "auth"),
            ("Задачи", "tasks"),
            ("Привычки", "habits"),
            ("Библиотека", "library"),
            ("Календарь", "calendar")
        ]

        for text, frame_name in buttons:
            btn = ctk.CTkButton(
                self.navigation_frame,
                text=text,
                command=lambda name=frame_name: self.show_frame(name),
                font=(Config.FONT_FAMILY, Config.FONT_SIZES["regular"]),
                corner_radius=Config.CORNER_RADIUS["regular"],
                height=Config.BUTTON["height"],
                hover_color=Config.DARK_THEME["accent_hover"] if ctk.get_appearance_mode() == "Dark" else Config.LIGHT_THEME["accent_hover"]
            )
            btn.pack(
                pady=Config.PADDING["small"],
                padx=Config.PADDING["regular"],
                fill="x"
            )

        # Добавляем разделитель перед кнопкой выхода
        bottom_separator = ctk.CTkFrame(
            self.navigation_frame,
            height=2,
            fg_color=("gray85", "gray20")
        )
        bottom_separator.pack(fill="x", padx=Config.PADDING["regular"], pady=Config.PADDING["regular"], side="bottom")

        # Кнопка выхода
        self.logout_button = ctk.CTkButton(
            self.navigation_frame,
            text="Выйти",
            command=self._handle_logout,
            font=(Config.FONT_FAMILY, Config.FONT_SIZES["regular"]),
            corner_radius=Config.CORNER_RADIUS["regular"],
            height=Config.BUTTON["height"],
            fg_color=Config.DARK_THEME["error"] if ctk.get_appearance_mode() == "Dark" else Config.LIGHT_THEME["error"],
            hover_color=("red", "darkred")
        )
        self.logout_button.pack(
            pady=Config.PADDING["regular"],
            padx=Config.PADDING["regular"],
            side="bottom",
            fill="x"
        )
        self._update_navigation_state()

    def setup_frames(self):
        """Инициализация всех фреймов"""
        print("Создание фреймов приложения...")
        self.frames = {
            "auth": AuthFrame(self.content_frame, self),
            "tasks": TasksFrame(self.content_frame, self),
            "habits": HabitsFrame(self.content_frame, self),
            "library": LibraryFrame(self.content_frame, self),
            "calendar": CalendarFrame(self.content_frame, self)
        }
        print("Все фреймы созданы успешно")

    def _show_initial_frame(self):
        """Показ начального фрейма в зависимости от состояния аутентификации"""
        if self.auth_service.is_authenticated():
            self.show_frame("tasks")
        else:
            self.show_frame("auth")

    def _update_navigation_state(self):
        """Обновление состояния навигационных элементов"""
        is_auth = self.auth_service.is_authenticated()
        self.logout_button.configure(state="normal" if is_auth else "disabled")

    def _handle_logout(self):
        """Обработка выхода из системы"""
        self.auth_service.logout()
        self._update_navigation_state()
        self.show_frame("auth")

    def show_frame(self, frame_name: str):
        """Отображение выбранного фрейма"""
        print(f"Переключение на фрейм: {frame_name}")

        # Проверяем, авторизован ли пользователь
        if frame_name != "auth" and not self.auth_service.is_authenticated():
            print("Пользователь не авторизован, показываем окно авторизации")
            frame_name = "auth"

        # Если пользователь авторизован и пытается открыть окно авторизации,
        # перенаправляем на tasks
        if frame_name == "auth" and self.auth_service.is_authenticated():
            print("Пользователь уже авторизован, показываем tasks")
            frame_name = "tasks"

        # Скрываем все фреймы
        for frame in self.frames.values():
            frame.pack_forget()

        # Показываем выбранный фрейм
        frame = self.frames[frame_name]
        frame.pack(fill="both", expand=True)

        # Обновляем состояние навигации
        self._update_navigation_state()
        print(f"Фрейм {frame_name} отображен")