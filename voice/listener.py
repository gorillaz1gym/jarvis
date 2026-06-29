import speech_recognition as sr
import time

recognizer = sr.Recognizer()
mic = sr.Microphone()

_last = ""
_last_time = 0

recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8

with mic as source:
    recognizer.adjust_for_ambient_noise(source, duration=1)


def listen(speaker=None):
    global _last, _last_time

    try:
        with mic as source:
            print("🎤 Слушаю...")

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=6
            )

        text = recognizer.recognize_google(audio, language="ru-RU")
        text = text.lower().strip()

        print("👤 Ты:", text)

        # 🔥 анти-дубль (работает нормально)
        now = time.time()

        if text == _last and (now - _last_time) < 1.5:
            return ""

        _last = text
        _last_time = now

        # 🔥 защита от самоговорения
        if speaker and getattr(speaker, "is_speaking", False):
            return ""

        return text

    except sr.WaitTimeoutError:
        return ""

    except sr.UnknownValueError:
        return ""

    except sr.RequestError:
        return ""

    except OSError:
        return ""

    except Exception as e:
        print("LISTENER ERROR:", e)
        return ""