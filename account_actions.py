"""Команды пользователей и аккаунтов."""
from cinema import Cinema
from menu import Menu
from subscription import PLANS
from user import User


def create_user(cinema: Cinema, menu: Menu) -> User:
    user = User(menu.text("Имя"))
    cinema.add_user(user)
    print("  Пользователь создан.")
    return user


def select_user(
    cinema: Cinema, menu: Menu, current: User | None,) -> User | None:
    selected = menu.choose("Пользователи", cinema.users, lambda user: user.name )
    return selected if selected is not None else current


def show_users(cinema: Cinema, menu: Menu) -> None:
    menu.section("Все пользователи")
    if not cinema.users:
        print("  Пользователей пока нет.")
    for user in cinema.users:
        plan_id = user.account.plan_id
        tariff = PLANS[plan_id].name if plan_id else "без подписки"
        print(f"  {user.name} | {user.account.balance} ₽ | {tariff}")


def update_user(cinema: Cinema, menu: Menu) -> None:
    user = menu.choose("Кого переименовать?", cinema.users, lambda u: u.name)
    if user is not None:
        cinema.update_user(user.name, menu.text("Новое имя"))
        print("  Имя изменено.")

def delete_user(cinema: Cinema, menu: Menu, current: User | None) -> User | None:
    user = menu.choose("Кого удалить?", cinema.users, lambda u: u.name)
    if user is not None and menu.confirm("Удалить пользователя вместе с балансом и историей?"):
        cinema.delete_user(user.name)
        print("  Пользователь удалён.")
        if user is current:
            return None
    return current


def deposit(cinema: Cinema, menu: Menu, user: User) -> None:
    print(f"  Баланс: {user.account.balance} ₽")
    amount = menu.number("Пополнение в рублях, 0 — назад")
    if amount != 0:
        user.account.deposit(amount)
        print(f"  Баланс: {user.account.balance} ₽")


def buy_plan(cinema: Cinema, menu: Menu, user: User) -> None:
    choice = menu.choose(
        "Тарифы", list(PLANS),
        lambda key: f"{PLANS[key].name} — {PLANS[key].price} ₽",
    )
    if choice is not None:
        user.account.buy_plan(choice)
        print(f"  Тариф подключён. Баланс: {user.account.balance} ₽")
