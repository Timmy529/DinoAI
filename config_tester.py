import json

import numpy as np
from PIL import ImageOps, ImageGrab, ImageDraw


def area_mean(area):
    """
    returns the number of pixels that have the mean color of a screen area
    :return: float
    """
    image = ImageGrab.grab(area)
    gray_img = ImageOps.grayscale(image)
    arr = np.array(gray_img.getcolors())
    return np.mean(arr)


def area_median(area):
    """
    returns the number of pixels that have the median color of a screen area
    :return: float
    """
    image = ImageGrab.grab(area)
    gray_img = ImageOps.grayscale(image)
    arr = np.array(gray_img.getcolors())
    return np.median(arr)


def load_config(file_path='config.json'):
    try:
        with open(file_path, 'r') as config_file:
            config_data = json.load(config_file)
        return config_data
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Unable to decode {file_path} as JSON.")
        return None


loaded_config = load_config()
if loaded_config:
    restart_coord = loaded_config['restart_coord']
    low_detection_area = loaded_config['low_detection_area']
    high_detection_area = loaded_config['high_detection_area']
    restart_area = loaded_config['restart_area']
    low_detection_median = loaded_config['low_detection_median']
    high_detection_median = loaded_config['high_detection_median']
    restart_median = loaded_config['restart_median']
    epsilon = loaded_config['epsilon']
    time_pixel = loaded_config['time_pixel']
    dino_area = loaded_config['dino_area']

# Initializations
prev_low_median = prev_high_median = prev_restart_median = prev_dino_median = None


image = ImageGrab.grab()
draw = ImageDraw.Draw(image)
left, top, right, bottom = low_detection_area
draw.rectangle([left, top, right, bottom], outline="red", width=2)
left, top, right, bottom = high_detection_area
draw.rectangle([left, top, right, bottom], outline="blue", width=2)
left, top, right, bottom = restart_area
draw.rectangle([left, top, right, bottom], outline="green", width=2)
left, top, right, bottom = dino_area
draw.rectangle([left, top, right, bottom], outline="yellow", width=2)
image.show()

while True:
    # Calculate current medians
    current_low_median = area_median(low_detection_area)
    current_high_median = area_median(high_detection_area)
    current_restart_median = area_mean(restart_area)
    current_dino_median = area_median(dino_area)

    # Check if values have changed
    if (
            current_low_median != prev_low_median or
            current_high_median != prev_high_median or
            current_restart_median != prev_restart_median or
            current_dino_median != prev_dino_median
    ):
        # Print only if values have changed
        print("low_detection_area_median: " + str(current_low_median))
        print("high_detection_area_median: " + str(current_high_median))
        print("restart_area_median: " + str(current_restart_median))
        print("dino_area_median: " + str(current_dino_median))

        # Update previous values
        prev_low_median = current_low_median
        prev_high_median = current_high_median
        prev_restart_median = current_restart_median
        prev_dino_median = current_dino_median
