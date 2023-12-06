import pygame
import random

# Инициализация Pygame
pygame.init()

# Установка размеров экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Постоянный салют")

# Цвета
white = (255, 255, 255)

# Основной цикл программы
running = True
clock = pygame.time.Clock()

# Функция для создания салюта
def create_firework():
    return {
        'x': random.randint(0, screen_width),
        'y': screen_height,
        'color': (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
        'radius': random.randint(5, 20),
        'speed': random.randint(1, 5)
    }

fireworks = []

while running:
    screen.fill(white)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Создание новых салютов
    if random.random() < 0.1:
        fireworks.append(create_firework())

    # Отрисовка и обновление салютов
    for firework in fireworks:
        pygame.draw.circle(screen, firework['color'], (firework['x'], firework['y']), firework['radius'])
        firework['y'] -= firework['speed']
        if firework['y'] < 0:
            fireworks.remove(firework)

    pygame.display.flip()
    clock.tick(60)

# Завершение работы Pygame
pygame.quit()