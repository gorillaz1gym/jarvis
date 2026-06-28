import webbrowser
import subprocess
import datetime


def execute(action):
    if action == "open_browser":
        webbrowser.open("https://google.com")
        return "Открываю браузер"

    elif action == "open_steam":
        subprocess.Popen(
            r"C:\Program Files (x86)\Steam\Steam.exe"
        )
        return "Открываю Steam"

    elif action == "time":
        current_time = datetime.datetime.now().strftime("%H:%M")
        return f"Сейчас {current_time}"

    elif action == "weather":
        return "Модуль погоды пока не подключен"

    return "Я пока не умею выполнять эту команду"