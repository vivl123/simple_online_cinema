from menu import choose_item, show_section
from movie import Movie
from movie_catalog import MOVIE_CATALOG
from recommendations import MovieRecommender
from recommendations import MovieRecommender, ViewingStats


def movie_label(movie):
    return f"{movie.title} ({movie.year}) · {movie.genre}"


def show_movies(cinema):
    show_section("Каталог кинотеатра")

    if not cinema.movies:
        print("  Каталог пуст. Добавьте фильм через пункт 2.")
        return

    for number, movie in enumerate(cinema.movies, start=1):
        print(f"  {number:>2}. {movie_label(movie)}")


def add_movie(cinema):
    genre = choose_item("Выберите жанр", list(MOVIE_CATALOG))
    if genre is None:
        return

    selected = choose_item(
        f"Выберите фильм · {genre}",
        MOVIE_CATALOG[genre],
        lambda film: f"{film[0]} ({film[1]})",
    )
    if selected is None:
        return

    title, year = selected
    movie = Movie(title, genre, year)
    cinema.add_movie(movie)
    print(f"   Добавлен фильм: {movie_label(movie)}")


def watch_movie(cinema, user):
    movie = choose_item("Что смотрим?", cinema.movies, movie_label)
    if movie is not None:
        user.watch(movie)
        print(f"   «{movie.title}» добавлен в историю просмотров.")


def show_recommendations(cinema, user):
    show_section("Ваши рекомендации")

    if not user.has_subscription:
        print("  Подключите тариф через пункт 8.")
        return

    if not user.watched:
        print("  Посмотрите первый фильм через пункт 3.")
        return

    movies = MovieRecommender(cinema).recommend(user)
    if not movies:
        print("  По вашему тарифу пока нет новых фильмов любимых жанров.")
        return

    for number, movie in enumerate(movies, start=1):
        print(f"  {number:>2}. {movie_label(movie)}")


def show_history(cinema, user):
    show_section(f"История просмотров · {user.name}")

    if not user.watched:
        print("  Вы пока не смотрели фильмы.")
        return

    for number, title in enumerate(user.watched, start=1):
        print(f"  {number:>2}. {title}")

    stats = ViewingStats(cinema, user)
    print(f"\n  Всего просмотров: {stats.total_views}")

    for genre, count in stats.genre_counts.items():
        print(f"  {genre.capitalize()}: {count}")

    print("  Любимые жанры:", ", ".join(stats.favorite_genres()))