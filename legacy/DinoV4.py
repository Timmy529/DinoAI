import json
import time
import keyboard

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


class DinoBot:
    """FSA for playing silly little brave dino game"""

    def __init__(self, restart_coords, low_detection_area, dino_area, restart_area,
                 low_detection_trigger, dino_median, jump_position, restart_trigger, time_pixel, epsilon):
        self.retries = 0
        self.jump_position = jump_position
        self.restart_trigger = restart_trigger
        self.low_detection_trigger = low_detection_trigger
        self.restart_area = restart_area
        self.dino_median = dino_median
        self.restart_coords = restart_coords
        self.low_detection_area = low_detection_area
        self.dino_area = dino_area
        self.epsilon = epsilon
        self.daytime = False
        self.jumps = 0
        self.ducks = 0
        self.start_time = time.time()
        self.velocity = 0
        self.time_pixel = time_pixel
        self.current_screenshot = None  # Reference to the current screenshot
        self.total_jumps = 0
        self.total_ducks = 0
        self.highscore = 0
        self.jumping = False
        self.ducking = False

    def update_screenshot(self):
        """
        Capture the current screenshot and update the reference.
        :return: None
        """
        screen = ImageGrab.grab()
        self.current_screenshot = ImageOps.grayscale(screen)

    def area_mean(self, area):
        """
        Returns the number of pixels that have the mean color of a screen area.
        :return: float
        """
        sub_area = self.current_screenshot.crop(area)
        arr = np.array(sub_area.getcolors())
        return np.mean(arr)

    def area_median(self, area):
        """
        Returns the number of pixels that have the median color of a screen area.
        :return: float
        """
        sub_area = self.current_screenshot.crop(area)
        arr = np.array(sub_area.getcolors())
        return np.median(arr)

    def jump(self):
        """
        Jump over the obstacle
        :return: None
        """
        pyautogui.keyUp('down')
        pyautogui.keyDown('space')
        pyautogui.keyUp('space')
        self.jumps += 1
        self.jumping = True
        self.ducking = False
        print("jumps: "+str(self.jumps))


    def duck(self):
        """
        ducks.
        :return: None
        """
        pyautogui.keyDown('down')
        self.ducks += 1
        self.ducking = True

    def restart(self):
        """
        Restart the game and set the default crawl run.
        :return: None
        """
        print("restarting!")
        time.sleep(1)
        pyautogui.click(self.restart_coords)
        self.total_jumps += self.jumps
        self.total_ducks += self.ducks
        self.highscore = self.velocity if self.highscore < self.velocity else self.highscore
        self.jumps = 0
        self.ducks = 0
        self.retries += 1
        self.start_time = time.time()
        print("game number: " + str(self.retries))

    def exit(self):
        print("games: " + str(self.retries))
        print("total jumps: "+ str(self.total_jumps))
        print("total ducks: "+ str(self.total_ducks))
        print("highscore: "+ str(self.highscore))
        exit()

    def run(self):
        """
        Main loop of the playing.
        :return: None
        """
        while True:

            if keyboard.is_pressed('esc'):
                self.exit()
            self.update_screenshot()  # Capture the current screenshot
            low_detection_median = 0
            if self.current_screenshot.getpixel(self.time_pixel) == 255:
                low_detection_median = self.low_detection_trigger[1]
            elif self.current_screenshot.getpixel(self.time_pixel) == 33:
                low_detection_median = self.low_detection_trigger[0]
            if low_detection_median != 0:
                print("velocity: "+str(self.velocity))
                if self.velocity < 100:
                    self.velocity = time.time() - self.start_time
                if np.array(self.current_screenshot.crop(self.restart_area)).tolist() == self.restart_trigger:
                    self.restart()
                offset = (self.low_detection_area[0] + self.velocity, self.low_detection_area[1],
                          self.low_detection_area[2] + self.velocity, self.low_detection_area[3])
                if self.area_median(offset) < low_detection_median - self.epsilon or self.area_median(
                        offset) > low_detection_median + self.epsilon:
                    self.jump()
                if self.jumping & self.current_screenshot.getpixel(self.jump_position) == 172 & self.area_median(self.dino_area) == self.dino_median:
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
    restart_img = loaded_config['restart_img']
    epsilon = loaded_config['epsilon']
    time_pixel = loaded_config['time_pixel']
    dino_area = loaded_config['dino_area']
    jump_position = loaded_config['jump_position']
    dino_median = loaded_config['dino_median']

    # Create DinoBot instance and run
    bot = DinoBot(restart_coord, low_detection_area, dino_area, restart_area, low_detection_median,
                  dino_median, jump_position, restart_img, time_pixel, epsilon)
    bot.run()
