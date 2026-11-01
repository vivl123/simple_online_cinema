import json
import xml.etree.ElementTree as ET
from cinema import Cinema
from movie import Movie
from user import User
from errors import CinemaError
import storage


cinema = Cinema()

while True:
    print("\n1 Фильмы  2 Добавить фильм  3 Добавить пользователя  4 Смотреть")
    print("5 Сохранить JSON  6 Загрузить JSON  7 Сохранить XML  8 Загрузить XML  0 Выход")
    command = input("Команда: ")

    try:
        if command == "0":
            break
        elif command == "1":
            for movie in cinema.movies:
                print(movie.title, "—", movie.genre, movie.year)
        elif command == "2":
            title = input("Название: ")
            genre = input("Жанр: ")
            year = int(input("Год: "))
            cinema.add_movie(Movie(title, genre, year))
            print("Фильм добавлен")
        elif command == "3":
            name = input("Имя: ")
            answer = input("Есть подписка? да/нет: ").lower()
            if answer not in ("да", "нет"):
                raise CinemaError("Ответьте да или нет")
            cinema.add_user(User(name, answer == "да"))
            print("Пользователь добавлен")
        elif command == "4":
            user = cinema.find_user(input("Имя пользователя: "))
            movie = cinema.find_movie(input("Название фильма: "))
            user.watch(movie)
            print("Просмотр записан")
        elif command == "5":
            storage.save_json(cinema, input("Имя файла: "))
            print("JSON сохранён")
        elif command == "6":
            cinema = storage.load_json(input("Имя файла: "))
            print("JSON загружен")
        elif command == "7":
            storage.save_xml(cinema, input("Имя файла: "))
            print("XML сохранён")
        elif command == "8":
            cinema = storage.load_xml(input("Имя файла: "))
            print("XML загружен")
        else:
            print("Нет такой команды")
    except (CinemaError, ValueError, OSError, json.JSONDecodeError, ET.ParseError) as error:
        print("Ошибка:", error)
