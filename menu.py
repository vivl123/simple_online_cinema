
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

from movie import Movie
from subscription import PLANS
from user import User


class Menu:


    def section(self, title: str) -> None:
        print(f"\n── {title} " + "─" * max(2, 40 - len(title)))

    def text(self, prompt: str) -> str:
        while True:
            value = input(f"  {prompt}: ").strip()
            if value:
                return value
            print("  Поле не может быть пустым.")

    def number(self, prompt: str) -> int:
        while True:
            try:
                return int(input(f"  {prompt}: ").strip())
            except ValueError:
                print("  Введите целое число.")

    def choose(
        self, title: str, items: Sequence[Any],
        describe: Callable[[Any], str] = str,
    ) -> Any:
        self.section(title)
        if not items:
            print("  Список пуст.")
            return None
        for index, item in enumerate(items, 1):
            print(f"  {index}. {describe(item)}")
        print("  0. Назад")
        while True:
            index = self.number("Выбор")
            if index == 0:
                return None
            if 1 <= index <= len(items):
                return items[index - 1]
            print(f"  Введите номер от 0 до {len(items)}.")

    def confirm(self, prompt: str) -> bool:
        return self.choose(prompt, ["Нет", "Да"]) == "Да"

    def filename(self, file_format: str) -> str:
        extension = "." + file_format.lower()
        while True:
            filename = self.text(f"Имя файла, например cinema{extension}")
            suffix = Path(filename).suffix.lower()
            if not suffix:
                return filename + extension
            if suffix == extension:
                return filename
            print(f"  Требуется расширение {extension}.")

    def movie_label(self, movie: Movie) -> str:
        return f"{movie.title} ({movie.year}) · {movie.genre}"

    def show(self, user: User | None) -> None:
        self.section("ОНЛАЙН-КИНОТЕАТР")
        if user is None:
            print("  Гость")
        else:
            plan_id = user.account.plan_id
            tariff = PLANS[plan_id].name if plan_id else "не подключён"
            print(
                f"  {user.name} | {user.account.balance} ₽ | Тариф: {tariff}"
            )
        print("  КАТАЛОГ  | 1 Фильмы | 2 Добавить | 3 Смотреть | 4 Советы")
        print("  АККАУНТ  | 5 Создать | 6 Выбрать | 7 Баланс | 8 Тариф")
        print("  ДАННЫЕ   | 9 История | 10 Сохранить | 11 Загрузить")
        print("  ФИЛЬМЫ   | 12 Изменить | 13 Удалить")
        print("  ЛЮДИ     | 14 Список | 15 Переименовать | 16 Удалить")
        print("  0 Выход")
