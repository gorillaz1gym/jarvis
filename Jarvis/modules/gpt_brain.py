import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MODELS = [
    "google/gemini-2.0-flash-exp:free",
    "meta-llama/llama-3.1-8b-instruct:free",
    "deepseek/deepseek-chat-v3-0324",
]

class GPTBrain:

    def chat(self, messages):

        for model in MODELS:
            try:
                res = client.chat.completions.create(
                    model=model,
                    messages=messages
                )

                return {
                    "type": "chat",
                    "text": res.choices[0].message.content,
                    "model": model
                }

            except Exception as e:
                print("MODEL FAIL:", model)
                continue

        return {
            "type": "chat",
            "text": "Все модели недоступны",
            "model": None
        }