import time

from voice.listener import listen
from voice.speaker import Speaker
from voice.wakeword import wait_for_wake_word

from core.brain import Brain
import control.windows as windows


class JarvisEngine:

    def __init__(self):
        self.speaker = Speaker()
        self.brain = Brain()

        self.last_text = ""

        print("🚀 JARVIS v5 READY")
        self.speaker.speak("Джарвис запущен", "system")

    # =========================
    # MAIN LOOP (STATE MACHINE)
    # =========================
    def run(self):

        while True:

            # 1. WAIT WAKEWORD
            print("👂 WakeWord v5 listening...")

            wait_for_wake_word()

            # ⚠️ СБРОС БУФЕРА после wakeword
            time.sleep(0.3)

            self.speaker.speak("Да, слушаю", "assistant")

            # 2. SESSION MODE
            self.session()

    # =========================
    # SESSION MODE
    # =========================
    def session(self):

        while True:

            text = listen(self.speaker)

            if not text:
                continue

            print("👤 USER:", text)

            # 🔥 выход из режима
            if "спать" in text or "стоп" in text:
                self.speaker.speak("Отключаюсь", "system")
                return

            # анти-дубль
            if text == self.last_text:
                continue

            self.last_text = text

            try:
                result = self.brain.ask(text)
                self.handle(result)

            except Exception as e:
                print("ENGINE ERROR:", e)
                self.speaker.speak("Ошибка системы", "error")

            time.sleep(0.2)

    # =========================
    # HANDLER
    # =========================
    def handle(self, result):

        if not isinstance(result, dict):
            self.speaker.speak("Ошибка ответа", "error")
            return

        t = result.get("type")

        if t == "chat":
            text = result.get("text", "")
            if text:
                self.speaker.speak(text, "assistant")

        elif t == "action":
            failures = 0

            for a in result.get("actions", []):
                if windows.execute(a) != "ok":
                    failures += 1

            self.speaker.speak(
                "Сделано" if failures == 0 else "Есть проблемы",
                "assistant"
            )

        elif t == "vision":
            self.speaker.speak("Анализирую экран", "assistant")

        else:
            self.speaker.speak("Не понял команду", "assistant")