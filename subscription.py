class SubscriptionPlan:
    def __init__(self, name, price, genres=None):
        self.name = name
        self.price = price
        self.genres = genres

    def allows(self, genre):
        if self.genres is None:
            return True
        return genre.strip().lower() in self.genres


PLANS = {
    "1": SubscriptionPlan("Фантастика", 150, {"фантастика"}),
    "2": SubscriptionPlan("Комедии и драмы", 200, {"комедия", "драма"}),
    "3": SubscriptionPlan("Полный", 350),
}