from menu import choose_item, read_number, read_text, show_section
from subscription import PLANS
from user import User


def create_user(cinema):
    show_section("Новый пользователь")
    name = read_text("Ваше имя")

    user = User(name)
    cinema.add_user(user)

    print(f"  Аккаунт создан. Вы вошли как {user.name}.")
    return user


def select_user(cinema, current_user):
    selected = choose_item(
        "Выберите пользователя",
        cinema.users,
        lambda person: person.name,
    )
    if selected is None:
        return current_user

    print(f"   Вы вошли как {selected.name}.")
    return selected


def deposit(user):
    show_section("Пополнение баланса")
    print(f"  На счёте: {user.account.balance} ₽")

    amount = read_number("Сумма в рублях (0 — назад)")
    if amount == 0:
        return

    user.account.deposit(amount)
    print(f"   Новый баланс: {user.account.balance} ₽")


def buy_plan(user):
    choice = choose_item(
        f"Тарифы · на счёте {user.account.balance} ₽",
        list(PLANS),
        lambda key: f"{PLANS[key].name} — {PLANS[key].price} ₽",
    )
    if choice is None:
        return

    user.account.buy_plan(choice)
    print(f"   Подключён тариф «{PLANS[choice].name}».")
    print(f"  Остаток: {user.account.balance} ₽")