import pyautogui
import time

from vision.ocr import find_text


def click_text(text):

    pos = find_text(text)

    if not pos:
        return False

    x, y = pos

    pyautogui.moveTo(
        x,
        y,
        duration=0.2
    )

    pyautogui.click()

    return True


def search_text(text):

    if not click_text("поиск"):
        if not click_text("search"):
            return False

    time.sleep(0.5)

    pyautogui.write(
        text,
        interval=0.03
    )

    pyautogui.press("enter")

    return True


def execute_vision_plan(plan):

    if not isinstance(plan, dict):
        return

    action = plan.get("action")

    if action == "click_text":
        click_text(plan.get("text", ""))

    elif action == "search":
        search_text(plan.get("text", ""))