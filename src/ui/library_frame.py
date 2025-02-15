import customtkinter as ctk
from tkinter import filedialog
from src.services.library_service import LibraryService

class LibraryFrame(ctk.CTkFrame):
    """
    Фрейм для работы с библиотекой
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.library_service = LibraryService()
        self.current_book = None

        self.create_widgets()

    def create_widgets(self):
        """Создание элементов интерфейса"""
        # Основной контейнер
        main_container = ctk.CTkFrame(self)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Левая панель со списком книг
        left_panel = ctk.CTkFrame(main_container)
        left_panel.pack(side="left", fill="y", padx=5, pady=5, expand=False)

        # Кнопка добавления книги
        add_button = ctk.CTkButton(
            left_panel,
            text="Добавить книгу",
            command=self.add_book
        )
        add_button.pack(pady=5)

        # Список книг
        self.books_frame = ctk.CTkScrollableFrame(left_panel)
        self.books_frame.pack(fill="both", expand=True)

        # Правая панель для чтения
        self.reader_frame = ctk.CTkFrame(main_container)
        self.reader_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        # Панель управления чтением
        control_panel = ctk.CTkFrame(self.reader_frame)
        control_panel.pack(fill="x", pady=5)

        self.page_entry = ctk.CTkEntry(
            control_panel,
            placeholder_text="Страница"
        )
        self.page_entry.pack(side="left", padx=5)

        go_button = ctk.CTkButton(
            control_panel,
            text="Перейти",
            command=self.go_to_page
        )
        go_button.pack(side="left", padx=5)

        # Область для текста
        self.text_area = ctk.CTkTextbox(self.reader_frame)
        self.text_area.pack(fill="both", expand=True, pady=5)

        # Область для заметок
        notes_frame = ctk.CTkFrame(self.reader_frame)
        notes_frame.pack(fill="x", pady=5)

        self.note_entry = ctk.CTkEntry(
            notes_frame,
            placeholder_text="Добавить заметку"
        )
        self.note_entry.pack(side="left", fill="x", expand=True, padx=5)

        add_note_button = ctk.CTkButton(
            notes_frame,
            text="Добавить заметку",
            command=self.add_note
        )
        add_note_button.pack(side="right", padx=5)

        # Список заметок
        self.notes_list = ctk.CTkTextbox(self.reader_frame)
        self.notes_list.pack(fill="both", expand=True, pady=5)

        self.refresh_books()

    def add_book(self):
        """Добавление новой книги"""
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF files", "*.pdf")]
        )
        if not file_path:
            return

        title = ctk.CTkInputDialog(
            text="Введите название книги:",
            title="Новая книга"
        ).get_input()

        if not title:
            return

        author = ctk.CTkInputDialog(
            text="Введите автора книги:",
            title="Новая книга"
        ).get_input()

        current_user = self.controller.auth_service.get_current_user()
        if not current_user:
            return

        book = self.library_service.add_book(
            user_id=current_user.id,
            title=title,
            author=author,
            file_path=file_path
        )

        if book:
            self.refresh_books()

    def create_book_widget(self, book):
        """Создание виджета для книги"""
        frame = ctk.CTkFrame(self.books_frame)
        frame.pack(fill="x", padx=5, pady=2)

        title_label = ctk.CTkLabel(
            frame,
            text=f"{book.title}\nАвтор: {book.author}"
        )
        title_label.pack(side="left", padx=5)

        open_button = ctk.CTkButton(
            frame,
            text="Открыть",
            command=lambda: self.open_book(book)
        )
        open_button.pack(side="right", padx=5)

    def open_book(self, book):
        """Открытие книги для чтения"""
        self.current_book = book
        self.load_page(book.current_page)
        self.refresh_notes()

    def load_page(self, page_number: int):
        """Загрузка страницы книги"""
        if not self.current_book:
            print("Нет открытой книги")
            return

        try:
            # Проверка валидности номера страницы
            if page_number < 0:
                print("Номер страницы не может быть отрицательным")
                return

            content = self.library_service.get_page_content(
                self.current_book.id,
                page_number
            )

            if content is None:
                print("Не удалось загрузить содержимое страницы")
                return

            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", content)

            self.library_service.update_current_page(
                self.current_book.id,
                page_number
            )
        except Exception as e:
            print(f"Ошибка при загрузке страницы: {e}")
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", "Ошибка при загрузке страницы")

    def go_to_page(self):
        """Переход на указанную страницу"""
        try:
            page_text = self.page_entry.get().strip()
            if not page_text:
                print("Номер страницы не указан")
                return

            page = int(page_text)
            if page < 0:
                print("Номер страницы не может быть отрицательным")
                return

            self.load_page(page)
        except ValueError:
            print("Некорректный номер страницы")
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", "Пожалуйста, введите корректный номер страницы")

    def add_note(self):
        """Добавление заметки к текущей странице"""
        if not self.current_book:
            return

        content = self.note_entry.get()
        if not content:
            return

        current_page = self.current_book.current_page
        self.library_service.add_note(
            self.current_book.id,
            current_page,
            content
        )

        self.note_entry.delete(0, "end")
        self.refresh_notes()

    def refresh_notes(self):
        """Обновление списка заметок"""
        if not self.current_book:
            return

        self.notes_list.delete("1.0", "end")
        notes = self.library_service.get_book_notes(self.current_book.id)

        for note in notes:
            self.notes_list.insert(
                "end",
                f"Страница {note.page_number}:\n{note.content}\n\n"
            )

    def refresh_books(self):
        """Обновление списка книг"""
        for widget in self.books_frame.winfo_children():
            widget.destroy()

        current_user = self.controller.auth_service.get_current_user()
        if not current_user:
            return

        books = self.library_service.get_user_books(current_user.id)
        for book in books:
            self.create_book_widget(book)