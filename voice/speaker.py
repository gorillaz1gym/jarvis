import asyncio
import edge_tts
import tempfile
import os
import threading
import queue
from playsound import playsound


class Speaker:
    def __init__(self):
        self.q = queue.Queue()
        self.running = True
        self.is_speaking = False

        self.voice = "ru-RU-DmitryNeural"

        self.thread = threading.Thread(
            target=self._worker,
            daemon=True
        )
        self.thread.start()

        print("🔊 JARVIS Voice Engine активирован")

    def speak(self, text: str, emotion="assistant"):

        if not text:
            return

        text = str(text).strip()

        if not text:
            return

        styled_text = self._apply_emotion(text, emotion)
        self.q.put((styled_text, emotion))

    def _apply_emotion(self, text, emotion):

        if emotion == "system":
            return text

        if emotion == "warning":
            return f"Внимание. {text}"

        if emotion == "success":
            return f"Готово. {text}"

        return text

    def _worker(self):
        while self.running:
            try:
                text, emotion = self.q.get(timeout=0.1)

                print(f"🤖 Jarvis: {text}")

                self.is_speaking = True
                asyncio.run(self._speak(text))
                self.is_speaking = False

            except queue.Empty:
                continue

            except Exception as e:
                self.is_speaking = False
                print("SPEAKER ERROR:", e)

    async def _speak(self, text):

        temp_file = tempfile.mktemp(suffix=".mp3")

        try:
            communicate = edge_tts.Communicate(
                text,
                self.voice
            )

            await communicate.save(temp_file)

            playsound(temp_file)

        finally:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass