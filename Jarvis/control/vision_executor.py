import pyautogui
import time


def execute_vision_plan(text: str):
    """
    Пока v1 — простой executor
    (в будущем сделаем координаты + OCR)
    """

    print("[VISION PLAN]", text)

    # очень простой MVP-режим:
    if "youtube" in text.lower():
        pyautogui.hotkey("win", "r")
        time.sleep(0.5)
        pyautogui.write("https://youtube.com")
        pyautogui.press("enter")
        return

    if "поиск" in text.lower():
        pyautogui.press("/")
        return

    if "воспроизвести" in text.lower():
        pyautogui.press("k")
        return