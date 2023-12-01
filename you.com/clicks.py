import time
from pynput.mouse import Button, Controller

# Создаем экземпляр контроллера мыши
mouse = Controller()

# Координаты клика
x = 100
y = 200

# Количество кликов
clicks = 10000

# Задержка между кликами в секундах
delay = 0.00001

# Перемещаем курсор на указанные координаты и кликаем
mouse.position = (x, y)
for i in range(clicks):
    mouse.click(Button.left)
    time.sleep(delay)
