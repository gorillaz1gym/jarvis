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

        self.voice = "ru-RU-DmitryNeural"

        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

        print("🔊 JARVIS Voice Engine активирован")

    # -------------------------
    # PUBLIC SPEAK METHOD
    # -------------------------
    def speak(self, text: str, emotion: str = "assistant"):
        styled_text = self._apply_emotion(text, emotion)
        self.q.put((styled_text, emotion))

    # -------------------------
    # EMOTION ENGINE
    # -------------------------
    def _apply_emotion(self, text: str, emotion: str):
        text = text.strip()

        if emotion == "system":
            return f"[системный режим] {text}"

        elif emotion == "warning":
            return f"Внимание. {text}"

        elif emotion == "success":
            return f"Готово. {text}"

        elif emotion == "assistant":
            return text

        return text

    # -------------------------
    # WORKER THREAD
    # -------------------------
    def _worker(self):
        while self.running:
            try:
                text, emotion = self.q.get(timeout=0.1)

                print(f"🗣️ ({emotion}) Jarvis:", text)

                asyncio.run(self._speak(text))

            except queue.Empty:
                continue

            except Exception as e:
                print("SPEAKER ERROR:", e)

    # -------------------------
    # EDGE TTS ENGINE
    # -------------------------
    async def _speak(self, text):
        temp_file = tempfile.mktemp(suffix=".mp3")

        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(temp_file)

        playsound(temp_file)

        try:
            os.remove(temp_file)
        except:
            pass