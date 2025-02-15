from typing import List
from datetime import datetime, time
from src.db.models import Habit
from src.db.database import Database
from src.patterns.observer import NotificationManager

class HabitService:
    """
    Сервис для работы с привычками
    """
    def __init__(self):
        self.db = Database()
        self.notification_manager = NotificationManager()

    def create_habit(self, user_id: int, name: str, frequency: str,
                    reminder_time: str = None) -> Habit:
        """
        Создание новой привычки
        """
        try:
            if not self.db.connect():
                return None

            self.db.begin_transaction()
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            result = self.db.execute('''
                INSERT INTO habits (user_id, name, frequency, reminder_time, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, name, frequency, reminder_time, current_time))

            if not result:
                self.db.rollback()
                return None

            habit_id = result.lastrowid
            self.db.commit()

            return Habit(
                id=habit_id,
                user_id=user_id,
                name=name,
                frequency=frequency,
                reminder_time=reminder_time,
                created_at=datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
            )
        except Exception as e:
            print(f"Ошибка при создании привычки: {e}")
            self.db.rollback()
            return None
        finally:
            self.db.close()

    def get_user_habits(self, user_id: int) -> List[Habit]:
        """
        Получение всех привычек пользователя
        """
        try:
            if not self.db.connect():
                return []

            result = self.db.execute('SELECT * FROM habits WHERE user_id = ?', (user_id,))
            if not result:
                return []

            habits = []
            for row in result.fetchall():
                habits.append(Habit(
                    id=row[0],
                    user_id=row[1],
                    name=row[2],
                    frequency=row[3],
                    reminder_time=row[4],
                    created_at=datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S')
                ))
            return habits
        except Exception as e:
            print(f"Ошибка при получении привычек: {e}")
            return []
        finally:
            self.db.close()

    def update_habit(self, habit: Habit) -> bool:
        """
        Обновление привычки
        """
        try:
            if not self.db.connect():
                return False

            self.db.begin_transaction()
            result = self.db.execute('''
                UPDATE habits 
                SET name = ?, frequency = ?, reminder_time = ?
                WHERE id = ?
            ''', (habit.name, habit.frequency, habit.reminder_time, habit.id))

            if not result:
                self.db.rollback()
                return False

            self.db.commit()
            return True
        except Exception as e:
            print(f"Ошибка при обновлении привычки: {e}")
            self.db.rollback()
            return False
        finally:
            self.db.close()

    def delete_habit(self, habit_id: int) -> bool:
        """
        Удаление привычки
        """
        try:
            if not self.db.connect():
                return False

            self.db.begin_transaction()
            result = self.db.execute('DELETE FROM habits WHERE id = ?', (habit_id,))

            if not result:
                self.db.rollback()
                return False

            self.db.commit()
            return True
        except Exception as e:
            print(f"Ошибка при удалении привычки: {e}")
            self.db.rollback()
            return False
        finally:
            self.db.close()

    def check_reminders(self):
        """
        Проверка напоминаний о привычках
        """
        try:
            current_time = datetime.now().strftime("%H:%M")
            if not self.db.connect():
                return

            result = self.db.execute('''
                SELECT * FROM habits 
                WHERE reminder_time = ?
            ''', (current_time,))

            if not result:
                return

            for habit in result.fetchall():
                message = f"Напоминание: Время выполнить привычку '{habit[2]}'"
                self.notification_manager.add_notification(message)
        except Exception as e:
            print(f"Ошибка при проверке напоминаний: {e}")
        finally:
            self.db.close()