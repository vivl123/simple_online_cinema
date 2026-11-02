"""Запись и чтение одного каталога в JSON и XML."""
import json
import xml.etree.ElementTree as ET
from cinema import Cinema
from movie import Movie
from user import User
from errors import CinemaError
from menu import choose_item, read_filename

def save_json(cinema, filename):
    data = {"movies": [], "users": []}
    for movie in cinema.movies:
        data["movies"].append({"title": movie.title, "genre": movie.genre, "year": movie.year})
    for user in cinema.users:
        data["users"].append({"name": user.name, "has_subscription": user.has_subscription,
                              "watched": user.watched})
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict) or not isinstance(data.get("movies"), list) or not isinstance(data.get("users"), list):
        raise CinemaError("Неверная структура JSON")
    cinema = Cinema()
    try:
        for item in data["movies"]:
            cinema.add_movie(Movie(item["title"], item["genre"], int(item["year"])))
        for item in data["users"]:
            if not isinstance(item["has_subscription"], bool) or not isinstance(item["watched"], list):
                raise CinemaError("Неверные данные пользователя")
            user = User(item["name"], item["has_subscription"])
            for title in item["watched"]:
                cinema.find_movie(title)
                user.watched.append(title)
            cinema.add_user(user)
    except (KeyError, TypeError, AttributeError) as error:
        raise CinemaError("Неверные данные JSON: " + str(error))
    return cinema


def save_xml(cinema, filename):
    root = ET.Element("cinema")
    movies = ET.SubElement(root, "movies")
    for movie in cinema.movies:
        item = ET.SubElement(movies, "movie")
        ET.SubElement(item, "title").text = movie.title
        ET.SubElement(item, "genre").text = movie.genre
        ET.SubElement(item, "year").text = str(movie.year)
    users = ET.SubElement(root, "users")
    for user in cinema.users:
        item = ET.SubElement(users, "user")
        ET.SubElement(item, "name").text = user.name
        ET.SubElement(item, "has_subscription").text = str(user.has_subscription).lower()
        watched = ET.SubElement(item, "watched")
        for title in user.watched:
            ET.SubElement(watched, "title").text = title
    ET.indent(root, space="  ")
    ET.ElementTree(root).write(filename, encoding="utf-8", xml_declaration=True)


def load_xml(filename):
    root = ET.parse(filename).getroot()
    if root.tag != "cinema" or root.find("movies") is None or root.find("users") is None:
        raise CinemaError("Неверная структура XML")
    cinema = Cinema()
    for item in root.findall("./movies/movie"):
        title = item.findtext("title")
        genre = item.findtext("genre")
        year = item.findtext("year")
        if title is None or genre is None or year is None:
            raise CinemaError("Неполные данные фильма в XML")
        cinema.add_movie(Movie(title, genre, int(year)))
    for item in root.findall("./users/user"):
        name = item.findtext("name")
        subscription = item.findtext("has_subscription")
        if name is None or subscription not in ("true", "false"):
            raise CinemaError("Неверные данные пользователя в XML")
        user = User(name, subscription == "true")
        for title in item.findall("./watched/title"):
            cinema.find_movie(title.text)
            user.watched.append(title.text)
        cinema.add_user(user)
    return cinema
def file_menu(cinema, saving):
    """Возвращает новый каталог только после успешной загрузки."""
    action = "Сохранить каталог" if saving else "Загрузить каталог"
    file_format = choose_item(action, ["JSON", "XML"])

    if file_format is None:
        return None

    filename = read_filename(file_format)

    if saving:
        if file_format == "JSON":
            save_json(cinema, filename)
        else:
            save_xml(cinema, filename)

        print(f"  ✓ Каталог сохранён в {filename}.")
        return None

    if file_format == "JSON":
        loaded = load_json(filename)
    else:
        loaded = load_xml(filename)

    print("  ✓ Каталог загружен. Выберите пользователя через пункт 6.")
    return loaded