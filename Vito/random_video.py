import random
import requests
from sentence_transformers import SentenceTransformer

# База данных фильмов
films_database = [
    {'title': 'Начало', 'country': 'США', 'genre': 'фантастика', 'year': 2010},
    {'title': 'Побег из Шоушенка', 'country': 'США', 'genre': 'драма', 'year': 1994},
    {'title': 'Крестный отец', 'country': 'США', 'genre': 'криминал', 'year': 1972},
    {'title': 'Темный рыцарь', 'country': 'США', 'genre': 'боевик', 'year': 2008},
    {'title': 'Брат', 'country': 'Россия', 'genre': 'криминал', 'year': 1997},
    {'title': 'Сталкер', 'country': 'СССР', 'genre': 'фантастика', 'year': 1979},
    {'title': 'Амели', 'country': 'Франция', 'genre': 'мелодрама', 'year': 2001},
    {'title': 'Унесенные призраками', 'country': 'Япония', 'genre': 'аниме', 'year': 2001},
    {'title': 'Паразиты', 'country': 'Корея Южная', 'genre': 'триллер', 'year': 2019},
    {'title': 'Достучаться до небес', 'country': 'Германия', 'genre': 'драма', 'year': 1997},
    {'title': 'Леон', 'country': 'Франция', 'genre': 'боевик', 'year': 1994},
    {'title': 'Властелин колец: Братство кольца', 'country': 'Новая Зеландия', 'genre': 'фэнтези', 'year': 2001},
    {'title': 'Гладиатор', 'country': 'США', 'genre': 'исторический', 'year': 2000},
    {'title': 'Джентльмены', 'country': 'Великобритания', 'genre': 'криминал', 'year': 2019},
    {'title': 'Достать ножи', 'country': 'США', 'genre': 'детектив', 'year': 2019},
]

# Инициализация модели для векторизации
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def search_movie_online(title):
    """Ищет фильм в интернете по названию"""
    try:
        response = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key=YOUR_API_KEY&query={title}")
        data = response.json()
        if data['results']:
            return data['results'][0]  # Возвращает первый найденный фильм
        else:
            return None
    except Exception as e:
        print(f"Ошибка при поиске фильма в интернете: {e}")
        return None

def get_random_film():
    """Генерирует случайные параметры для фильма"""
    try:
        random_film = random.choice(films_database)
        return random_film['title'], random_film['country'], random_film['genre'], random_film['year']
    except Exception as e:
        print(f"Произошла ошибка при генерации фильма: {e}")
        return None, None, None, None

def main():
    while True:
        print("\n=== Генератор случайных фильмов ===")
        title, country, genre, year = get_random_film()
        
        if title:
            print(f"\nВаш фильм на сегодня!")
            print(f"Название: {title}")
            print(f"Страна: {country}")
            print(f"Жанр: {genre}")
            print(f"Год: {year}")
            
            # Поиск фильма в интернете
            online_movie = search_movie_online(title)
            if online_movie:
                print(f"Информация из интернета: {online_movie['title']} ({online_movie['release_date']})")
            else:
                print("К сожалению, информация о фильме не найдена в интернете.")
        else:
            print("К сожалению, не удалось сгенерировать фильм.")
        
        choice = input("\nХотите найти еще один фильм? (да/нет): ").lower()
        if choice != 'да':
            print("Спасибо за использование генератора фильмов!")
            break

if __name__ == "__main__":
    main()