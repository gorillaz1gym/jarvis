import pyautogui

def click(x=None, y=None):
    if x and y:
        pyautogui.click(x, y)
    else:
        pyautogui.click()