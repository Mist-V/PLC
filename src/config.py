class Config:
    """
    Класс с конфигурационными параметрами приложения
    """
    # Параметры базы данных
    DB_PATH = "life_manager.db"

    # Параметры UI
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800

    # Параметры темы
    LIGHT_THEME = {
        "bg_primary": "#ffffff",
        "bg_secondary": "#f8f9fa",
        "fg_primary": "#212529",
        "fg_secondary": "#6c757d",
        "accent": "#228be6",
        "accent_hover": "#1971c2",
        "success": "#40c057",
        "error": "#fa5252",
        "warning": "#fd7e14",
        "border": "#e9ecef",
        "button_text": "#ffffff"
    }

    DARK_THEME = {
        "bg_primary": "#212529",
        "bg_secondary": "#343a40",
        "fg_primary": "#f8f9fa",
        "fg_secondary": "#adb5bd",
        "accent": "#339af0",
        "accent_hover": "#1c7ed6",
        "success": "#51cf66",
        "error": "#ff6b6b",
        "warning": "#fcc419",
        "border": "#495057",
        "button_text": "#ffffff"
    }

    # Параметры шрифтов
    FONT_FAMILY = "Roboto"
    FONT_SIZES = {
        "small": 12,
        "regular": 14,
        "large": 16,
        "title": 28
    }

    # Отступы и размеры
    PADDING = {
        "small": 8,
        "regular": 16,
        "large": 24
    }

    CORNER_RADIUS = {
        "small": 6,
        "regular": 10,
        "large": 15
    }

    # Размеры элементов
    BUTTON = {
        "width": 180,
        "height": 45
    }

    INPUT = {
        "width": 320,
        "height": 45
    }

    # Параметры AI сервиса
    AI_HOST = "http://localhost"
    AI_PORT = 11434

    # Параметры для напоминаний
    NOTIFICATION_CHECK_INTERVAL = 60  # в секундах