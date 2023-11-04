import os

# Выполнение команды обновления Windows
def update_windows():
    os.system("cmd /c start ms-settings:windowsupdate")

# Запуск обновления Windows
update_windows()
