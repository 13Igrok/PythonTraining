import pygame

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

# Размер клетки
square_size = WIDTH // 8

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

# Проверка нахождения клетки в пределах доски
def is_valid_position(row, col):
    return 0 <= row < 8 and 0 <= col < 8

# Инициализация игры
def start_game():
    global pieces, selected_piece, turn
    pieces = []
    selected_piece = None
    turn = RED

    for row in range(3):
        for col in range(row % 2, 8, 2):
            pieces.append(Piece(BLACK, row, col))
    for row in range(5, 8):
        for col in range(row % 2, 8, 2):
            pieces.append(Piece(RED, row, col))

# Проверка возможности выполнения хода
def is_valid_move(piece, row, col):
    if not is_valid_position(row, col):
        return False

    if abs(row - piece.row) != abs(col - piece.col):
        return False

    if abs(row - piece.row) == 1 and abs(col - piece.col) == 1:
        return True

    middle_row = (row + piece.row) // 2
    middle_col = (col + piece.col) // 2

    middle_piece = None
    for piece_ in pieces:
        if piece_.row == middle_row and piece_.col == middle_col:
            middle_piece = piece_
            break
    
    if middle_piece and middle_piece.color != piece.color:
        return True
    
    return False

# Выполнение хода
def move_piece(piece, row, col):
    piece.row = row
    piece.col = col

    middle_row = (row + piece.row) // 2
    middle_col = (col + piece.col) // 2

    middle_piece = None
    for piece_ in pieces:
        if piece_.row == middle_row and piece_.col == middle_col:
            middle_piece = piece_
            break

    if middle_piece:
        pieces.remove(middle_piece)

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    col = x // square_size
                    row = y // square_size

                    for piece in pieces:
                        if piece.row == row and piece.col == col and piece.color == turn:
                            selected_piece = piece
                            break
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and selected_piece:
                    x, y = event.pos
                    col = x // square_size
                    row = y // square_size

                    if is_valid_move(selected_piece, row, col):
                        move_piece(selected_piece, row, col)
                        selected_piece = None

                    if selected_piece.row == 7 and selected_piece.color == BLACK:
                        win_caption = "Шашки - Черные победили!"
                        pygame.display.set_caption(win_caption)
                        running = False
                    elif selected_piece.row == 0 and selected_piece.color == RED:
                        win_caption = "Шашки - Красные победили!"
                        pygame.display.set_caption(win_caption)
                        running = False

        update_screen()

    pygame.quit()

# Запуск игры
game_loop()