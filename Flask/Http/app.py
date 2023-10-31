from flask import Flask, render_template

app = Flask(__name__)

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Страница "Регистрации"
@app.route('/registration')
def about():
    return render_template('registration.html')

# Страница "О нас"
@app.route('/about')
def about():
    return render_template('about.html')

# Страница "Контакты"
@app.route('/contact')
def contact():
    return render_template('contact.html')



if __name__ == '__main__':
    app.run()