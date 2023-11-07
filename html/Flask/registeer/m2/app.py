from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Создание базы данных SQLite
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Создание таблицы пользователей
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT,
                   password TEXT)''')
conn.commit()

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Добавление пользователя в базу данных
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()

        return redirect('/success')

    return render_template('register.html')

@app.route('/success')
def success():
    return 'Регистрация прошла успешно!'

if __name__ == '__main__':
    app.run()
