# import random - imports the random module, which is used to generate random integer values for the mouse cursor position
# import pyautogui - imports the pyautogui library, which provides functions for automating GUI interactions
# def click_left_mouse(): - defines a function called click_left_mouse() which will move the mouse cursor to the specified coordinates and simulate a left-click
# pyautogui.moveTo(x, y) - moves the mouse cursor to the specified x and y coordinates on the screen
# while True: - begins an infinite loop that will repeatedly execute the code inside the loop
# x = random.randint(0, 1920) - generates a random integer value between 0 and 1920 for the x coordinate of the mouse cursor position
# y = random.randint(0, 1080) - generates a random integer value between 0 and 1080 for the y coordinate of the mouse cursor position
# click_left_mouse() - calls the click_left_mouse() function to move the mouse cursor to the specified coordinates and simulate a left-click
# pyautogui.click() - simulates a left-click at the current mouse cursor position
import random

import pyautogui


def click_left_mouse():
    pyautogui.moveTo ( x, y )


while True:
    x = random.randint ( 0, 1920 )
    y = random.randint ( 0, 1080 )
    click_left_mouse ()
    pyautogui.click ()
