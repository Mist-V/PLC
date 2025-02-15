import customtkinter as ctk
from src.services.auth_service import AuthService
from src.config import Config

class AuthFrame(ctk.CTkFrame):
    """
    Фрейм авторизации пользователя
    """
    def __init__(self, parent, controller):
        print("Инициализация AuthFrame...")
        super().__init__(
            parent,
            corner_radius=Config.CORNER_RADIUS["regular"],
            fg_color="transparent"
        )
        self.controller = controller
        self.auth_service = AuthService()

        print("Создание виджетов авторизации...")
        self.create_widgets()
        print("AuthFrame инициализирован")

    def create_widgets(self):
        """Создание элементов интерфейса"""
        # Центральный контейнер
        container = ctk.CTkFrame(
            self,
            corner_radius=Config.CORNER_RADIUS["large"],
            fg_color=("gray95", "gray10")
        )
        container.place(relx=0.5, rely=0.5, anchor="center")

        # Внутренний контейнер с отступами
        inner_container = ctk.CTkFrame(
            container,
            fg_color="transparent"
        )
        inner_container.pack(padx=Config.PADDING["large"], pady=Config.PADDING["large"])

        # Заголовок
        print("Создание заголовка...")
        title = ctk.CTkLabel(
            inner_container,
            text="Добро пожаловать",
            font=(Config.FONT_FAMILY, Config.FONT_SIZES["title"], "bold")
        )
        title.pack(pady=Config.PADDING["large"])

        subtitle = ctk.CTkLabel(
            inner_container,
            text="Войдите в свой аккаунт",
            font=(Config.FONT_FAMILY, Config.FONT_SIZES["regular"]),
            text_color=("gray60", "gray70")
        )
        subtitle.pack(pady=(0, Config.PADDING["large"]))

        print("Создание полей ввода...")
        # Поле для username
        self.username_entry = ctk.CTkEntry(
            inner_container,
            placeholder_text="Имя пользователя",
            width=Config.INPUT["width"],
            height=Config.INPUT["height"],
            font=(Config.FONT_FAMILY, Config.FONT_SIZES["regular"]),
            corner_radius=Config.CORNER_RADIUS["regular"]
        )
        self.username_entry.pack(pady=Config.PADDING["regular"])

        # Поле для пароля
        self.password_entry = ctk.CTkEntry(
            inner_container,
            placeholder_text="Пароль",
            show="•",
            width=Config.INPUT["width"],
            height=Config.INPUT["height"],
            font=(Config.FONT_FAMILY, Config.FONT_SIZES["regular"]),
            corner_radius=Config.CORNER_RADIUS["regular"]
        )
        self.password_entry.pack(pady=Config.PADDING["regular"])

        print("Создание кнопок...")
        # Кнопки
        button_container = ctk.CTkFrame(
            inner_container,
            fg_color="transparent"
        )
        button_container.pack(pady=Config.PADDING["large"])

        login_button = ctk.CTkButton(
            button_container,
            text="Войти",
            command=self.login,
            width=Config.BUTTON["width"],
            height=Config.BUTTON["height"],
            font=(Config.FONT_FAMILY, Config.FONT_SIZES["regular"]),
            corner_radius=Config.CORNER_RADIUS["regular"],
            hover_color=Config.DARK_THEME["accent_hover"] if ctk.get_appearance_mode() == "Dark" else Config.LIGHT_THEME["accent_hover"]
        )
        login_button.pack(side="left", padx=Config.PADDING["small"])

        register_button = ctk.CTkButton(
            button_container,
            text="Регистрация",
            command=self.register,
            width=Config.BUTTON["width"],
            height=Config.BUTTON["height"],
            font=(Config.FONT_FAMILY, Config.FONT_SIZES["regular"]),
            corner_radius=Config.CORNER_RADIUS["regular"],
            fg_color="transparent",
            hover_color=("gray85", "gray20"),
            border_width=2,
            border_color=Config.DARK_THEME["accent"] if ctk.get_appearance_mode() == "Dark" else Config.LIGHT_THEME["accent"]
        )
        register_button.pack(side="left", padx=Config.PADDING["small"])

        # Метка для сообщений об ошибках
        self.message_label = ctk.CTkLabel(
            inner_container,
            text="",
            text_color=("gray60", "gray70"),
            font=(Config.FONT_FAMILY, Config.FONT_SIZES["regular"])
        )
        self.message_label.pack(pady=Config.PADDING["regular"])
        print("Все виджеты авторизации созданы")

    def _validate_input(self) -> tuple[bool, str]:
        """Валидация входных данных"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username:
            return False, "Введите имя пользователя"
        if not password:
            return False, "Введите пароль"
        if len(username) < 3:
            return False, "Имя пользователя должно быть не менее 3 символов"
        if len(password) < 6:
            return False, "Пароль должен быть не менее 6 символов"

        return True, ""

    def _clear_inputs(self):
        """Очистка полей ввода"""
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.username_entry.focus()

    def login(self):
        """Обработка входа пользователя"""
        print("Попытка входа...")
        is_valid, error_message = self._validate_input()

        if not is_valid:
            self.message_label.configure(
                text=error_message,
                text_color=Config.LIGHT_THEME["error"]
            )
            print(f"Ошибка валидации при входе: {error_message}")
            return

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if self.auth_service.login(username, password):
            self.message_label.configure(
                text="Успешный вход!",
                text_color=Config.LIGHT_THEME["success"]
            )
            print("Вход выполнен успешно")
            self._clear_inputs()
            # Переключаемся на основной экран
            self.controller.show_frame("tasks")
        else:
            self.message_label.configure(
                text="Неверное имя пользователя или пароль",
                text_color=Config.LIGHT_THEME["error"]
            )
            print("Ошибка входа: неверные учетные данные")

    def register(self):
        """Обработка регистрации пользователя"""
        print("Попытка регистрации...")
        is_valid, error_message = self._validate_input()

        if not is_valid:
            self.message_label.configure(
                text=error_message,
                text_color=Config.LIGHT_THEME["error"]
            )
            print(f"Ошибка валидации при регистрации: {error_message}")
            return

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if self.auth_service.register(username, password):
            self.message_label.configure(
                text="Регистрация успешна! Теперь вы можете войти",
                text_color=Config.LIGHT_THEME["success"]
            )
            self._clear_inputs()
            print("Регистрация выполнена успешно")
        else:
            self.message_label.configure(
                text="Пользователь уже существует",
                text_color=Config.LIGHT_THEME["error"]
            )
            print("Ошибка регистрации: пользователь существует")