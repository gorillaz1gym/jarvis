APPS = {
    "браузер": "chrome",
    "chrome": "chrome",
    "яндекс": "C:\\Program Files\\Yandex\\YandexBrowser\\Application\\browser.exe",
    "yandex": "C:\\Program Files\\Yandex\\YandexBrowser\\Application\\browser.exe",
    "discord": "discord",
    "телеграм": "telegram",
    "telegram": "telegram"
}

def resolve(name: str):
    name = name.lower().strip()

    return APPS.get(name, None)