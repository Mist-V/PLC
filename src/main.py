import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

print("Инициализация приложения...")

try:
    import customtkinter as ctk
    from src.ui.main_window import MainWindow
    from src.db.database import Database
    from src.config import Config
    print("Все необходимые модули импортированы успешно")
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("Убедитесь, что все необходимые пакеты установлены")
    sys.exit(1)

def main():
    """
    Главная точка входа в приложение.
    Инициализирует базу данных и запускает главное окно.
    """
    try:
        print("Настройка темы приложения...")
        # Настраиваем тему приложения
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        print("Инициализация конфигурации...")
        # Инициализируем конфигурацию
        config = Config()

        print("Инициализация базы данных...")
        # Инициализируем базу данных
        db = Database()
        if not db.initialize():
            print("Ошибка инициализации базы данных")
            return

        print("Создание главного окна приложения...")
        # Создаем и запускаем главное окно
        app = MainWindow()

        print("Запуск главного цикла приложения...")
        app.mainloop()
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()