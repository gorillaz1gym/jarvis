import json
from openai import OpenAI


client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)


class Brain:

    def ask(self, user_text: str, screen_state: str = None):

        if not screen_state:
            screen_state = "SCREEN NOT AVAILABLE"

        system_prompt = """
Ты JARVIS.

Отвечай ТОЛЬКО валидным JSON.

Форматы:

CHAT:
{"type":"chat","text":"..."}

ACTION:
{
  "type":"action",
  "actions":[
    {
      "type":"open|close|minimize|maximize|focus",
      "name":"..."
    }
  ]
}

VISION:
{
  "type":"vision",
  "task":"..."
}

Правила:

- только JSON
- никакого markdown
- никаких пояснений
- никаких мыслей
- если не уверен → CHAT
- если пользователь хочет открыть программу или сайт → ACTION
- если нужно понять содержимое экрана → VISION
"""

        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content":
                    f"USER: {user_text}\n"
                    f"SCREEN: {screen_state}"
            }
        ]

        try:
            res = client.chat.completions.create(
                model="qwen3:8b",
                messages=messages,
                temperature=0.1,
                max_tokens=150
            )

            raw = res.choices[0].message.content.strip()

            print("🧠 RAW:", raw)

            parsed = self._safe_parse(raw)

            return self._normalize(parsed)

        except Exception as e:
            print("[BRAIN ERROR]", e)

            return {
                "type": "chat",
                "text": "brain offline"
            }

    def _safe_parse(self, text: str):

        text = (
            text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:
            return json.loads(text)

        except Exception:
            return {
                "type": "chat",
                "text": text
            }

    def _normalize(self, data):

        if isinstance(data, list):
            return {
                "type": "action",
                "actions": data
            }

        if not isinstance(data, dict):
            return {
                "type": "chat",
                "text": "invalid format"
            }

        t = str(
            data.get("type", "")
        ).lower()

        if t == "chat":
            return {
                "type": "chat",
                "text": data.get("text", "")
            }

        if t == "action":
            return {
                "type": "action",
                "actions": data.get("actions", [])
            }

        if t == "vision":
            return {
                "type": "vision",
                "task": data.get("task", "")
            }

        return {
            "type": "chat",
            "text": "invalid format"
        }