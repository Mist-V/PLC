import requests
from typing import Optional
from src.config import Config

class AIService:
    """
    Сервис для работы с локальной нейросетью (Ollama)
    """
    def __init__(self):
        self.base_url = f"{Config.AI_HOST}:{Config.AI_PORT}"
        self.model = "llama2"  # Модель по умолчанию

    def generate_response(self, prompt: str) -> Optional[str]:
        """
        Генерация ответа от нейросети
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                return response.json().get('response')
            return None
        except Exception as e:
            print(f"Ошибка при обращении к AI сервису: {e}")
            return None

    def generate_daily_idea(self) -> str:
        """
        Генерация идеи дня
        """
        prompt = """Сгенерируй одну интересную идею для саморазвития на сегодня.
        Идея должна быть конкретной и выполнимой за один день."""
        
        response = self.generate_response(prompt)
        return response if response else "Не удалось сгенерировать идею дня"

    def analyze_task(self, task_description: str) -> str:
        """
        Анализ задачи и предложение по её выполнению
        """
        prompt = f"""Проанализируй следующую задачу и предложи 
        эффективный способ её выполнения: {task_description}"""
        
        response = self.generate_response(prompt)
        return response if response else "Не удалось проанализировать задачу"

    def suggest_habit_improvement(self, habit_name: str) -> str:
        """
        Предложение по улучшению привычки
        """
        prompt = f"""Предложи способ улучшить выполнение следующей привычки: 
        {habit_name}. Дай конкретный совет."""
        
        response = self.generate_response(prompt)
        return response if response else "Не удалось получить рекомендацию"
