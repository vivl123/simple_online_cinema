from errors import CinemaError


class Cinema:
    def __init__(self):
        self.movies = []
        self.users = []

    def add_movie(self, movie):
        for old_movie in self.movies:
            if old_movie.title == movie.title:
                raise CinemaError("Такой фильм уже есть")
        self.movies.append(movie)

    def add_user(self, user):
        for old_user in self.users:
            if old_user.name == user.name:
                raise CinemaError("Такой пользователь уже есть")
        self.users.append(user)

    def find_movie(self, title):
        for movie in self.movies:
            if movie.title == title:
                return movie
        raise CinemaError("Фильм не найден")

    def find_user(self, name):
        for user in self.users:
            if user.name == name:
                return user
        raise CinemaError("Пользователь не найден")
