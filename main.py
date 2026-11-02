import xml.etree.ElementTree as ET

import account_actions
import cinema_actions
import storage
from cinema import Cinema
from errors import CinemaError
from menu import show_menu


def main():
    cinema = Cinema()
    user = None

    while True:
        show_menu(user)
        command = input("  Выберите действие → ").strip()

        if command == "0":
            print("  До встречи!")
            break

        if command in {"3", "4", "7", "8", "9"} and user is None:
            print("  Сначала создайте пользователя (5) или выберите его (6).")
            continue

        try:
            if command == "1":
                cinema_actions.show_movies(cinema)
            elif command == "2":
                cinema_actions.add_movie(cinema)
            elif command == "3":
                cinema_actions.watch_movie(cinema, user)
            elif command == "4":
                cinema_actions.show_recommendations(cinema, user)
            elif command == "5":
                user = account_actions.create_user(cinema)
            elif command == "6":
                user = account_actions.select_user(cinema, user)
            elif command == "7":
                account_actions.deposit(user)
            elif command == "8":
                account_actions.buy_plan(user)
            elif command == "9":
                cinema_actions.show_history(cinema, user)
            elif command in {"10", "11"}:
                loaded = storage.file_menu(cinema, saving=(command == "10"))
                if loaded is not None:
                    cinema = loaded
                    user = None
            else:
                print("  Выберите действие от 0 до 11.")

        except (CinemaError, ValueError, OSError, ET.ParseError) as error:
            print(f"  Ошибка: {error}")


if __name__ == "__main__":
    main()