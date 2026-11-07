"""Пользователь и его история просмотров."""
from account import Account
from movie import Movie
from subscription import PLANS


class User:
    """Объединяет имя, аккаунт и историю названий."""

    def __init__(self, name: str, has_subscription: bool = False) -> None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Имя не может быть пустым")
        if type(has_subscription) is not bool:
            raise ValueError("Признак подписки должен быть логическим")
        self.name = name.strip()
        self.watched: list[str] = []
        # Совместимость с прежними файлами: true означало полный доступ.
        self.account = Account(plan_id="3" if has_subscription else None)

    @property
    def has_subscription(self) -> bool:
        """Вычисляемый признак, зависящий от текущего тарифа."""
        return self.account.plan_id is not None

    def watch(self, movie: Movie) -> None:
        """Записывает просмотр только после проверки доступа."""
        plan_id = self.account.plan_id
        if plan_id is None:
            raise ValueError("Сначала оформите подписку")
        plan = PLANS[plan_id]
        if not plan.allows(movie.genre):
            raise ValueError(
                f"Жанр «{movie.genre}» не входит в тариф «{plan.name}»"
            )
        self.watched.append(movie.title)
