import keyboard
import pyautogui
import time

def clicker():
    while True:
        if keyboard.is_pressed('right shift'):
            # Координаты клика
            x, y = pyautogui.position()

            # Выполнение клика
            pyautogui.click(x, y)

            # Задержка перед следующим кликом
            time.sleep(0.001)  # Установите желаемую скорость нажатий

clicker()
