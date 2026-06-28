import speech_recognition as sr

def wait_for_wake_word():
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Listening for wake word...")

        audio = r.listen(source)

    try:
        text = r.recognize_google(audio).lower()
        return "jarvis" in text

    except:
        return False