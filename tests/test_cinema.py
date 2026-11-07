"""Регрессионные проверки CRUD, файлов и команд меню."""
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import CinemaApp
from cinema import Cinema
from movie import Movie
from recommendations import MovieRecommender
from storage import Storage
from user import User


class CinemaTests(unittest.TestCase):
    """Проверяет состояние после успешных и отклонённых действий."""

    def setUp(self) -> None:
        self.cinema = Cinema()
        self.user = User("Анна")
        self.cinema.add_user(self.user)
        for title, genre in [
            ("Интерстеллар", "Фантастика"),
            ("Марсианин", "Фантастика"),
            ("Заклятие", "Ужасы"),
        ]:
            self.cinema.add_movie(Movie(title, genre, 2014))
        self.user.account.deposit(200)
        self.user.account.buy_plan("1")
        self.user.watch(self.cinema.movies[0])

    def test_denied_actions_preserve_state(self) -> None:
        with self.assertRaises(ValueError):
            self.user.account.buy_plan("3")
        with self.assertRaises(ValueError):
            self.user.account.buy_plan("1")
        with self.assertRaises(ValueError):
            self.user.account.deposit(-100)
        with self.assertRaises(ValueError):
            self.user.watch(self.cinema.movies[2])
        self.assertEqual(self.user.account.balance, 50)
        self.assertEqual(self.user.account.plan_id, "1")
        self.assertEqual(self.user.watched, ["Интерстеллар"])

    def test_movie_crud_and_history(self) -> None:
        self.cinema.update_movie(
            "Интерстеллар", "Матрица", "Фантастика", 1999
        )
        self.assertEqual(self.user.watched, ["Матрица"])
        self.assertEqual(self.cinema.find_movie("Матрица").year, 1999)
        with self.assertRaises(ValueError):
            self.cinema.update_movie("Матрица", "Марсианин", "Драма", 2000)
        self.assertEqual(self.cinema.find_movie("Матрица").year, 1999)
        self.cinema.delete_movie("Матрица")
        self.assertEqual(self.user.watched, [])
        with self.assertRaises(ValueError):
            self.cinema.find_movie("Матрица")

    def test_user_crud_preserves_account(self) -> None:
        self.cinema.add_user(User("Даниил"))
        with self.assertRaises(ValueError):
            self.cinema.update_user("Анна", "Даниил")
        self.cinema.update_user("Анна", "Аня")
        self.assertIs(self.cinema.find_user("Аня"), self.user)
        self.assertEqual(self.user.account.balance, 50)
        self.cinema.delete_user("Аня")
        self.assertEqual([u.name for u in self.cinema.users], ["Даниил"])

    def test_recommendations(self) -> None:
        movies = MovieRecommender(self.cinema).recommend(self.user)
        self.assertEqual([m.title for m in movies], ["Марсианин"])

    def test_round_trip_both_formats(self) -> None:
        self.cinema.add_user(User("Без подписки"))
        self.cinema.users[-1].account.deposit(75)
        with tempfile.TemporaryDirectory() as folder:
            for backend, extension in [
                (Storage(), "json"), (Storage(), "xml")
            ]:
                path = str(Path(folder) / ("data." + extension))
                backend.save(self.cinema, path)
                restored = backend.load(path)
                first, second = restored.users
                self.assertEqual(first.account.balance, 50)
                self.assertEqual(first.account.plan_id, "1")
                self.assertEqual(first.watched, ["Интерстеллар"])
                self.assertEqual(second.account.balance, 75)
                self.assertIsNone(second.account.plan_id)

    def test_old_samples(self) -> None:
        root = Path(__file__).resolve().parents[1]
        for backend, filename in [
            (Storage(), "sample_data.json"),
            (Storage(), "annacinema.json"),
            (Storage(), "sample_data.xml"),
        ]:
            restored = backend.load(str(root / filename))
            self.assertTrue(restored.movies)
            for user in restored.users:
                self.assertEqual(user.account.balance, 0)

    def test_invalid_data_and_failed_load_keep_catalog(self) -> None:
        app = CinemaApp()
        app.set_cinema(self.cinema)
        app.user = self.user
        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / "bad.json")
            Path(path).write_text(
                json.dumps({"movies": [], "users": [{}]}), encoding="utf-8"
            )
            with patch("builtins.input", side_effect=["1", path]):
                with redirect_stdout(StringIO()):
                    with self.assertRaises(ValueError):
                        app.execute("11")
        self.assertIs(app.cinema, self.cinema)
        self.assertIs(app.user, self.user)

    def test_successful_load_resets_user(self) -> None:
        app = CinemaApp()
        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / "good.json")
            Storage().save(self.cinema, path)
            with patch("builtins.input", side_effect=["1", path]):
                with redirect_stdout(StringIO()):
                    app.execute("11")
        self.assertIsNone(app.user)
        self.assertEqual(app.cinema.users[0].account.balance, 50)

    def test_current_user_deleted_from_menu(self) -> None:
        app = CinemaApp()
        app.set_cinema(self.cinema)
        app.user = self.user
        with patch("builtins.input", side_effect=["1", "2"]):
            with redirect_stdout(StringIO()):
                app.execute("16")
        self.assertIsNone(app.user)
        self.assertEqual(app.cinema.users, [])

    def test_full_console_flow(self) -> None:
        app = CinemaApp()
        # Создать; пополнить; купить; добавить из справочника; посмотреть;
        # показать историю; заменить фильм; переименовать; удалить; выйти.
        answers = [
            "5", "Анна", "7", "200", "8", "1",
            "2", "1", "1", "3", "1", "9",
            "12", "1", "1", "2", "2",
            "15", "1", "Аня", "13", "1", "2", "0",
        ]
        output = StringIO()
        with patch("builtins.input", side_effect=answers):
            with redirect_stdout(output):
                app.run()
        self.assertNotIn("Ошибка:", output.getvalue())
        self.assertEqual(app.cinema.movies, [])
        self.assertEqual(app.cinema.users[0].name, "Аня")
        self.assertEqual(app.cinema.users[0].account.balance, 50)
        self.assertEqual(app.cinema.users[0].watched, [])


if __name__ == "__main__":
    unittest.main()
