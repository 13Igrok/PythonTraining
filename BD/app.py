import sqlite3

# Создание подключения к базе данных
conn = sqlite3.connect('database.db')

# Создание курсора для выполнения SQL-запросов
cursor = conn.cursor()

# Создание таблицы пользователей, если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT,
                   password TEXT)''')

# Функция для регистрации нового пользователя
def register_user(username, password):
    # Проверка, что пользователь с таким именем не существует
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        print("Пользователь с таким именем уже существует.")
        return
    
    # Вставка нового пользователя в таблицу
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    print("Пользователь успешно зарегистрирован.")

# Пример использования функции регистрации
register_user("john123", "password123")

# Закрытие соединения с базой данных
conn.close()
