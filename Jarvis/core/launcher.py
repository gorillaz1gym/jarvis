import os
import webbrowser

# ======================
# 🧩 БАЗА ПРИЛОЖЕНИЙ
# ======================
APPS = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "discord": r"C:\Users\Gorillaz\AppData\Local\Discord\Update.exe --processStart Discord.exe",
    "steam": r"C:\Program Files (x86)\Steam\Steam.exe",
    "opera": r"C:\Users\Gorillaz\AppData\Local\Programs\Opera\launcher.exe"
}

# ======================
# 🌐 БАЗА САЙТОВ
# ======================
SITES = {
    "youtube": "https://youtube.com",
    "google": "https://google.com",
    "github": "https://github.com",
    "chatgpt": "https://chat.openai.com",
    "discord_web": "https://discord.com/app"
}


# ======================
# 🚀 ЗАПУСК ПРИЛОЖЕНИЙ
# ======================
def launch_app(name: str):
    name = name.lower()

    if name in APPS:
        print(f"[JARVIS] Запускаю приложение: {name}")
        os.startfile(APPS[name])
    else:
        print(f"[JARVIS] Приложение не найдено: {name}")


# ======================
# 🌐 ОТКРЫТИЕ САЙТОВ
# ======================
def open_site(name: str):
    name = name.lower()

    if name in SITES:
        print(f"[JARVIS] Открываю сайт: {name}")
        webbrowser.open(SITES[name])
    else:
        print(f"[JARVIS] Сайт не найден: {name}")


# ======================
# 🧠 ГЛАВНЫЙ РОУТЕР
# ======================
def handle_command(command: str):
    command = command.lower()

    # приложения
    if command.startswith("app "):
        app_name = command.replace("app ", "")
        launch_app(app_name)

    # сайты
    elif command.startswith("site "):
        site_name = command.replace("site ", "")
        open_site(site_name)

    else:
        print("[JARVIS] Не понял команду")