import asyncio
import edge_tts
import tempfile
import os
import threading
import queue
import time
from playsound import playsound


class Speaker:
    def __init__(self):
        self.q = queue.Queue()
        self.running = True

        self.voice = "ru-RU-DmitryNeural"

        # 🔥 флаг чтобы микрофон НЕ слушал пока он говорит
        self.is_speaking = False

        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

        print("🔊 Speaker ready")

    def speak(self, text: str, emotion: str = "assistant"):
        self.q.put((text, emotion))

    def _worker(self):
        while self.running:
            try:
                text, emotion = self.q.get(timeout=0.1)

                self.is_speaking = True  # 🔥 ВКЛ МУТ МОД

                print("🗣️ JARVIS:", text)

                asyncio.run(self._speak(text))

                time.sleep(0.3)
                self.is_speaking = False  # 🔥 ВЫКЛ МУТ МОД

            except queue.Empty:
                continue

            except Exception as e:
                print("SPEAKER ERROR:", e)
                self.is_speaking = False

    async def _speak(self, text):
        tmp_file = tempfile.mktemp(suffix=".mp3")

        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(tmp_file)

        playsound(tmp_file)

        try:
            os.remove(tmp_file)
        except:
            pass