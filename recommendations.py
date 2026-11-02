from subscription import PLANS


class ViewingStats:
    def __init__(self, cinema, user):
        self.total_views = len(user.watched)
        self.genre_counts = {}

        for title in user.watched:
            movie = cinema.find_movie(title)
            genre = movie.genre.strip().lower()
            self.genre_counts[genre] = self.genre_counts.get(genre, 0) + 1

    def favorite_genres(self):
        if not self.genre_counts:
            return []

        maximum = max(self.genre_counts.values())
        return [
            genre for genre, count in self.genre_counts.items()
            if count == maximum
        ]


class MovieRecommender:
    def __init__(self, cinema):
        self.cinema = cinema

    def recommend(self, user):
        if not user.has_subscription:
            return []

        plan = PLANS[user.account.plan_id]
        stats = ViewingStats(self.cinema, user)
        favorites = stats.favorite_genres()
        watched = set(user.watched)
        result = []

        for movie in self.cinema.movies:
            genre = movie.genre.strip().lower()

            if movie.title in watched:
                continue

            if genre in favorites and plan.allows(movie.genre):
                result.append(movie)

        return result