import time

from voice.listener import listen
from voice.speaker import Speaker
from voice.wake_word import wait_for_wake_word

from core.brain import Brain
import control.windows as windows

from vision.vision_executor import execute_vision_plan


# =====================
# INIT
# =====================

speaker = Speaker()
brain = Brain()

speaker.speak("JARVIS запущен", "system")

print("🚀 SYSTEM READY")


# =====================
# ROUTER
# =====================

def route(text: str):
    prompt = f"""
Ты AI-роутер Jarvis.

Определи режим:

1) CHAT:
{{"type":"chat","text":"..." }}

2) ACTION:
[
  {{"type":"app|web","name":"..."}}
]

3) VISION:
{{"type":"vision_action","task":"..."}}

ПРАВИЛА:
- только JSON
- без текста
- без объяснений

КОМАНДА:
{text}
"""
    return brain.ask(prompt)


# =====================
# MAIN LOOP
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

            # =====================
            # 💬 CHAT MODE
            # =====================
            if isinstance(result, dict) and result.get("type") == "chat":
                speaker.speak(result.get("text", ""), "assistant")
                continue

            # =====================
            # ⚙️ ACTION MODE
            # =====================
            if isinstance(result, list):
                if len(result) == 0:
                    speaker.speak("Не понял команду", "warning")
                    continue

                for action in result:
                    windows.execute(action)

                speaker.speak("Готово", "assistant")
                continue

            # =====================
            # 👁 VISION MODE
            # =====================
            if isinstance(result, dict) and result.get("type") == "vision_action":

                task = result.get("task", "")

                speaker.speak("Смотрю экран", "assistant")

                execute_vision_plan({
                    "action": "search",
                    "text": task.replace("найди", "").strip()
                })

                speaker.speak("Готово", "assistant")
                continue

        except Exception as e:
            speaker.speak("Ошибка в обработке команды", "error")
            print("ERROR:", e)