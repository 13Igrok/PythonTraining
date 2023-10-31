import pygame
import random

# Определение цветов
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Определение размеров экрана
width = 400
height = 400

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Крестики-нолики')

# Инициализация игрового поля
board = [' ' for _ in range(9)]
player = 'X'
game_over = False

# Инициализация искусственного интеллекта
available_moves = [i for i in range(9)]


def draw_board():
    screen.fill(white)

    pygame.draw.line(screen, black, (width / 3, 0), (width / 3, height), 5)
    pygame.draw.line(screen, black, (width / 3 * 2, 0), (width / 3 * 2, height), 5)
    pygame.draw.line(screen, black, (0, height / 3), (width, height / 3), 5)
    pygame.draw.line(screen, black, (0, height / 3 * 2), (width, height / 3 * 2), 5)

    for i in range(3):
        for j in range(3):
            x = j * width / 3 + width / 6
            y = i * height / 3 + height / 6
            if board[i * 3 + j] == 'X':
                pygame.draw.line(screen, red, (x - 30, y - 30), (x + 30, y + 30), 5)
                pygame.draw.line(screen, red, (x + 30, y - 30), (x - 30, y + 30), 5)
            elif board[i * 3 + j] == 'O':
                pygame.draw.circle(screen, blue, (int(x), int(y)), 30, 5)

    pygame.display.update()


def make_move(position):
    global player, available_moves
    if board[position] == ' ':
        board[position] = player
        available_moves.remove(position)
        if player == 'X':
            player = 'O'
        else:
            player = 'X'
        draw_board()


def check_winner():
    lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

    for line in lines:
        if board[line[0]] == board[line[1]] == board[line[2]] != ' ':
            return board[line[0]]

    if len(available_moves) == 0:
        return 'Ничья'

    return None


def check_game_over():
    result = check_winner()
    if result:
        global game_over
        game_over = True
        if result == 'Ничья':
            print("Ничья!")
        else:
            print("Победил игрок", result)


def play_ai_move():
    if len(available_moves) > 0:
        position = random.choice(available_moves)
        make_move(position)


def play_game():
    global game_over
    draw_board()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if player == 'X':
                    x, y = pygame.mouse.get_pos()
                    row = y // (height / 3)
                    col = x // (width / 3)
                    position = int(row * 3 + col)
                    make_move(position)

        check_game_over()
        if not game_over and player == 'O':
            play_ai_move()


play_game()