"""Тарифы и правила доступа."""


class SubscriptionPlan:
    """Тариф с фиксированной ценой в целых рублях."""

    def __init__(
        self, name: str, price: int, genres: set[str] | None = None
    ) -> None:
        if not name.strip() or type(price) is not int or price < 0:
            raise ValueError("Неверное название или стоимость тарифа")
        self.name = name
        self.price = price
        self.genres = (
            None if genres is None else {g.strip().lower() for g in genres}
        )

    def allows(self, genre: str) -> bool:
        """None означает доступ ко всем жанрам."""
        return self.genres is None or genre.strip().lower() in self.genres


PLANS: dict[str, SubscriptionPlan] = {
    "1": SubscriptionPlan("Фантастика", 150, {"фантастика"}),
    "2": SubscriptionPlan("Комедии и драмы", 200, {"комедия", "драма"}),
    "3": SubscriptionPlan("Полный", 350),
}
