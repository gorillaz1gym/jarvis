import time
from vision.screen import take_screenshot
from vision.vision_ai import analyze_screen

latest_screen_state = "initializing"


def get_screen_state():
    return latest_screen_state


def vision_loop():

    global latest_screen_state

    while True:
        try:
            img_path = take_screenshot()

            result = analyze_screen(img_path)

            # 🔥 защита от мусора
            if not result:
                latest_screen_state = "empty"
            else:
                latest_screen_state = result

        except Exception as e:
            print("[VISION ERROR REAL]:", repr(e))

            # НЕ убиваем систему
            latest_screen_state = "vision_failed"

        time.sleep(1)