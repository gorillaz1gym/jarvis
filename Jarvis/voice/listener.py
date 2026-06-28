import speech_recognition as sr
import time
import re

recognizer = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
    recognizer.adjust_for_ambient_noise(source, duration=1)


def clean(text: str) -> str:
    return text.lower().strip()


def is_noise(text: str) -> bool:
    """
    Фильтр мусорных / системных фраз
    """

    if not text:
        return True

    text = text.lower()

    # 🔥 отсечь системные/битые ответы
    bad_phrases = [
        "ошибка обработки команды",
        "системный режим",
        "джарвис запущен",
        "assistant",
        "jarvis",
        "[системный режим]"
    ]

    if any(p in text for p in bad_phrases):
        return True

    # слишком короткое
    if len(text) < 2:
        return True

    return False


def listen(speaker=None):
    try:
        with mic as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)

        text = recognizer.recognize_google(audio, language="ru-RU")

        text = clean(text)

        # 🔥 1. не слушаем себя
        if speaker and getattr(speaker, "is_speaking", False):
            return ""

        # 🔥 2. фильтр мусора
        if is_noise(text):
            return ""

        return text

    except sr.UnknownValueError:
        return ""

    except sr.WaitTimeoutError:
        return ""

    except sr.RequestError:
        return ""

    except Exception as e:
        print("LISTENER ERROR:", e)
        return ""