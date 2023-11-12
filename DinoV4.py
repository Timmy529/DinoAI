from PIL import ImageGrab, ImageOps, ImageDraw
import pyautogui
import time
import numpy as np
import json

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


def area_mean(area):
    """
    returns the mean value of a screen area
    :return: float
    """
    image = ImageGrab.grab(area)
    gray_img = ImageOps.grayscale(image)
    arr = np.array(gray_img.getcolors())
    return arr.mean()

class DinoBot:
    """FSA for playing silly little brave dino game"""
    def __init__(self, dino_coords, restart_coords, low_detection_area, high_detection_area, restart_area, low_detection_trigger, high_detection_trigger, restart_trigger, epsilon):
        self.retries = 0
        self.restart_trigger = restart_trigger
        self.low_detection_trigger = low_detection_trigger
        self.high_detection_trigger = high_detection_trigger
        self.restart_area = restart_area
        self.dino_coords = dino_coords
        self.restart_coords = restart_coords
        self.low_detection_area = low_detection_area
        self.high_detection_area = high_detection_area
        self.epsilon = epsilon
        self.daytime = False

    def restart(self):
        """
        Restart the game and set default crawl run
        :return: None
        """
        pyautogui.click(self.restart_coords)

    def jump(self):
        """
        Jump over the obstacle
        :return: None
        """
        pyautogui.keyDown('space')
        pyautogui.keyUp('space')

    def duck(self):
        """
        ducks.
        :return: None
        """
        pyautogui.keyDown('down')
        time.sleep(0.2)
        pyautogui.keyUp('down')

    def run(self):
        """
        Main loop of the playing
        :return: None
        """
        while True:

            if self.restart_trigger-self.epsilon < area_mean(self.restart_area) < self.restart_trigger+self.epsilon:
                self.restart()
                self.retries += 1
                print("restarting!")
                print("game number: "+ str(self.retries))
                time.sleep(3)
            if area_mean(self.low_detection_area) < self.low_detection_trigger - self.epsilon or area_mean(self.low_detection_area) > self.low_detection_trigger + self.epsilon:
                self.jump()
            elif area_mean(self.high_detection_area) < self.high_detection_trigger - self.epsilon or area_mean(self.high_detection_area) > self.high_detection_trigger + self.epsilon:
                self.duck()

# Load configuration values
loaded_config = load_config()
if loaded_config:
    dino_coord = loaded_config['dino_coord']
    restart_coord = loaded_config['restart_coord']
    low_detection_area = loaded_config['low_detection_area']
    high_detection_area = loaded_config['high_detection_area']
    restart_area = loaded_config['restart_area']
    low_detection_mean = loaded_config['low_detection_mean']
    high_detection_mean = loaded_config['high_detection_mean']
    restart_mean = loaded_config['restart_mean']
    epsilon = loaded_config['epsilon']

    # Create DinoBot instance and run
    bot = DinoBot(dino_coord, restart_coord, low_detection_area, high_detection_area, restart_area, low_detection_mean, high_detection_mean, restart_mean, epsilon)
    bot.run()