import os
import webbrowser


# =========================
# 🌐 WEB APPS
# =========================
WEB_APPS = {
    "youtube": "https://youtube.com",
    "google": "https://google.com",
    "chatgpt": "https://chat.openai.com",
    "instagram": "https://instagram.com",
    "tiktok": "https://tiktok.com",
    "music": "https://music.yandex.ru"
}


# =========================
# 🚀 EXECUTOR
# =========================
def execute(action: dict):

    t = action.get("type")
    name = action.get("name", "").lower().strip()

    # 🌐 WEB
    if t == "web":
        url = WEB_APPS.get(name, f"https://{name}.com")
        print(f"[WINDOWS] opening web: {url}")
        webbrowser.open(url)
        return True

    # 💻 APP
    if t == "app":

        print(f"[WINDOWS] launching app: {name}")

        # 🎯 OPERA GX (твой браузер)
        if "opera" in name:
            paths = [
                r"C:\Program Files\Opera GX\launcher.exe",
                r"C:\Users\%USERNAME%\AppData\Local\Programs\Opera GX\launcher.exe"
            ]

            for p in paths:
                p = os.path.expandvars(p)
                if os.path.exists(p):
                    os.startfile(p)
                    return True

            os.system("start opera gx")
            return True

        # 🎯 YANDEX MUSIC
        if "yandex" in name or "music" in name:
            paths = [
                r"C:\Users\%USERNAME%\AppData\Local\Programs\YandexMusic\Яндекс Музыка.exe",
                r"C:\Program Files\Yandex Music\YandexMusic.exe"
            ]

            for p in paths:
                p = os.path.expandvars(p)
                if os.path.exists(p):
                    os.startfile(p)
                    return True

            webbrowser.open("https://music.yandex.ru")
            return True

        # 🎯 DEFAULT WINDOWS LAUNCH
        try:
            os.system(f'start "" "{name}"')
            return True
        except:
            print(f"[WINDOWS] failed: {name}")
            return False