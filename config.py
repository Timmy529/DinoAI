import json
from PIL import ImageGrab, ImageOps
import pyautogui
import time
import numpy as np

def area_mean(area):
    """
    returns the mean value of a screen area
    :return: float
    """
    image = ImageGrab.grab(area)
    gray_img = ImageOps.grayscale(image)
    arr = np.array(gray_img.getcolors())
    return arr.mean()

input("select the top-left corner of the restart_area and press enter...")
restart_top_left = pyautogui.position()

input("select the bottom-right corner of the restart_area and press enter...")
restart_bottom_right = pyautogui.position()

restart_area = (restart_top_left[0], restart_top_left[1], restart_bottom_right[0], restart_bottom_right[1])

input("press enter to calculate the restart_mean...")
restart_mean = area_mean(restart_area)

input("select the restart button and press enter...")
restart_coord = pyautogui.position()

print("click restart, then click this window again")
time.sleep(3)

input("select the top-left corner of the lower detection area and press enter...")
low_detection_top_left = pyautogui.position()

input("select the bottom-right corner of the lower detection area and press enter...")
low_detection_bottom_right = pyautogui.position()

input("press enter to calculate the low_detection_mean...")
low_detection_area = (low_detection_top_left[0], low_detection_top_left[1], low_detection_bottom_right[0], low_detection_bottom_right[1])

low_detection_mean = area_mean(low_detection_area)

input("select the top-left corner of the upper detection area and press enter...")
high_detection_top_left = pyautogui.position()

input("select the bottom-right corner of the upper detection area and press enter...")
high_detection_bottom_right = pyautogui.position()

input("press enter to calculate the high_detection_mean...")
high_detection_area = (high_detection_top_left[0], high_detection_top_left[1], high_detection_bottom_right[0], high_detection_bottom_right[1])

high_detection_mean = area_mean(high_detection_area)

input("select the center of the dino and press enter...")
dino_coord = pyautogui.position()

screenshot = ImageGrab.grab()
dino_value = screenshot.getpixel(dino_coord)

input("select the ground truth (time) pixel and press enter...")
time_pixel = pyautogui.position()

epsilon = int(input("enter the acceptable range for error in values (epsilon): "))

config_data = {
    'restart_area': restart_area,
    'restart_mean': restart_mean,
    'restart_coord': restart_coord,
    'low_detection_area': low_detection_area,
    'low_detection_mean': low_detection_mean,
    'high_detection_area': high_detection_area,
    'high_detection_mean': high_detection_mean,
    'dino_coord': dino_coord,
    'dino_value': dino_value,
    'time_pixel': time_pixel,
    'epsilon': epsilon
}

# Writing to config.json
with open('config.json', 'w') as config_file:
    json.dump(config_data, config_file)

print("Configuration values have been saved to config.json.")
