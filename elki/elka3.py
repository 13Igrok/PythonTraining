import turtle
import time
import random
import datetime

# Создаем экран
screen = turtle.Screen()
screen.bgcolor("black")

# Создаем елку
tree = turtle.Turtle()
tree.color("green")
tree.width(5)
tree.speed(10)

# Функция для рисования 2D-елки
def draw_2d_tree():
    tree.forward(100)
    tree.left(120)
    tree.forward(100)
    tree.left(120)
    tree.forward(100)
    tree.left(120)

# Рисуем 2D-елку
draw_2d_tree()

# Создаем мерцающую гирлянду с большим количеством огоньков
lights = [turtle.Turtle() for _ in range(50)]
colors = ["red", "orange", "yellow", "green", "blue", "purple"]

# Функция для мерцания гирлянды
def twinkle():
    for light in lights:
        light.color(random.choice(colors))
        light.penup()
        light.goto(random.randint(-200, 200), random.randint(-200, 200))

# Мерцающая гирлянда
while True:
    twinkle()
    time.sleep(0.5)

# Добавляем изображение Деда Мороза
screen.addshape("santa.gif")
santa = turtle.Turtle()
santa.shape("santa.gif")
santa.penup()
santa.goto(0, -200)

# Добавляем надпись "С Новым Годом"
new_year_text = turtle.Turtle()
new_year_text.hideturtle()
new_year_text.color("white")
new_year_text.write("С Новым Годом!", align="center", font=("Arial", 30, "normal"))

# Таймер до Нового Года
new_year = datetime.datetime(datetime.datetime.now().year + 1, 1, 1)
time_left = new_year - datetime.datetime.now()
timer_text = turtle.Turtle()
timer_text.hideturtle()
timer_text.color("white")
timer_text.write(f"До Нового Года осталось: {time_left.days} дней {time_left.seconds // 3600} часов {time_left.seconds % 3600 // 60} минут", align="center", font=("Arial", 12, "normal"))

turtle.done()
