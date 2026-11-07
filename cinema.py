from movie import Movie
from user import User

class Cinema:

    def __init__(self) -> None:
        self.movies: list[Movie] = []
        self.users: list[User] = []

    def add_movie(self, movie: Movie) -> None:
        if any(old.title == movie.title for old in self.movies):
            raise ValueError("Такой фильм уже есть")
        self.movies.append(movie)

    def add_user(self, user: User) -> None:
        if any(old.name == user.name for old in self.users):
            raise ValueError("Такой пользователь уже есть")
        self.users.append(user)

    def find_movie(self, title: str) -> Movie:
        for movie in self.movies:
            if movie.title == title:
                return movie
        raise ValueError("Фильм не найден")

    def find_user(self, name: str) -> User:
        for user in self.users:
            if user.name == name:
                return user
        raise ValueError("Пользователь не найден")

    def update_movie(self, old_title: str, title: str, genre: str, year: int) -> None:
        movie = self.find_movie(old_title)
        replacement = Movie(title, genre, year)
        if any(other is not movie and other.title == replacement.title for other in self.movies):
            raise ValueError("Такой фильм уже есть")
        movie.title = replacement.title
        movie.genre = replacement.genre
        movie.year = replacement.year
        for user in self.users:
            user.watched = [
                movie.title if name == old_title else name
                for name in user.watched
            ]

    def delete_movie(self, title: str) -> None:
        movie = self.find_movie(title)
        self.movies.remove(movie)
        for user in self.users:
            user.watched = [name for name in user.watched if name != title]

    def update_user(self, old_name: str, new_name: str) -> None:
        user = self.find_user(old_name)
        replacement = User(new_name)
        if any(
            other is not user and other.name == replacement.name
            for other in self.users
        ):
            raise ValueError("Такой пользователь уже есть")
        user.name = replacement.name

    def delete_user(self, name: str) -> None:
        self.users.remove(self.find_user(name))
