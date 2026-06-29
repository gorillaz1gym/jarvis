import asyncio
import edge_tts
import tempfile
import os
import threading
from playsound import playsound


class Speaker:

    def __init__(self):
        self.voice = "ru-RU-DmitryNeural"
        self.is_speaking = False
        print("🔊 Voice Engine v5")

    def speak(self, text, emotion="assistant"):
        if not text:
            return

        text = str(text).strip()

        print(f"🤖 JARVIS: {text}")

        threading.Thread(
            target=lambda: asyncio.run(self._speak(text)),
            daemon=True
        ).start()

    async def _speak(self, text):
        self.is_speaking = True

        file = tempfile.mktemp(".mp3")

        try:
            tts = edge_tts.Communicate(text, self.voice)
            await tts.save(file)

            playsound(file)

        finally:
            self.is_speaking = False
            try:
                os.remove(file)
            except:
                pass