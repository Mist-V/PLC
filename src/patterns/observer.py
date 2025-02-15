from abc import ABC, abstractmethod
from typing import List

class Observer(ABC):
    """
    Абстрактный класс наблюдателя
    """
    @abstractmethod
    def update(self, message: str):
        pass

class Subject:
    """
    Субъект, за которым наблюдают (например, система напоминаний)
    """
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        """Добавление наблюдателя"""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        """Удаление наблюдателя"""
        self._observers.remove(observer)

    def notify(self, message: str):
        """Уведомление всех наблюдателей"""
        for observer in self._observers:
            observer.update(message)

class NotificationManager(Subject):
    """
    Менеджер уведомлений, реализующий паттерн Observer
    """
    def __init__(self):
        super().__init__()
        self._notifications = []

    def add_notification(self, message: str):
        """Добавление нового уведомления"""
        self._notifications.append(message)
        self.notify(message)
