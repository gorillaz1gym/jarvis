import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)

MODELS = [
    "openai/gpt-4o-mini",
    "anthropic/claude-3-haiku",
]


class Brain:

    def ask(self, text: str):

        messages = [
            {
                "role": "system",
                "content": """
Ты — Jarvis.

Ты можешь работать в 2 режимах:

1) CHAT:
если это разговор → ответ:
{"type":"chat","text":"..."}

2) ACTION:
если это команда → ответ:
[
  {"type":"app|web","name":"..."}
]
3) VISION:

{
  "type":"vision_action",
  "task":"..."
}

ПРАВИЛА:
- если сомнение → CHAT
- не ломай JSON
- не пиши объяснений
"""
            },
            {"role": "user", "content": text}
        ]

        for model in MODELS:
            try:
                res = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.3
                )

                content = res.choices[0].message.content.strip()

                return self._safe_parse(content)

            except Exception as e:
                print("[BRAIN FAIL]", model, e)

        return {"type": "chat", "text": "Brain offline"}


    def _safe_parse(self, text: str):

        try:
            return json.loads(text)
        except:
            pass

        text = text.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(text)
        except:
            pass

        start = text.find("[")
        end = text.rfind("]")

        if start != -1 and end != -1:
            try:
                return json.loads(text[start:end+1])
            except:
                pass

        return {"type": "chat", "text": text}