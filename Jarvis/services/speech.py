import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()

# настройка голоса
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # 0 = мужской, 1 = женский
engine.setProperty('rate', 180)


def speak(text: str):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Слушаю...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio, language="ru-RU")
        print("Ты:", command)
        return command

    except sr.UnknownValueError:
        return ""

    except sr.RequestError:
        return "ошибка сервиса распознавания"