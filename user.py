from errors import CinemaError


class User:
    def __init__(self, name, has_subscription):
        if not name:
            raise CinemaError("Имя не может быть пустым")
        self.name = name
        self.has_subscription = has_subscription
        self.watched = []

    def watch(self, movie):
        if not self.has_subscription:
            raise CinemaError("Нужна подписка для просмотра")
        self.watched.append(movie.title)
