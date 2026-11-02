from account import Account
from errors import CinemaError
from subscription import PLANS


class User:
    def __init__(self, name, has_subscription=False):
        if not name:
            raise CinemaError("Имя не может быть пустым")

        self.name = name
        self.watched = []

        # В старых файлах подписка true открывала все фильмы.
        self.account = Account(plan_id="3" if has_subscription else None)

    @property
    def has_subscription(self):
        return self.account.plan_id is not None

    def watch(self, movie):
        if not self.has_subscription:
            raise CinemaError("Сначала оформите подписку")

        plan = PLANS[self.account.plan_id]
        if not plan.allows(movie.genre):
            raise CinemaError(
                f"Жанр «{movie.genre}» не входит в тариф «{plan.name}»"
            )

        self.watched.append(movie.title)