import time

def countdown_to_new_year():
    current_time = time.localtime()
    remaining_time = time.mktime((current_time.tm_year + 1, 1, 1, 0, 0, 0, 0, 0, 0)) - time.mktime(current_time)
    days = int(remaining_time // (24 * 3600))
    remaining_time = remaining_time % (24 * 3600)
    hours = int(remaining_time // 3600)
    remaining_time %= 3600
    minutes = int(remaining_time // 60)
    remaining_time %= 60
    seconds = int(remaining_time)
    print(f'До Нового Года осталось {days} дней, {hours} часов, {minutes} минут и {seconds} секунд')

def fireworks_with_message(message):
    print(f'Салют с надписью: {message}')

fireworks_with_message('С Новым Годом!')
countdown_to_new_year()
