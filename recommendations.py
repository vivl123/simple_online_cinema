"""Простые рекомендации на основе истории просмотров."""
from cinema import Cinema
from movie import Movie
from subscription import PLANS
from user import User


class MovieRecommender:
    """Считает любимые жанры и предлагает доступные новые фильмы."""

    def __init__(self, cinema: Cinema) -> None:
        self.cinema = cinema

    def genre_counts(self, user: User) -> dict[str, int]:
        counts: dict[str, int] = {}
        for title in user.watched:
            movie = self.cinema.find_movie(title)
            genre = movie.genre.lower()
            counts[genre] = counts.get(genre, 0) + 1
        return counts

    def recommend(self, user: User) -> list[Movie]:
        if user.account.plan_id is None:
            return []
        counts = self.genre_counts(user)
        if not counts:
            return []

        plan = PLANS[user.account.plan_id]
        maximum = max(counts.values())
        result = []
        for movie in self.cinema.movies:
            if movie.title in user.watched:
                continue
            if not plan.allows(movie.genre):
                continue
            if counts.get(movie.genre.lower(), 0) == maximum:
                result.append(movie)
        return result
