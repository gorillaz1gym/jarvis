import base64
import requests
import os

API_KEY = os.getenv("OPENROUTER_API_KEY")


def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def analyze_screen(image_path, task: str):

    img = encode_image(image_path)

    prompt = f"""
Ты — AI зрение ассистента Jarvis.

Пользователь хочет: {task}

На экране есть интерфейс (YouTube / музыка / приложения).

Твоя задача:
- объяснить где кликнуть
- что нажать
- что ввести

Отвечай КОРОТКО:
- шаги
- без лишнего текста
"""

    res = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}"
        },
        json={
            "model": "openai/gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{img}"
                            }
                        }
                    ]
                }
            ]
        }
    )

    try:
        return res.json()["choices"][0]["message"]["content"]
    except:
        return "vision_error"