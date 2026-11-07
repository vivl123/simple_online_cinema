"""Чтение и запись каталога в JSON и XML."""
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from account import Account
from cinema import Cinema
from movie import Movie
from user import User


class Storage:
    """Хранит фильмы, пользователей, счета и историю в одном файле."""

    def save(self, cinema: Cinema, filename: str) -> None:
        if Path(filename).suffix.lower() == ".json":
            self.save_json(cinema, filename)
        elif Path(filename).suffix.lower() == ".xml":
            self.save_xml(cinema, filename)
        else:
            raise ValueError("Выберите формат JSON или XML")

    def load(self, filename: str) -> Cinema:
        if Path(filename).suffix.lower() == ".json":
            return self.load_json(filename)
        if Path(filename).suffix.lower() == ".xml":
            return self.load_xml(filename)
        raise ValueError("Выберите формат JSON или XML")

    def to_data(self, cinema: Cinema) -> dict[str, Any]:
            return {
                "movies": [
                    {"title": m.title, "genre": m.genre, "year": m.year}
                    for m in cinema.movies
                ],
                "users": [
                    {
                        "name": u.name,
                        "has_subscription": u.has_subscription,
                        "balance": u.account.balance,
                        "plan_id": u.account.plan_id,
                        "watched": list(u.watched),
                    }
                    for u in cinema.users
                ],
            }

    def from_data(self, data: Any) -> Cinema:
            if not isinstance(data, dict) or not all(
                isinstance(data.get(key), list) for key in ("movies", "users")
            ):
                raise ValueError("Неверная структура каталога")
            cinema = Cinema()
            try:
                for item in data["movies"]:
                    cinema.add_movie(
                        Movie(item["title"], item["genre"], item["year"])
                    )
                for item in data["users"]:
                    user = User(item["name"], item["has_subscription"])
                    user.account = Account(
                        item.get("balance", 0),
                        item.get("plan_id", user.account.plan_id),
                    )
                    if not isinstance(item["watched"], list):
                        raise ValueError("История должна быть списком")
                    for title in item["watched"]:
                        cinema.find_movie(title)
                        user.watched.append(title)
                    cinema.add_user(user)
            except (KeyError, TypeError, AttributeError) as error:
                raise ValueError("Неверные поля каталога") from error
            return cinema

    def save_json(self, cinema: Cinema, filename: str) -> None:
            data = self.to_data(cinema)
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)

    def load_json(self, filename: str) -> Cinema:
            with open(filename, encoding="utf-8") as file:
                data = json.load(file)
            return self.from_data(data)

    def save_xml(self, cinema: Cinema, filename: str) -> None:
            data = self.to_data(cinema)
            root = ET.Element("cinema")
            movies = ET.SubElement(root, "movies")
            for movie in data["movies"]:
                item = ET.SubElement(movies, "movie")
                for key, value in movie.items():
                    ET.SubElement(item, key).text = str(value)
            users = ET.SubElement(root, "users")
            for user in data["users"]:
                item = ET.SubElement(users, "user")
                ET.SubElement(item, "name").text = user["name"]
                ET.SubElement(item, "has_subscription").text = str(
                    user["has_subscription"]
                ).lower()
                ET.SubElement(item, "balance").text = str(user["balance"])
                # Пустой тег явно обозначает отсутствие тарифа.
                ET.SubElement(item, "plan_id").text = user["plan_id"] or ""
                watched = ET.SubElement(item, "watched")
                for title in user["watched"]:
                    ET.SubElement(watched, "title").text = title
            ET.indent(root, space="  ")
            ET.ElementTree(root).write(
                filename, encoding="utf-8", xml_declaration=True
            )

    def load_xml(self, filename: str) -> Cinema:
            root = ET.parse(filename).getroot()
            if (
                root.tag != "cinema"
                or root.find("movies") is None
                or root.find("users") is None
            ):
                raise ValueError("Неверная структура XML")
            data: dict[str, Any] = {"movies": [], "users": []}
            for item in root.findall("./movies/movie"):
                data["movies"].append({
                    "title": item.findtext("title"),
                    "genre": item.findtext("genre"),
                    "year": int(item.findtext("year", "")),
                })
            for item in root.findall("./users/user"):
                subscription = item.findtext("has_subscription")
                if subscription not in ("true", "false"):
                    raise ValueError("Неверный признак подписки в XML")
                user: dict[str, Any] = {
                    "name": item.findtext("name"),
                    "has_subscription": subscription == "true",
                    "balance": int(item.findtext("balance", "0")),
                    "watched": [
                        title.text for title in item.findall("./watched/title")
                    ],
                }
                # В старом XML тега нет: используем прежний has_subscription.
                if item.find("plan_id") is not None:
                    user["plan_id"] = item.findtext("plan_id") or None
                data["users"].append(user)
            return self.from_data(data)
