import speech_recognition as sr

def listen():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Слушаю...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="ru-RU")
        print(f"Ты сказал: {text}")
        return text

    except Exception:
        return ""