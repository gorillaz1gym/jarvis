import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY не найден в .env")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)

MODELS = [
    "openai/gpt-4o-mini",
    "anthropic/claude-3-haiku",
    "meta-llama/llama-3.1-8b-instruct",
]


class Brain:

    def think(self, text: str):
        messages = [
            {
                "role": "system",
                "content": "Ты JARVIS — умный ассистент. Отвечай кратко и по делу."
            },
            {
                "role": "user",
                "content": text
            }
        ]

        last_error = None

        for model in MODELS:
            try:
                res = client.chat.completions.create(
                    model=model,
                    messages=messages
                )

                content = res.choices[0].message.content

                return {
                    "text": content,
                    "model": model
                }

            except Exception as e:
                print("MODEL FAIL:", model, e)
                last_error = e
                continue

        return {
            "text": f"Brain offline: {last_error}"
        }