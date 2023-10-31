import pygame
import pyautogui

# Получаем текущую позицию курсора
x, y = pyautogui.position()

# Печатаем текущие координаты курсора
print(f"Текущие координаты курсора: x={x}, y={y}")

# Перемещаем курсор в новую позицию
new_x, new_y = 100, 100
pyautogui.moveTo(new_x, new_y)

# Получаем новую позицию курсора
x, y = pyautogui.position()

# Печатаем новые координаты курсора
print(f"Новые координаты курсора: x={x}, y={y}")
# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 800

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

# Создание окна
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Шашки")

# Класс для шашки
class Piece:
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col

    def draw(self):
        radius = square_size // 2 - 10
        x = self.col * square_size + square_size // 2
        y = self.row * square_size + square_size // 2
        pygame.draw.circle(win, self.color, (x, y), radius)

# Отрисовка доски
def draw_board():
    win.fill(GRAY)
    for row in range(8):
        for col in range(row % 2, 8, 2):
            x = col * square_size
            y = row * square_size
            pygame.draw.rect(win, WHITE, (x, y, square_size, square_size))

# Обновление экрана
def update_screen():
    draw_board()
    for piece in pieces:
        piece.draw()
    pygame.display.update()

# Инициализация игры
def start_game():
    global pieces
    pieces = []
    for row in range(3):
        for col in range(row % 2, 8, 2):
            pieces.append(Piece(BLACK, row, col))
    for row in range(5, 8):
        for col in range(row % 2, 8, 2):
            pieces.append(Piece(RED, row, col))

# Основной игровой цикл
def game_loop():
    running = True
    clock = pygame.time.Clock()

    start_game()

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        update_screen()

    pygame.quit()

# Размеры клетки на доске
square_size = WIDTH // 8

# Запуск игрового цикла
game_loop()