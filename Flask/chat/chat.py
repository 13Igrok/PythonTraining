from flask import Flask, render_template, request

app = Flask(__name__)

# Список сообщений
messages = []

@app.route("/")
def index():
return render_template("index.html", messages=messages)

@app.route("/send_message", methods=["POST"])
def send_message():
# Получаем данные из формы
username = request.form.get("username")
message = request.form.get("message")

# Добавляем сообщение в список
messages.append({"username": username, "message": message})

return render_template("index.html", messages=messages)

if __name__ == "__main__":
app.run(debug=True)
