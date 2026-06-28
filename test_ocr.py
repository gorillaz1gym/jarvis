import pyautogui
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

img = pyautogui.screenshot()
img.save("test.png")

text = pytesseract.image_to_string(
    img,
    lang="rus+eng"
)

print(text)