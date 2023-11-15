import turtle

# Создаем экран для рисования
screen = turtle.Screen()

# Создаем черепашку
t = turtle.Turtle()

# Рисуем круг для лица
t.circle(100)

# Рисуем глаза
t.penup()
t.goto(-40, 120)
t.pendown()
t.circle(20)
t.penup()
t.goto(40, 120)
t.pendown()
t.circle(20)

# Рисуем рот
t.penup()
t.goto(-40, 80)
t.pendown()
t.setheading(-60)
t.circle(40, 120)

# Закрываем окно после клика
screen.exitonclick()
