import json
from PIL import ImageGrab, ImageOps
import pyautogui
import numpy as np

input("select the top-left corner of the lower detection area and press enter...")
detection_top_left = pyautogui.position()

input("select the bottom-right corner of the lower detection area and press enter...")
detection_bottom_right = pyautogui.position()

detection_area = (detection_top_left[0], detection_top_left[1], detection_bottom_right[0], detection_bottom_right[1])

input("select the top_left of the dino and press enter...")
top_left_dino_coord = pyautogui.position()

input("select the bottom_right of the dino and press enter...")
bottom_right_dino_coord = pyautogui.position()

dino_area = (top_left_dino_coord[0], top_left_dino_coord[1], bottom_right_dino_coord[0], bottom_right_dino_coord[1])

input("select the max dino jump height and press enter...")
jump_coord = pyautogui.position()

input("select the ground truth (time) pixel and press enter...")
time_pixel = pyautogui.position()

input("select the top-left corner of the restart_area and press enter...")
restart_top_left = pyautogui.position()

input("select the bottom-right corner of the restart_area and press enter...")
restart_bottom_right = pyautogui.position()

restart_area = (restart_top_left[0], restart_top_left[1], restart_bottom_right[0], restart_bottom_right[1])

input("press enter to get the restart image...")
restart_image = ImageOps.grayscale(ImageGrab.grab(restart_area))

input("select the restart button and press enter...")
restart_coord = pyautogui.position()

epsilon = int(input("enter the acceptable range for error in values (epsilon): "))

config_data = {
    "detection_area": detection_area,
    "dino_area": dino_area,
    "restart_area": restart_area,
    "jump_coord": jump_coord,
    "time_pixel": time_pixel,
    "epsilon": epsilon,
    "restart_image": np.array(restart_image).tolist()
}

# Writing to config.json
with open('config.json', 'w') as config_file:
    json.dump(config_data, config_file)

print("Configuration values have been saved to config.json.")
