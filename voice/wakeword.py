import speech_recognition as sr
import time

mic = sr.Microphone()
rec = sr.Recognizer()

rec.dynamic_energy_threshold = True

_last_trigger = 0
COOLDOWN = 2.5


def wait_for_wake_word():
    global _last_trigger

    with mic as source:
        rec.adjust_for_ambient_noise(source, duration=0.2)

        print("👂 WakeWord v5 listening...")

        audio = rec.listen(source, timeout=3, phrase_time_limit=3)

    try:
        text = rec.recognize_google(audio, language="ru-RU").lower()

        print("🎧 HEARD:", text)

        if "джарвис" in text:

            now = time.time()

            if now - _last_trigger < COOLDOWN:
                return False

            _last_trigger = now
            print("🔥 WAKE WORD TRIGGERED")
            return True

    except:
        return False

    return False