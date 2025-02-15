from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    """Модель пользователя"""
    id: Optional[int]
    username: str
    password_hash: str
    created_at: datetime

@dataclass
class Task:
    """Модель задачи"""
    id: Optional[int]
    user_id: int
    title: str
    description: Optional[str]
    status: str  # new, completed, cancelled, postponed
    priority: int
    color: Optional[str]
    created_at: datetime

@dataclass
class Habit:
    """Модель привычки"""
    id: Optional[int]
    user_id: int
    name: str
    frequency: str  # daily, weekly, monthly
    reminder_time: Optional[str]
    created_at: datetime

@dataclass
class Book:
    """Модель книги"""
    id: Optional[int]
    user_id: int
    title: str
    author: Optional[str]
    file_path: str
    current_page: int
    created_at: datetime

@dataclass
class Note:
    """Модель заметки к книге"""
    id: Optional[int]
    book_id: int
    page_number: int
    content: str
    created_at: datetime
