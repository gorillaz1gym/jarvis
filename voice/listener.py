import speech_recognition as sr
import time

recognizer = sr.Recognizer()
mic = sr.Microphone()

# стабильность
recognizer.dynamic_energy_threshold = False
recognizer.pause_threshold = 0.6

_last_text = ""
_last_time = 0

# калибровка шума ОДИН раз
with mic as source:
    recognizer.adjust_for_ambient_noise(source, duration=0.5)


def listen(speaker=None):
    global _last_text, _last_time

    try:
        with mic as source:
            print("🎤 listen...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)

        text = recognizer.recognize_google(audio, language="ru-RU")
        text = text.lower().strip()

        if not text:
            return ""

        # 🔥 не слушаем себя
        if speaker and getattr(speaker, "is_speaking", False):
            return ""

        # 🔥 анти-дубль
        now = time.time()
        if text == _last_text and (now - _last_time) < 1.5:
            return ""

        _last_text = text
        _last_time = now

        print("👤 USER:", text)
        return text

    except sr.WaitTimeoutError:
        return ""

    except sr.UnknownValueError:
        return ""

    except sr.RequestError:
        return ""

    except Exception as e:
        print("LISTENER ERROR:", e)
        return ""