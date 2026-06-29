from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)


class Brain:

    def ask(self, user_text, context=""):

        system = """
Ты JARVIS AI.

ОТВЕЧАЙ ТОЛЬКО JSON:

{
  "type": "chat | action",
  "text": "",
  "actions": [{"type":"open","name":"browser"}]
}

ПРАВИЛА:
- без текста вне JSON
- если команда → action
- иначе → chat
"""

        messages = [
            {"role": "system", "content": system},
        ]

        if context:
            messages.append({"role": "system", "content": f"MEMORY:\n{context}"})

        messages.append({"role": "user", "content": user_text})

        res = client.chat.completions.create(
            model="qwen3:8b",
            messages=messages,
            max_tokens=80,
            temperature=0.2,
        )

        text = res.choices[0].message.content.strip()

        try:
            import json
            return json.loads(text)
        except:
            return {"type": "chat", "text": text}