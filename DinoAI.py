from PIL import ImageGrab, ImageOps, ImageDraw
import pyautogui
import time
import numpy as np

# Dumb Dino V1 (high score 724)
# half stolen from https://becominghuman.ai/google-chrome-dinosaur-game-python-bot-b698723e86e

class Bot:
    """Bot for playing Chrome dino run game"""
    def __init__(self):
        self.restart_area = (350, 230, 610, 260)
        self.dino_coords = (156, 300)
        self.restart_coords = (500, 300)
        self.area = (self.dino_coords[0] + 70, self.dino_coords[1] + 35,
                     self.dino_coords[0] + 230, self.dino_coords[1] + 40)

    def set_dino_coords(self, x, y):
        """
        Change default dino coordinates
        :param x: top right x coordinate (int)
        :param y: top right y coordinate (int)
        :return: None
        """
        self.dino_coords = (x, y)

    def set_restart_coords(self, x, y):
        """
        Change default restart button coordinates
        :param x: center x coordinate (int)
        :param y: center y coordinate (int)
        :return: None
        """
        self.restart_coords = (x, y)

    def restart(self):
        """
        Restart the game and set default crawl run
        :return: None
        """
        pyautogui.click(self.restart_coords)
        pyautogui.keyDown('down')

    def jump(self):
        """
        Jump over the obstacle
        :return: None
        """
        pyautogui.keyUp('down')
        pyautogui.keyDown('space')
        time.sleep(0.08)
        pyautogui.keyUp('space')
        pyautogui.keyDown('down')

    def detection_area(self, area):
        """
        Checks the area to have obstacles
        :return: float
        """
        image = ImageGrab.grab(area)
        gray_img = ImageOps.grayscale(image)
        arr = np.array(gray_img.getcolors())
        # print(arr.mean())
        return arr.mean()

    def draw_area_box(self):
        """
        Draw a box around the self.area region
        :return: None
        """
        image = ImageGrab.grab()
        draw = ImageDraw.Draw(image)
        left, top, right, bottom = self.area
        draw.rectangle([left, top, right, bottom], outline="red", width=2)
        left, top, right, bottom = self.restart_area
        draw.rectangle([left, top, right, bottom], outline="blue", width=2)
        image.show()

    def main(self):
        """
        Main loop of the playing
        :return: None
        """
        #self.restart()
        #self.draw_area_box()
        detection_mean = 0
        restart_mean = 0
        while True:
            if detection_mean != self.detection_area(self.area):
                detection_mean = self.detection_area(self.area)
                print("Detection area mean: " + str(detection_mean))
            if restart_mean != self.detection_area(self.restart_area):
                restart_mean = self.detection_area(self.restart_area)
                # print("Restart area mean: " + str(restart_mean))

            if 65 < restart_mean < 85:
                self.restart()
                print("restarting!")
            if detection_mean != 416.5:
                self.jump()
bot = Bot()
bot.main()