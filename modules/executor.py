import time
import pyautogui
import pygetwindow as gw


# =========================
# 🔍 WINDOW FINDER
# =========================
def find_window(name: str):
    name = name.lower()

    for w in gw.getAllWindows():
        if w.title and name in w.title.lower():
            return w

    return None


# =========================
# 🚀 FALLBACK OPEN
# =========================
def fallback_open(name: str):

    # открыть поиск Windows
    pyautogui.hotkey("win", "s")
    time.sleep(0.8)

    # очистить строку
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")

    time.sleep(0.2)

    # ввести название
    pyautogui.write(name, interval=0.05)

    time.sleep(0.6)

    # открыть результат
    pyautogui.press("enter")


# =========================
# ⚙️ MAIN EXECUTOR
# =========================
def execute(action: dict):

    if not isinstance(action, dict):
        return "fail"

    t = action.get("type", "")
    name_raw = action.get("name", "")

    if not name_raw:
        return "fail"

    name = name_raw.lower()

    # нормализация названий
    aliases = {
        "browser": "chrome",
        "google": "chrome",
        "музыка": "яндекс музыка",
        "music": "spotify"
    }

    name = aliases.get(name, name)

    w = find_window(name)

    # =====================
    # OPEN
    # =====================
    if t == "open":

        if w:
            try:
                w.activate()
                return "ok"
            except:
                fallback_open(name)
                return "fallback_used"
        else:
            fallback_open(name)
            return "fallback_used"

    # =====================
    # CLOSE
    # =====================
    elif t == "close":
        if w:
            try:
                w.close()
                return "ok"
            except:
                return "fail"
        return "fail"

    # =====================
    # MINIMIZE
    # =====================
    elif t == "minimize":
        if w:
            try:
                w.minimize()
                return "ok"
            except:
                return "fail"
        return "fail"

    # =====================
    # MAXIMIZE
    # =====================
    elif t == "maximize":
        if w:
            try:
                w.maximize()
                return "ok"
            except:
                return "fail"
        return "fail"

    # =====================
    # FOCUS
    # =====================
    elif t == "focus":
        if w:
            try:
                w.activate()
                return "ok"
            except:
                return "fail"
        return "fail"

    return "fail"