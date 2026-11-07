"""Команды каталога и просмотров."""
from cinema import Cinema
from menu import Menu
from movie import Movie
from movie_catalog import MOVIE_CATALOG, movies_in_genre
from recommendations import MovieRecommender
from user import User


def show_movies(cinema: Cinema, menu: Menu) -> None:
    menu.section("Каталог")
    if not cinema.movies:
        print("  Каталог пуст.")
    for movie in cinema.movies:
        print(" ", menu.movie_label(movie))


def select_catalog_movie(cinema: Cinema, menu: Menu) -> Movie | None:
    genre = menu.choose("Жанр", list(MOVIE_CATALOG))
    if genre is None:
        return None
    return menu.choose(
        "Фильм", movies_in_genre(genre),
        menu.movie_label,
    )


def add_movie(cinema: Cinema, menu: Menu) -> None:
    movie = select_catalog_movie(cinema, menu)
    if movie is not None:
        cinema.add_movie(movie)
        print("  Фильм добавлен.")


def update_movie(cinema: Cinema, menu: Menu) -> None:
    old = menu.choose(
        "Какую запись изменить?", cinema.movies,
        menu.movie_label,
    )
    if old is None:
        return
    # Новые данные также берутся из справочника, чтобы не менять жанр
    # произвольным вводом. История обновляется внутри Cinema.
    new = select_catalog_movie(cinema, menu)
    if new is None:
        return
    if menu.confirm("Заменить запись и обновить её в истории?"):
        cinema.update_movie(
            old.title, new.title, new.genre, new.year
        )
        print("  Запись обновлена.")


def delete_movie(cinema: Cinema, menu: Menu) -> None:
    movie = menu.choose(
        "Удалить фильм", cinema.movies, menu.movie_label
    )
    if movie is not None and menu.confirm(
        "Удалить фильм и все записи о его просмотрах?"
    ):
        cinema.delete_movie(movie.title)
        print("  Фильм удалён.")


def watch_movie(cinema: Cinema, menu: Menu, user: User) -> None:
    movie = menu.choose(
        "Что смотрим?", cinema.movies, menu.movie_label
    )
    if movie is not None:
        user.watch(movie)
        print("  Просмотр записан.")


def show_recommendations(cinema: Cinema, menu: Menu, user: User) -> None:
    menu.section("Рекомендации")
    if not user.has_subscription:
        print("  Подключите тариф.")
        return
    if not user.watched:
        print("  Сначала посмотрите фильм.")
        return
    movies = MovieRecommender(cinema).recommend(user)
    if not movies:
        print("  Доступных новых фильмов любимых жанров пока нет.")
    for movie in movies:
        print(" ", menu.movie_label(movie))


def show_history(cinema: Cinema, menu: Menu, user: User) -> None:
    menu.section("История просмотров")
    for title in user.watched:
        print(" ", title)
    print(f"  Всего просмотров: {len(user.watched)}")
    counts = MovieRecommender(cinema).genre_counts(user)
    for genre, count in counts.items():
        print(f"  {genre}: {count}")
