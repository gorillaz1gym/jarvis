import pyautogui

def take_screenshot():
    img = pyautogui.screenshot()
    img.save("screen.png")
    return "screen.png"