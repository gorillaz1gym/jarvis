import time

from voice.listener import listen
from voice.speaker import Speaker
from voice.wake_word import wait_for_wake_word

from core.brain import Brain
from core.agent import Agent

from vision.screen import take_screenshot
from vision.vision_ai import analyze_screen

from control import windows


# =========================
# INIT
# =========================

speaker = Speaker()
brain = Brain()

# tools для агента (явно и безопасно)
class Tools:
    def open_browser(self):
        windows.open_app("chrome")

    def analyze_screen(self):
        img = take_screenshot()
        return analyze_screen(img)


tools = Tools()


# =========================
# AGENT (ВАЖНО: убираем intent/router/memory если их нет)
# =========================

agent = Agent(
    tools=tools,
    brain=brain
)


# стартовое сообщение
speaker.speak("JARVIS", "system")


# =========================
# MAIN LOOP
# =========================

while True:

    # ожидание wake word
    if not wait_for_wake_word():
        continue

    speaker.speak("Слушаю", "assistant")

    while True:

        text = listen(speaker)

        if not text:
            continue

        text = text.lower().strip()

        # выход в сон
        if "спать" in text or "выключись" in text:
            speaker.speak("Отключаюсь")
            break

        try:
            result = agent.run(text)

            # безопасный вывод
            response = result.get("text") if isinstance(result, dict) else str(result)

            speaker.speak(response, "assistant")

        except Exception as e:
            speaker.speak("Ошибка выполнения команды", "error")
            print("Agent error:", e)

        time.sleep(0.1)