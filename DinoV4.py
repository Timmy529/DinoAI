import json
import time

import numpy as np
import pyautogui
from PIL import ImageGrab, ImageOps


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


def area_median(area):
    """
    returns the number of pixels that have the median color of a screen area
    :return: float
    """
    image = ImageGrab.grab(area)
    gray_img = ImageOps.grayscale(image)
    arr = np.array(gray_img.getcolors())
    return np.median(arr)

def area_mean(area):
    """
    returns the number of pixels that have the mean color of a screen area
    :return: float
    """
    image = ImageGrab.grab(area)
    gray_img = ImageOps.grayscale(image)
    arr = np.array(gray_img.getcolors())
    return np.mean(arr)


class DinoBot:
    """FSA for playing silly little brave dino game"""

    def __init__(self, restart_coords, low_detection_area, high_detection_area, restart_area,
                 low_detection_trigger, high_detection_trigger, restart_trigger, epsilon):
        self.retries = 0
        self.restart_trigger = restart_trigger
        self.low_detection_trigger = low_detection_trigger
        self.high_detection_trigger = high_detection_trigger
        self.restart_area = restart_area
        self.restart_coords = restart_coords
        self.low_detection_area = low_detection_area
        self.high_detection_area = high_detection_area
        self.epsilon = epsilon
        self.daytime = False
        self.jumps = 0
        self.ducks = 0
        self.start_time = time.time()
        self.velocity = 0

    def restart(self):
        """
        Restart the game and set default crawl run
        :return: None
        """
        time.sleep(0.5)
        pyautogui.click(self.restart_coords)
        self.jumps = 0
        self.ducks = 0
        self.retries += 1
        self.start_time = time.time()
        print("restarting!")
        print("game number: " + str(self.retries))

    def jump(self):
        """
        Jump over the obstacle
        :return: None
        """
        pyautogui.keyDown('space')
        pyautogui.keyUp('space')
        self.jumps += 1
        print("jumps: "+str(self.jumps))

    def duck(self):
        """
        ducks.
        :return: None
        """
        pyautogui.keyDown('down')
        time.sleep(0.2)
        pyautogui.keyUp('down')
        self.ducks += 1
        print("ducks: "+str(self.ducks))

    def run(self):
        """
        Main loop of the playing
        :return: None
        """
        while True:
            print("velocity: "+str(self.velocity))
            if self.velocity < 100:
                self.velocity = time.time() - self.start_time
            if self.restart_trigger - self.epsilon < area_mean(self.restart_area) < self.restart_trigger + self.epsilon:
                self.restart()
                time.sleep(3)
            offset = (self.low_detection_area[0] + self.velocity, self.low_detection_area[1] , self.low_detection_area[2] + self.velocity, self.low_detection_area[3])
            high_offset = (self.high_detection_area[0] + self.velocity, self.high_detection_area[1] , self.high_detection_area[2] + self.velocity, self.high_detection_area[3])
            if area_median(offset) < self.low_detection_trigger - self.epsilon or area_median(
                    offset) > self.low_detection_trigger + self.epsilon:
                self.jump()
            elif area_median(high_offset) < self.high_detection_trigger - self.epsilon or area_median(
                    high_offset) > self.high_detection_trigger + self.epsilon:
                self.duck()

# Load configuration values
loaded_config = load_config()
if loaded_config:
    restart_coord = loaded_config['restart_coord']
    low_detection_area = loaded_config['low_detection_area']
    high_detection_area = loaded_config['high_detection_area']
    restart_area = loaded_config['restart_area']
    low_detection_median = loaded_config['low_detection_median']
    high_detection_median = loaded_config['high_detection_median']
    restart_mean = loaded_config['restart_mean']
    epsilon = loaded_config['epsilon']
    time_pixel = loaded_config['time_pixel']


    # Create DinoBot instance and run
    bot = DinoBot(restart_coord, low_detection_area, high_detection_area, restart_area, low_detection_median,
                  high_detection_median, restart_mean, epsilon)
    bot.run()
