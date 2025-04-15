import pygame
import random
import sys
from database import init_db, save_game_state, get_best_moves, update_game_result, get_game_stats, update_game_stats
import logging
import datetime
import json
import os
import math

# Настройка логирования
logging.basicConfig(
    filename=f'xo_ai_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Путь к файлу с историей обучения
LEARNING_HISTORY_FILE = 'learning_history.json'

# Определение цветов
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
gray = (200, 200, 200)

# Определение размеров экрана
width = 800
height = 600

# Определение размеров игрового поля
board_width = 500
board_height = 500
board_x = 20  # Отступ слева
board_y = 20  # Отступ сверху

# Определение размеров панели статистики
stats_width = 250
stats_x = board_x + board_width + 20
stats_y = board_y

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Крестики-нолики')

# Инициализация игрового поля
board = [' ' for _ in range(9)]
player = 'X'
game_over = False
ai_plays_for_x = False
self_learning = False  # Флаг для режима самообучения

# Инициализация искусственного интеллекта
available_moves = [i for i in range(9)]


def draw_board():
    # Очищаем только область игрового поля
    pygame.draw.rect(screen, gray, (board_x - 10, board_y - 10, board_width + 20, board_height + 20))
    
    # Рисуем фон для игрового поля
    pygame.draw.rect(screen, white, (board_x - 10, board_y - 10, board_width + 20, board_height + 20))
    
    # Рисуем рамку игрового поля
    pygame.draw.rect(screen, black, (board_x - 5, board_y - 5, board_width + 10, board_height + 10), 5)
    
    # Рисуем линии игрового поля
    cell_width = board_width / 3
    cell_height = board_height / 3
    
    for i in range(1, 3):
        pygame.draw.line(screen, black, 
                        (board_x + i * cell_width, board_y),
                        (board_x + i * cell_width, board_y + board_height), 5)
        pygame.draw.line(screen, black,
                        (board_x, board_y + i * cell_height),
                        (board_x + board_width, board_y + i * cell_height), 5)

    # Рисуем крестики и нолики
    for i in range(3):
        for j in range(3):
            x = board_x + j * cell_width + cell_width / 2
            y = board_y + i * cell_height + cell_height / 2
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


def evaluate_board():
    lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    
    for line in lines:
        if board[line[0]] == board[line[1]] == board[line[2]] == 'X':
            return -10
        elif board[line[0]] == board[line[1]] == board[line[2]] == 'O':
            return 10
    
    if ' ' not in board:
        return 0
    
    return None


def minimax(depth, is_maximizing):
    score = evaluate_board()
    if score is not None:
        return score
    
    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(depth + 1, False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(depth + 1, True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score


def find_best_move():
    # Проверяем, есть ли сохраненные лучшие ходы для текущего состояния
    saved_moves = get_best_moves(board)
    if saved_moves:
        # Фильтруем только доступные ходы
        available_saved_moves = {k: v for k, v in saved_moves.items() if int(k) in available_moves}
        if available_saved_moves:
            # Выбираем ход с наибольшим количеством побед
            best_move = max(available_saved_moves.items(), key=lambda x: x[1]['wins'])[0]
            return int(best_move)
    
    # Если сохраненных ходов нет или они не доступны, используем алгоритм minimax
    best_score = -float('inf')
    best_move = None
    
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(0, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i
    
    return best_move if best_move is not None else random.choice(available_moves)


def play_ai_move():
    if len(available_moves) > 0:
        position = find_best_move()
        make_move(position)
        
        # Сохраняем текущее состояние и лучший ход
        best_moves = {str(pos): {'wins': 0, 'losses': 0, 'draws': 0} for pos in available_moves}
        if str(position) in best_moves:  # Проверяем, что позиция существует в словаре
            best_moves[str(position)]['wins'] = 1
        save_game_state(board, best_moves)


def draw_stats():
    # Очищаем только область статистики
    pygame.draw.rect(screen, gray, (stats_x - 10, stats_y - 10, stats_width + 20, height - 40))
    
    # Рисуем фон для панели статистики
    pygame.draw.rect(screen, white, (stats_x - 10, stats_y - 10, stats_width + 20, height - 40))
    pygame.draw.rect(screen, black, (stats_x - 5, stats_y - 5, stats_width + 10, height - 30), 3)
    
    stats = get_game_stats()
    font = pygame.font.Font(None, 36)
    
    # Отображаем статистику
    stats_text = [
        f'Побед игрока: {stats["player_wins"]}',
        f'Побед ИИ: {stats["ai_wins"]}',
        f'Ничьих: {stats["draws"]}'
    ]
    
    y = stats_y + 20
    for text in stats_text:
        rendered_text = font.render(text, True, black)
        screen.blit(rendered_text, (stats_x + 10, y))
        y += 50
    
    # Кнопки управления
    button_width = stats_width - 20
    button_height = 45
    button_y = height - 300
    
    # Кнопка включения/выключения бота
    bot_button = pygame.Rect(stats_x + 10, button_y, button_width, button_height)
    pygame.draw.rect(screen, white, bot_button)
    pygame.draw.rect(screen, blue if ai_plays_for_x else red, bot_button, 3)
    bot_text = font.render('Бот играет за X' if ai_plays_for_x else 'Игрок играет за X', True, blue if ai_plays_for_x else red)
    text_rect = bot_text.get_rect(center=bot_button.center)
    screen.blit(bot_text, text_rect)
    
    # Кнопка самообучения
    button_y += 70
    self_learning_button = pygame.Rect(stats_x + 10, button_y, button_width, button_height)
    pygame.draw.rect(screen, white, self_learning_button)
    pygame.draw.rect(screen, green if self_learning else black, self_learning_button, 3)
    learning_text = font.render('Самообучение' if not self_learning else 'Остановить', True, green if self_learning else black)
    text_rect = learning_text.get_rect(center=self_learning_button.center)
    screen.blit(learning_text, text_rect)
    
    # Кнопки управления внизу
    button_y += 70
    exit_button = pygame.Rect(stats_x + 10, button_y, button_width, button_height)
    pygame.draw.rect(screen, white, exit_button)
    pygame.draw.rect(screen, red, exit_button, 3)
    exit_text = font.render('Выход', True, red)
    text_rect = exit_text.get_rect(center=exit_button.center)
    screen.blit(exit_text, text_rect)
    
    button_y += 70
    restart_button = pygame.Rect(stats_x + 10, button_y, button_width, button_height)
    pygame.draw.rect(screen, white, restart_button)
    pygame.draw.rect(screen, blue, restart_button, 3)
    restart_text = font.render('Заново', True, blue)
    text_rect = restart_text.get_rect(center=restart_button.center)
    screen.blit(restart_text, text_rect)
    
    return exit_button, restart_button, bot_button, self_learning_button


def reset_game():
    global board, player, game_over, available_moves
    board = [' ' for _ in range(9)]
    player = 'X'
    game_over = False
    available_moves = [i for i in range(9)]
    # Очищаем только необходимые области
    pygame.draw.rect(screen, gray, (0, 0, width, height))
    draw_board()
    draw_stats()
    pygame.display.update()


def check_game_over():
    result = check_winner()
    if result:
        global game_over
        game_over = True
        if result == 'Ничья':
            print("Ничья!")
            update_game_result(board, 'draw')
            update_game_stats('draw')
        else:
            print("Победил игрок", result)
            update_game_result(board, result)
            update_game_stats(result)
        
        # Отображаем результат
        font = pygame.font.Font(None, 48)
        if result == 'Ничья':
            text = font.render('НИЧЬЯ!', True, black)
        else:
            text = font.render(f'ПОБЕДИЛ {result}!', True, red if result == 'X' else blue)
        
        text_rect = text.get_rect(center=(width/2, height/2))
        screen.blit(text, text_rect)
        pygame.display.update()
        
        # Автоматический перезапуск через 2 секунды
        pygame.time.wait(2000)
        reset_game()
        
        # Автоматически начинаем новую игру
        global player
        player = 'X'  # Игрок всегда ходит первым
        game_over = False


def load_learning_history():
    if os.path.exists(LEARNING_HISTORY_FILE):
        with open(LEARNING_HISTORY_FILE, 'r') as f:
            return json.load(f)
    return {
        'total_games': 0,
        'player_wins': 0,
        'ai_wins': 0,
        'draws': 0,
        'win_rate': 0.0,
        'learning_rate': 0.1
    }

def save_learning_history(history):
    with open(LEARNING_HISTORY_FILE, 'w') as f:
        json.dump(history, f)

def update_learning_rate(history):
    # Увеличиваем скорость обучения, если ИИ выигрывает реже
    if history['ai_wins'] / max(1, history['total_games']) < 0.5:
        history['learning_rate'] = min(0.3, history['learning_rate'] + 0.01)
    else:
        history['learning_rate'] = max(0.05, history['learning_rate'] - 0.005)
    return history

def self_learn():
    global board, player, game_over, available_moves, self_learning
    current_board = board.copy()
    current_player = player
    current_game_over = game_over
    current_available_moves = available_moves.copy()
    
    move_stats = {}
    learning_history = load_learning_history()
    exploration_rate = 0.2  # Начальная вероятность исследования
    
    logging.info("Начало процесса самообучения")
    logging.info(f"Текущая статистика: {learning_history}")
    
    for game_num in range(1000):
        if not self_learning:
            break
            
        board = [' ' for _ in range(9)]
        player = 'X'
        game_over = False
        available_moves = [i for i in range(9)]
        game_history = []
        
        while not game_over and self_learning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    _, _, _, self_learning_button = draw_stats()
                    if self_learning_button and self_learning_button.collidepoint(event.pos):
                        self_learning = False
                        break
            
            if not self_learning:
                break
                
            board_state = ''.join(board)
            
            if board_state not in move_stats:
                move_stats[board_state] = {str(i): {'wins': 0, 'losses': 0, 'draws': 0, 'visits': 0} for i in range(9) if board[i] == ' '}
            
            # Адаптивная вероятность исследования
            if random.random() < exploration_rate:
                position = random.choice(available_moves)
                logging.debug(f"Случайный ход: {position}")
            else:
                available_moves_stats = {k: v for k, v in move_stats[board_state].items() if int(k) in available_moves}
                if available_moves_stats:
                    # Используем UCB1 для выбора хода
                    total_visits = sum(stats['visits'] for stats in available_moves_stats.values())
                    best_move = None
                    best_score = -float('inf')
                    
                    for move, stats in available_moves_stats.items():
                        if stats['visits'] == 0:
                            score = float('inf')
                        else:
                            win_rate = (stats['wins'] + 1) / (stats['visits'] + 2)
                            exploration = math.sqrt(2 * math.log(total_visits + 1) / (stats['visits'] + 1))
                            score = win_rate + learning_history['learning_rate'] * exploration
                        
                        if score > best_score:
                            best_score = score
                            best_move = move
                    
                    position = int(best_move)
                    logging.debug(f"Выбран ход {position} с оценкой {best_score}")
                else:
                    position = random.choice(available_moves)
            
            game_history.append((board_state, str(position)))
            make_move(position)
            
            # Обновляем статистику посещений
            if board_state in move_stats and str(position) in move_stats[board_state]:
                move_stats[board_state][str(position)]['visits'] += 1
            
            draw_board()
            pygame.display.update(pygame.Rect(board_x - 10, board_y - 10, board_width + 20, board_height + 20))
            
            result = check_winner()
            if result:
                game_over = True
                learning_history['total_games'] += 1
                
                for board_state, move in game_history:
                    if board_state in move_stats and move in move_stats[board_state]:
                        if result == 'Ничья':
                            move_stats[board_state][move]['draws'] += 1
                            learning_history['draws'] += 1
                        elif (result == 'X' and player == 'O') or (result == 'O' and player == 'X'):
                            move_stats[board_state][move]['wins'] += 1
                            learning_history['ai_wins'] += 1
                        else:
                            move_stats[board_state][move]['losses'] += 1
                            learning_history['player_wins'] += 1
                
                # Обновляем скорость обучения
                learning_history = update_learning_rate(learning_history)
                
                # Уменьшаем вероятность исследования
                exploration_rate = max(0.05, exploration_rate * 0.995)
                
                if result == 'Ничья':
                    update_game_result(board, 'draw')
                    update_game_stats('draw')
                    logging.info(f"Игра {game_num}: Ничья")
                else:
                    update_game_result(board, result)
                    update_game_stats(result)
                    logging.info(f"Игра {game_num}: Победил {result}")
                
                draw_stats()
                pygame.display.update(pygame.Rect(stats_x - 10, stats_y - 10, stats_width + 20, height - 40))
            
            pygame.time.wait(50)
    
    if not self_learning:
        board = current_board
        player = current_player
        game_over = current_game_over
        available_moves = current_available_moves
        reset_game()
    else:
        for board_state, moves in move_stats.items():
            save_game_state(list(board_state), moves)
        
        # Сохраняем историю обучения
        save_learning_history(learning_history)
        logging.info("Завершение процесса самообучения")
        logging.info(f"Финальная статистика: {learning_history}")


def play_game():
    global game_over, screen, player, ai_plays_for_x, self_learning
    init_db()
    
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Крестики-нолики')
    
    board = [' ' for _ in range(9)]
    player = 'X'
    game_over = False
    available_moves = [i for i in range(9)]
    
    reset_game()
    exit_button = None
    restart_button = None
    bot_button = None
    self_learning_button = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button and exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif restart_button and restart_button.collidepoint(event.pos):
                    reset_game()
                    game_over = False
                    player = 'X'
                elif bot_button and bot_button.collidepoint(event.pos):
                    ai_plays_for_x = not ai_plays_for_x
                    reset_game()
                elif self_learning_button and self_learning_button.collidepoint(event.pos):
                    self_learning = not self_learning
                    if self_learning:
                        self_learn()
                    else:
                        reset_game()
                elif not game_over and player == 'X' and not ai_plays_for_x and not self_learning:
                    x, y = pygame.mouse.get_pos()
                    if board_x <= x <= board_x + board_width and board_y <= y <= board_y + board_height:
                        col = int((x - board_x) // (board_width / 3))
                        row = int((y - board_y) // (board_height / 3))
                        position = row * 3 + col
                        make_move(position)
                        check_game_over()

        if not game_over and ((player == 'O') or (player == 'X' and (ai_plays_for_x or self_learning))):
            play_ai_move()
            check_game_over()
        
        exit_button, restart_button, bot_button, self_learning_button = draw_stats()
        pygame.display.update()


play_game()