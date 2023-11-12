import pyautogui
from PIL import ImageGrab, ImageOps

last_value = (0, 0)
while True:
    if(pyautogui.position() != last_value):
        last_value = pyautogui.position()
        print("x: "+str(last_value[0]))
        print("y: "+str(last_value[1]))
        screenshot = ImageGrab.grab()
        gray_img = ImageOps.grayscale(screenshot)
        print("value: "+str(gray_img.getpixel(last_value)))
        print()
