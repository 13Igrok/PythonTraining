# Получаем текущий год и месяц
year = 2023
month = 10

# Создаем объект календаря
cal = calendar.monthcalendar(year, month)

# Выводим заголовок
print(calendar.month_name[month], year)

# Выводим названия дней недели
print("Пн Вт Ср Чт Пт Сб Вс")

# Выводим дни месяца
for week in cal:
    for day in week:
        if day == 0:
            print("  ", end=" ")
        else:
            print(f"{day:2d}", end=" ")
    print()
