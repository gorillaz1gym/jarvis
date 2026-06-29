import time
import pyautogui
import pygetwindow as gw


def find_window(name: str):
    import pygetwindow as gw

    name = name.lower()

    for w in gw.getAllWindows():
        if w.title and name in w.title.lower():
            return w

    # 🔥 fallback: более агрессивный поиск
    for w in gw.getAllWindows():
        if w.title:
            if any(part in w.title.lower() for part in name.split()):
                return w

    return None


def fallback_open(name: str):
    pyautogui.hotkey("win", "s")
    time.sleep(0.7)

    pyautogui.write(name, interval=0.05)
    time.sleep(0.6)

    pyautogui.press("enter")

    return "opened"


def force_focus(window):
    try:
        window.restore()
        time.sleep(0.2)
        window.activate()
        return True
    except:
        return False


def execute(action: dict):

    if not isinstance(action, dict):
        return "fail"

    t = action.get("type", "").lower()
    name = action.get("name", "").lower()

    if not t or not name:
        return "fail"

    aliases = {
        "browser": "chrome",
        "google": "chrome",
        "музыка": "spotify",
        "music": "spotify"
    }

    name = aliases.get(name, name)

    w = find_window(name)

    if t == "open":
        if w:
            if force_focus(w):
                return "ok"
        return fallback_open(name)

    if t == "close":
        if w:
            w.close()
            return "ok"
        return "fail"

    if t == "minimize":
        if w:
            w.minimize()
            return "ok"
        return "fail"

    if t == "maximize":
        if w:
            w.maximize()
            return "ok"
        return "fail"

    if t == "focus":
        if w:
            if force_focus(w):
                return "ok"
        return "fail"

    return "fail"