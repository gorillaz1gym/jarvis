import cv2
import numpy as np
import pyautogui
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def screenshot():
    img = pyautogui.screenshot()
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


def read_screen():

    img = screenshot()

    text = pytesseract.image_to_string(
        img,
        lang="rus+eng"
    )

    return text


def find_text(text_to_find):

    img = screenshot()

    data = pytesseract.image_to_data(
        img,
        lang="rus+eng",
        output_type=pytesseract.Output.DICT
    )

    for i, word in enumerate(data["text"]):

        if not word:
            continue

        word = word.lower().strip()

        if text_to_find.lower() in word:

            x = data["left"][i]
            y = data["top"][i]
            w = data["width"][i]
            h = data["height"][i]

            return (
                x + w // 2,
                y + h // 2
            )

    return None