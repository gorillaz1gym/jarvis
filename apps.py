import os
import difflib

APPS = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "discord": r"C:\Users\%Gorillaz%\AppData\Local\Discord\Update.exe --processStart Discord.exe",
    "steam": r"C:\Program Files (x86)\Steam\Steam.exe",
    "spotify": r"C:\Users\%Gorillaz%\AppData\Roaming\Spotify\Spotify.exe",
    "notepad": "notepad.exe"
}

def find_best_match(command: str):
    command = command.lower().strip()

    matches = difflib.get_close_matches(command, APPS.keys(), n=1, cutoff=0.3)

    return matches[0] if matches else None


def open_app(command: str):
    app = find_best_match(command)

    if not app:
        print("🔴 Jarvis: приложение не найдено")
        return

    path = os.path.expandvars(APPS[app])

    print(f"🟢 Jarvis: запускаю {app}")

    try:
        os.startfile(path)
    except:
        print("🔴 Ошибка запуска, пробую через start cmd")
        os.system(f'start "" "{path}"')