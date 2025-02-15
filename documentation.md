# Life Manager - Документация проекта

## Содержание
1. [Общее описание проекта](#общее-описание-проекта)
2. [Архитектура](#архитектура)
3. [Паттерны проектирования](#паттерны-проектирования)
4. [Сервисы](#сервисы)
5. [UI компоненты](#ui-компоненты)
6. [База данных](#база-данных)
7. [Взаимодействие с AI](#взаимодействие-с-ai)
8. [Инструкции по использованию](#инструкции-по-использованию)

## Общее описание проекта

Life Manager - это десктопное приложение для управления личной жизнью, разработанное с использованием Python и микросервисной архитектуры. Приложение предоставляет комплексное решение для управления задачами, привычками, библиотекой и календарем с интегрированным AI-помощником.

### Основные возможности
- Управление задачами с приоритетами и статусами
- Трекер привычек с напоминаниями
- Личная библиотека
- Календарь событий
- AI-помощник для анализа задач и привычек
- Система аутентификации пользователей
- Поиск и фильтрация по всем типам данных
- Статистика и аналитика

### Технологический стек
- Python 3.11
- CustomTkinter (GUI framework)
- SQLite (База данных)
- Ollama (Локальный AI сервис)
- Паттерны проектирования (Observer, Factory, Repository)

## Архитектура

### Микросервисная архитектура
Проект построен на основе микросервисной архитектуры, где каждый компонент отвечает за свою конкретную функциональность:

```
src/
├── services/         # Сервисные компоненты
├── ui/              # Компоненты пользовательского интерфейса
├── db/              # Слой работы с базой данных
├── patterns/        # Реализации паттернов проектирования
└── config.py        # Конфигурация приложения
```

### Компоненты системы

#### 1. Сервисный слой
- `AuthService`: Аутентификация и управление пользователями
- `TaskService`: Управление задачами
- `HabitService`: Управление привычками
- `LibraryService`: Управление библиотекой
- `AIService`: Взаимодействие с Ollama AI

#### 2. UI слой
- `MainWindow`: Главное окно приложения
- `AuthFrame`: Компонент авторизации
- `TasksFrame`: Управление задачами
- `HabitsFrame`: Трекер привычек
- `LibraryFrame`: Библиотека
- `CalendarFrame`: Календарь

#### 3. Слой данных
- `Repository`: Абстрактный класс для работы с данными
- `TaskRepository`: Репозиторий задач
- SQLite база данных

## Паттерны проектирования

### 1. Observer Pattern
Используется для уведомлений о событиях в системе.

```python
class Observer(ABC):
    @abstractmethod
    def update(self, message: str):
        pass

class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, message: str):
        for observer in self._observers:
            observer.update(message)
```

### 2. Factory Pattern
Применяется для создания различных типов задач.

```python
class TaskCreator(ABC):
    @abstractmethod
    def create_task(self, user_id: int, title: str, description: Optional[str] = None) -> Task:
        pass

class SimpleTaskCreator(TaskCreator):
    def create_task(self, user_id: int, title: str, description: Optional[str] = None) -> Task:
        return Task(
            user_id=user_id,
            title=title,
            description=description or "",
            status="new",
            priority=1
        )

class UrgentTaskCreator(TaskCreator):
    def create_task(self, user_id: int, title: str, description: Optional[str] = None) -> Task:
        return Task(
            user_id=user_id,
            title=title,
            description=description or "",
            status="new",
            priority=3,
            color="#ff0000"
        )
```

### 3. Repository Pattern
Используется для абстрагирования работы с данными.

```python
class Repository(ABC):
    @abstractmethod
    def create(self, entity: Any) -> Any:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: int) -> Any:
        pass

    @abstractmethod
    def get_all(self, user_id: int) -> List[Any]:
        pass

    @abstractmethod
    def update(self, entity: Any) -> None:
        pass

    @abstractmethod
    def delete(self, entity_id: int) -> None:
        pass
```

## Сервисы

### 1. AuthService
Сервис аутентификации пользователей.

#### Основные методы:
```python
def login(self, username: str, password: str) -> bool
def register(self, username: str, password: str) -> bool
def logout(self) -> None
def is_authenticated(self) -> bool
def get_current_user(self) -> Optional[User]
```

### 2. TaskService
Сервис управления задачами.

#### Основные методы:
```python
def create_task(self, user_id: int, title: str, description: str = None, task_type: str = "simple") -> Task
def get_user_tasks(self, user_id: int, status: str = None, search_query: str = None, sort_by: str = "priority", sort_order: str = "desc") -> List[Task]
def update_task_status(self, task_id: int, new_status: str) -> None
def update_task_priority(self, task_id: int, new_priority: int) -> None
def delete_task(self, task_id: int) -> None
def get_task_statistics(self, user_id: int) -> dict
```

### 3. HabitService
Сервис управления привычками.

#### Основные методы:
```python
def create_habit(self, user_id: int, name: str, frequency: str, reminder_time: str) -> Habit
def get_user_habits(self, user_id: int) -> List[Habit]
def delete_habit(self, habit_id: int) -> None
def check_habit(self, habit_id: int) -> None
```

### 4. AIService
Сервис взаимодействия с AI.

#### Основные методы:
```python
def generate_response(self, prompt: str) -> Optional[str]
def generate_daily_idea(self) -> str
def analyze_task(self, task_description: str) -> str
def suggest_habit_improvement(self, habit_name: str) -> str
```

## UI компоненты

### 1. MainWindow
Главное окно приложения с навигацией.

#### Основные функции:
- Управление темной/светлой темой
- Навигация между разделами
- Управление авторизацией
- Отображение контента

### 2. TasksFrame
Компонент управления задачами.

#### Возможности:
- Создание простых и срочных задач
- Поиск и фильтрация задач
- Сортировка по приоритету и дате
- Отображение статистики
- AI-анализ задач
- Изменение статуса и приоритета

### 3. HabitsFrame
Компонент управления привычками.

#### Возможности:
- Создание привычек
- Установка частоты выполнения
- Настройка напоминаний
- AI-рекомендации
- Идея дня
- Отслеживание прогресса

## База данных

### Схема базы данных

#### Users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Tasks
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'new',
    priority INTEGER DEFAULT 1,
    color TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

#### Habits
```sql
CREATE TABLE habits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    frequency TEXT NOT NULL,
    reminder_time TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

## Взаимодействие с AI

### Интеграция с Ollama

Приложение использует локальный AI сервис Ollama для:
1. Анализа задач и предложения способов их выполнения
2. Генерации идей для саморазвития
3. Рекомендаций по улучшению привычек

#### Пример взаимодействия:
```python
response = requests.post(
    f"{Config.AI_HOST}:{Config.AI_PORT}/api/generate",
    json={
        "model": "llama2",
        "prompt": prompt,
        "stream": False
    }
)
```

### Типы AI-анализа

1. Анализ задач:
```python
prompt = f"""Проанализируй следующую задачу и предложи 
эффективный способ её выполнения: {task_description}"""
```

2. Генерация идеи дня:
```python
prompt = """Сгенерируй одну интересную идею для саморазвития на сегодня.
Идея должна быть конкретной и выполнимой за один день."""
```

3. Улучшение привычек:
```python
prompt = f"""Предложи способ улучшить выполнение следующей привычки: 
{habit_name}. Дай конкретный совет."""
```

## Инструкции по использованию

### 1. Запуск приложения
```bash
python src/main.py
```

### 2. Авторизация
1. Введите имя пользователя (минимум 3 символа)
2. Введите пароль (минимум 6 символов)
3. Нажмите "Войти" или "Регистрация"

### 3. Управление задачами
1. Создание задачи:
   - Введите название и описание
   - Выберите тип (простая/срочная)
   - Нажмите кнопку добавления

2. Работа с задачами:
   - ✓ - изменение статуса
   - ↑↓ - изменение приоритета
   - 🤖 - AI-анализ
   - ✕ - удаление

3. Фильтрация и поиск:
   - Используйте поле поиска
   - Выберите статус
   - Настройте сортировку

### 4. Управление привычками
1. Создание привычки:
   - Введите название
   - Выберите частоту
   - Установите время напоминания

2. Работа с привычками:
   - Отмечайте выполнение
   - Используйте AI-рекомендации
   - Получайте идею дня

### 5. Настройка темы
- Используйте кнопку 🌓 для переключения темы

### 6. Статистика
- Отслеживайте прогресс в разделе задач:
  - Общее количество задач
  - Завершенные задачи
  - Задачи в работе
  - Процент выполнения
