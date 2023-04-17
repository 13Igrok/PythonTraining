import random

import pyautogui


def click_left_mouse():
    pyautogui.moveTo ( x, y )


while True:
    x = random.randint ( 0, 1920 )
    y = random.randint ( 0, 1080 )
    click_left_mouse ()
    pyautogui.click ()
