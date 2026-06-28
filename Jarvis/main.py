import time
import json

from voice.listener import listen
from voice.speaker import Speaker
from voice.wake_word import wait_for_wake_word

from core.brain import Brain
import control.windows as windows


# =====================
# INIT
# =====================

speaker = Speaker()
brain = Brain()

speaker.speak("JARVIS запущен", "system")

print("🚀 SYSTEM READY")


# =====================
# 🧠 SMART ROUTER
# =====================
def route(text: str):

    prompt = f"""
Ты AI-роутер Jarvis.

Твоя задача:
определить это команда или разговор.

ДОСТУПНЫЕ РЕЖИМЫ:

1) ACTION (если команда):
[
  {{"type": "app|web", "name": "..."}}
]

2) CHAT (если разговор):
{{
  "type": "chat",
  "text": "ответ пользователю"
}}

ПРАВИЛА:
- всегда отвечай JSON
- без объяснений
- без текста вне JSON

ПРИМЕРЫ:

вход: привет
выход: {{"type":"chat","text":"Привет!"}}

вход: как дела
выход: {{"type":"chat","text":"Всё отлично, я готов."}}

вход: открой браузер
выход: [{{"type":"app","name":"opera gx"}}]

вход: включи музыку
выход: [{{"type":"app","name":"yandex music"}}]

КОМАНДА:
{text}
"""

    res = brain.ask(prompt)

    return res


# =====================
# LOOP
# =====================

while True:

    print("👂 waiting wake word...")

    if not wait_for_wake_word():
        continue

    speaker.speak("Да, слушаю", "assistant")

    while True:

        text = listen(speaker)

        if not text:
            continue

        text = text.lower().strip()

        if "спать" in text:
            speaker.speak("Отключаюсь", "warning")
            break

        try:
            result = route(text)

            # 🧠 CHAT MODE
            if isinstance(result, dict) and result.get("type") == "chat":
                speaker.speak(result.get("text", ""), "assistant")
                continue

            # ⚙️ ACTION MODE
            if isinstance(result, list):
                if len(result) == 0:
                    speaker.speak("Не понял команду", "warning")
                    continue

                for action in result:
                    windows.execute(action)

                speaker.speak("Готово", "assistant")
                continue

            speaker.speak("Ошибка интерпретации", "warning")

        except Exception as e:
            print("ERROR:", e)
            speaker.speak("Ошибка системы", "error")

        time.sleep(0.05)