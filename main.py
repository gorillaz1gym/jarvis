import time
from voice.listener import listen
from voice.speaker import Speaker
from core.brain import Brain

speaker = Speaker()
brain = Brain()

print("🚀 JARVIS READY")

last_text = None
processing = False

while True:

    if processing:
        time.sleep(0.1)
        continue

    text = listen(speaker)

    if not text:
        continue

    text = text.strip().lower()

    # анти-дубль
    if text == last_text:
        continue

    last_text = text

    print(f"👤 Ты: {text}")

    processing = True

    try:
        result = brain.ask(text)

        print("🧠 RAW:", result)

        if not isinstance(result, dict):
            processing = False
            continue

        t = result.get("type")

        if t == "chat":
            msg = result.get("text", "")

            # защита от сломанного JSON в строке
            if isinstance(msg, str):
                if msg.strip().startswith("{"):
                    try:
                        import json
                        msg = json.loads(msg).get("text", msg)
                    except:
                        pass

            if msg:
                speaker.speak(msg, "assistant")

        elif t == "action":
            speaker.speak("выполняю команду", "assistant")

        else:
            speaker.speak("не понял", "assistant")

    except Exception as e:
        print("ERROR:", e)
        speaker.speak("ошибка", "assistant")

    processing = False
    time.sleep(0.2)