import pyautogui

def take_screenshot(path="screen.png"):
    img = pyautogui.screenshot()
    img.save(path)
    return path