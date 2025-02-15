from typing import List, Optional
import os
from datetime import datetime
import PyPDF2
from src.db.models import Book, Note
from src.db.database import Database

class LibraryService:
    """
    Сервис для работы с библиотекой
    """
    def __init__(self):
        self.db = Database()

    def add_book(self, user_id: int, title: str, author: str,
                file_path: str) -> Optional[Book]:
        """
        Добавление новой книги в библиотеку
        """
        try:
            # Проверка PDF файла
            if not os.path.exists(file_path):
                print(f"Файл не найден: {file_path}")
                return None

            with open(file_path, 'rb') as file:
                pdf = PyPDF2.PdfReader(file)
                # Просто проверяем, что можем прочитать PDF
                _ = len(pdf.pages)

            if not self.db.connect():
                return None

            cursor = self.db.cursor
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute('''
                INSERT INTO books (user_id, title, author, file_path, current_page, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, title, author, file_path, 0, current_time))

            book_id = cursor.lastrowid
            self.db.conn.commit()

            return Book(
                id=book_id,
                user_id=user_id,
                title=title,
                author=author,
                file_path=file_path,
                current_page=0,
                created_at=datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
            )
        except Exception as e:
            print(f"Ошибка при добавлении книги: {e}")
            return None
        finally:
            self.db.close()

    def get_user_books(self, user_id: int) -> List[Book]:
        """
        Получение всех книг пользователя
        """
        try:
            if not self.db.connect():
                return []

            cursor = self.db.cursor
            cursor.execute('SELECT * FROM books WHERE user_id = ?', (user_id,))

            books = []
            for row in cursor.fetchall():
                books.append(Book(
                    id=row[0],
                    user_id=row[1],
                    title=row[2],
                    author=row[3],
                    file_path=row[4],
                    current_page=row[5],
                    created_at=datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S')
                ))
            return books
        except Exception as e:
            print(f"Ошибка при получении книг: {e}")
            return []
        finally:
            self.db.close()

    def update_current_page(self, book_id: int, page: int) -> bool:
        """
        Обновление текущей страницы книги
        """
        try:
            if not self.db.connect():
                return False

            cursor = self.db.cursor
            cursor.execute('''
                UPDATE books 
                SET current_page = ?
                WHERE id = ?
            ''', (page, book_id))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка при обновлении страницы: {e}")
            return False
        finally:
            self.db.close()

    def add_note(self, book_id: int, page_number: int, content: str) -> Optional[Note]:
        """
        Добавление заметки к книге
        """
        try:
            if not self.db.connect():
                return None

            cursor = self.db.cursor
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute('''
                INSERT INTO notes (book_id, page_number, content, created_at)
                VALUES (?, ?, ?, ?)
            ''', (book_id, page_number, content, current_time))

            note_id = cursor.lastrowid
            self.db.conn.commit()

            return Note(
                id=note_id,
                book_id=book_id,
                page_number=page_number,
                content=content,
                created_at=datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
            )
        except Exception as e:
            print(f"Ошибка при добавлении заметки: {e}")
            return None
        finally:
            self.db.close()

    def get_book_notes(self, book_id: int) -> List[Note]:
        """
        Получение всех заметок к книге
        """
        try:
            if not self.db.connect():
                return []

            cursor = self.db.cursor
            cursor.execute('SELECT * FROM notes WHERE book_id = ?', (book_id,))

            notes = []
            for row in cursor.fetchall():
                notes.append(Note(
                    id=row[0],
                    book_id=row[1],
                    page_number=row[2],
                    content=row[3],
                    created_at=datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S')
                ))
            return notes
        except Exception as e:
            print(f"Ошибка при получении заметок: {e}")
            return []
        finally:
            self.db.close()

    def get_page_content(self, book_id: int, page_number: int) -> str:
        """
        Получение содержимого страницы книги
        """
        try:
            book = self.get_book_by_id(book_id)
            if not book or not os.path.exists(book.file_path):
                return ""

            with open(book.file_path, 'rb') as file:
                pdf = PyPDF2.PdfReader(file)
                if 0 <= page_number < len(pdf.pages):
                    return pdf.pages[page_number].extract_text()
            return ""
        except Exception as e:
            print(f"Ошибка при чтении PDF: {e}")
            return ""

    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """
        Получение книги по ID
        """
        try:
            if not self.db.connect():
                return None

            cursor = self.db.cursor
            cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
            book_data = cursor.fetchone()

            if book_data:
                return Book(
                    id=book_data[0],
                    user_id=book_data[1],
                    title=book_data[2],
                    author=book_data[3],
                    file_path=book_data[4],
                    current_page=book_data[5],
                    created_at=datetime.strptime(book_data[6], '%Y-%m-%d %H:%M:%S')
                )
            return None
        except Exception as e:
            print(f"Ошибка при получении книги: {e}")
            return None
        finally:
            self.db.close()