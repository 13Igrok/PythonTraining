import sqlite3

# Установка соединения с базой данных
conn = sqlite3.connect('minecraft.db')

# Создание курсора
cursor = conn.cursor()

# Создание таблицы
cursor.execute('''CREATE TABLE IF NOT EXISTS players
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT,
                   score INTEGER)''')

# Вставка данных в таблицу
cursor.execute("INSERT INTO players (name, score) VALUES (?, ?)", ('Steve', 100))
cursor.execute("INSERT INTO players (name, score) VALUES (?, ?)", ('Alex', 200))

# Получение данных из таблицы
cursor.execute("SELECT * FROM players")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Закрытие соединения с базой данных
conn.close()
