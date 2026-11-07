
from pathlib import Path

from cinema import Cinema
from menu import Menu
from storage import Storage


class FileActions:


    def __init__(self, menu: Menu) -> None:
        self.menu = menu

    def execute(self, cinema: Cinema, saving: bool) -> Cinema | None:
        action = "Сохранение" if saving else "Загрузка"
        file_format = self.menu.choose(action, ["JSON", "XML"])
        if file_format is None:
            return None
        filename = self.menu.filename(file_format)
        storage = Storage()
        if saving:
            if Path(filename).exists() and not self.menu.confirm(
                "Файл уже существует. Перезаписать?"
            ):
                return None
            storage.save(cinema, filename)
            print("  Каталог сохранён.")
            return None
        loaded = storage.load(filename)
        print("  Каталог загружен. Выберите пользователя через пункт 6.")
        return loaded
