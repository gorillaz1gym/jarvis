import pyautogui
import time


def click(x, y):
    pyautogui.moveTo(x, y, duration=0.2)
    pyautogui.click()


def type_text(text):
    pyautogui.write(text, interval=0.05)


def press(key):
    pyautogui.press(key)


def scroll(amount):
    pyautogui.scroll(amount)