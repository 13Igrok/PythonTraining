import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Параметры экрана
WIDTH, HEIGHT = 1024, 720
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
GRID_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (255, 255, 255)

# Параметры змейки
snake = [(0, 0)]
snake_direction = (1, 0)
snake_length = 1
snake_speed = 2

# Параметры фрукта
fruit = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

# Инициализация экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

# Основной цикл игры
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != (0, 1):
                snake_direction = (0, -1)
            elif event.key == pygame.K_DOWN and snake_direction != (0, -1):
                snake_direction = (0, 1)
            elif event.key == pygame.K_LEFT and snake_direction != (1, 0):
                snake_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                snake_direction = (1, 0)

    # Двигаем змейку
    x, y = snake[0]
    new_head = (x + snake_direction[0], y + snake_direction[1])

    # Проверка на окончание игры
    if (
        new_head in snake
        or new_head[0] < 0
        or new_head[0] >= GRID_WIDTH
        or new_head[1] < 0
        or new_head[1] >= GRID_HEIGHT
    ):
        pygame.quit()
        sys.exit()

    # Добавляем новую голову
    snake.insert(0, new_head)

    # Проверка, съела ли змейка фрукт
    if snake[0] == fruit:
        snake_length += 1
        fruit = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    # Удаляем лишний хвост
    if len(snake) > snake_length:
        snake.pop()

    # Очистка экрана
    screen.fill(BACKGROUND_COLOR)

    # Отрисовка змейки
    for segment in snake:
        pygame.draw.rect(
            screen, GRID_COLOR, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        )

    # Отрисовка фрукта
    pygame.draw.rect(
        screen, (255, 0, 0), (fruit[0] * GRID_SIZE, fruit[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    )

    # Обновление экрана
    pygame.display.update()

    # Задержка для скорости змейки
    clock.tick(snake_speed)