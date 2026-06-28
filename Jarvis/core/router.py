import json

class AIRouter:

    def __init__(self, brain):
        self.brain = brain

    def parse(self, text: str):
        """
        AI превращает текст в действия
        """

        prompt = f"""
Ты — AI роутер для ассистента Jarvis.

Преобразуй команду пользователя в JSON массив действий.

Доступные типы:
- app (запуск приложения)
- web (открыть сайт)

Правила:
- отвечай ТОЛЬКО JSON
- без текста
- без объяснений

Примеры:

вход: открой браузер
выход:
[{{"type":"app","name":"opera gx"}}]

вход: включи музыку
выход:
[{{"type":"app","name":"yandex music"}}]

вход: открой ютуб
выход:
[{{"type":"web","name":"youtube"}}]

Теперь команда:
{text}
"""

        response = self.brain.ask(prompt)

        try:
            return json.loads(response)
        except:
            return []