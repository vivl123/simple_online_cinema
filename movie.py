"""Модель фильма."""


class Movie:
    """Хранит проверенные сведения о фильме."""

    def __init__(self, title: str, genre: str, year: int) -> None:
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Название фильма не заполнено")
        if not isinstance(genre, str) or not genre.strip():
            raise ValueError("Жанр фильма не заполнен")
        if type(year) is not int or year < 1888:
            raise ValueError("Год должен быть целым числом от 1888")
        self.title = title.strip()
        self.genre = genre.strip()
        self.year = year
