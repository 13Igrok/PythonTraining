import sqlite3
import json

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Создаем таблицу для хранения состояний игры и лучших ходов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS game_states (
        board_state TEXT PRIMARY KEY,
        best_moves TEXT,
        wins INTEGER DEFAULT 0,
        losses INTEGER DEFAULT 0,
        draws INTEGER DEFAULT 0
    )
    ''')
    
    # Создаем таблицу для хранения общей статистики
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS game_stats (
        id INTEGER PRIMARY KEY,
        player_wins INTEGER DEFAULT 0,
        ai_wins INTEGER DEFAULT 0,
        draws INTEGER DEFAULT 0
    )
    ''')
    
    # Создаем запись статистики, если её нет
    cursor.execute('INSERT OR IGNORE INTO game_stats (id) VALUES (1)')
    
    conn.commit()
    conn.close()

def save_game_state(board_state, best_moves):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Преобразуем список в строку для хранения
    board_str = ''.join(board_state)
    best_moves_str = json.dumps(best_moves)
    
    cursor.execute('''
    INSERT OR REPLACE INTO game_states (board_state, best_moves)
    VALUES (?, ?)
    ''', (board_str, best_moves_str))
    
    conn.commit()
    conn.close()

def get_best_moves(board_state):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    board_str = ''.join(board_state)
    cursor.execute('SELECT best_moves FROM game_states WHERE board_state = ?', (board_str,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        return json.loads(result[0])
    return None

def update_game_result(board_state, result):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    board_str = ''.join(board_state)
    if result == 'X':
        cursor.execute('UPDATE game_states SET wins = wins + 1 WHERE board_state = ?', (board_str,))
    elif result == 'O':
        cursor.execute('UPDATE game_states SET losses = losses + 1 WHERE board_state = ?', (board_str,))
    else:
        cursor.execute('UPDATE game_states SET draws = draws + 1 WHERE board_state = ?', (board_str,))
    
    conn.commit()
    conn.close()

def get_game_stats():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT player_wins, ai_wins, draws FROM game_stats WHERE id = 1')
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        return {
            'player_wins': result[0],
            'ai_wins': result[1],
            'draws': result[2]
        }
    return {'player_wins': 0, 'ai_wins': 0, 'draws': 0}

def update_game_stats(result):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    if result == 'X':
        cursor.execute('UPDATE game_stats SET player_wins = player_wins + 1 WHERE id = 1')
    elif result == 'O':
        cursor.execute('UPDATE game_stats SET ai_wins = ai_wins + 1 WHERE id = 1')
    else:
        cursor.execute('UPDATE game_stats SET draws = draws + 1 WHERE id = 1')
    
    conn.commit()
    conn.close() 