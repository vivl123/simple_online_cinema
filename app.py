
import xml.etree.ElementTree as ET

import account_actions
from cinema import Cinema
import cinema_actions
from file_actions import FileActions
from menu import Menu
from user import User


class CinemaApp:


    def __init__(self) -> None:
        self.menu = Menu()
        self.files = FileActions(self.menu)
        self.user: User | None = None
        self.set_cinema(Cinema())

    def set_cinema(self, cinema: Cinema) -> None:
        self.cinema = cinema
        self.user = None

    def current_user(self) -> User:#метод должен возвращать объект класса User
        if self.user is None:
            raise ValueError("Сначала создайте или выберите пользователя")
        return self.user

    def execute(self, command: str) -> None:
        cinema = self.cinema
        menu = self.menu
        user = self.user

        if command == "1":
            cinema_actions.show_movies(cinema, menu)
        elif command == "2":
            cinema_actions.add_movie(cinema, menu)
        elif command == "3":
            cinema_actions.watch_movie(cinema, menu, self.current_user())
        elif command == "4":
            cinema_actions.show_recommendations(
                cinema, menu, self.current_user()
            )
        elif command == "5":
            self.user = account_actions.create_user(cinema, menu)
        elif command == "6":
            self.user = account_actions.select_user(cinema, menu, user)
        elif command == "7":
            account_actions.deposit(cinema, menu, self.current_user())
        elif command == "8":
            account_actions.buy_plan(cinema, menu, self.current_user())
        elif command == "9":
            cinema_actions.show_history(cinema, menu, self.current_user())
        elif command in {"10", "11"}:
            loaded = self.files.execute(cinema, command == "10")
            if loaded is not None:
                self.set_cinema(loaded)
        elif command == "12":
            cinema_actions.update_movie(cinema, menu)
        elif command == "13":
            cinema_actions.delete_movie(cinema, menu)
        elif command == "14":
            account_actions.show_users(cinema, menu)
        elif command == "15":
            account_actions.update_user(cinema, menu)
        elif command == "16":
            self.user = account_actions.delete_user(cinema, menu, user)
        else:
            print("  Выберите действие от 0 до 16.")

    def run(self) -> None:
        while True:
            try:
                self.menu.show(self.user)
                command = input("  Выберите действие : ").strip()#удаляет пробелы в начале и в конце строки
                if command == "0":
                    print("  До встречи!")
                    return
                self.execute(command)#'этот метод  опрделеяет какое дейтсвие выполнить
            except (EOFError, KeyboardInterrupt):
                print("\n  Работа завершена.")
                return
            except (ValueError, OSError, ET.ParseError) as error:
                print(f"  Ошибка: {error}")
