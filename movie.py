from errors import CinemaError


class Movie:
    def __init__(self, title, genre, year):
        if not title or not genre:
            raise CinemaError("Название и жанр не могут быть пустыми")
        if year < 1888:
            raise CinemaError("Неверный год фильма")
        self.title = title
        self.genre = genre
        self.year = year
