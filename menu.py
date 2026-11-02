from pathlib import Path

from subscription import PLANS


def show_section(title):
    print(f"\n── {title} " + "─" * max(2, 40 - len(title)))


def read_text(prompt):
    while True:
        text = input(f"  {prompt}: ").strip()
        if text:
            return text
        print("  Поле пустое. Попробуйте ещё раз.")


def read_number(prompt):
    while True:
        try:
            return int(input(f"  {prompt}: ").strip())
        except ValueError:
            print("  Введите целое число.")


def choose_item(title, items, describe=str):
    """Возвращает выбранный элемент или None, если пользователь нажал 0."""
    show_section(title)

    if not items:
        print("  Список пока пуст.")
        return None

    for number, item in enumerate(items, start=1):
        print(f"  {number:>2}. {describe(item)}")
    print("   0. Назад")

    while True:
        number = read_number("Ваш выбор")
        if number == 0:
            return None
        if 1 <= number <= len(items):
            return items[number - 1]
        print(f"  Выберите номер от 0 до {len(items)}.")


def read_filename(file_format):
    extension = "." + file_format.lower()

    while True:
        filename = read_text(f"Имя файла, например cinema{extension}")
        suffix = Path(filename).suffix.lower()

        if not suffix:
            return filename + extension
        if suffix == extension:
            return filename

        print(f"  Для формата {file_format} укажите расширение {extension}.")


def show_menu(user):
    show_section("ОНЛАЙН-КИНОТЕАТР")

    if user is None:
        print("  Гость")
    else:
        plan_id = user.account.plan_id
        tariff = PLANS[plan_id].name if plan_id is not None else "не подключён"
        print(f"  {user.name}  |  Баланс: {user.account.balance} ₽  |  Тариф: {tariff}")

    print()
    print("  КАТАЛОГ   │1. Фильмы     2. Добавить    3. Смотреть    4. Рекомендации")
    print("  АККАУНТ   │5. Создать    6. Выбрать     7. Пополнить   8. Тарифы   9. История")
    print("  ФАЙЛЫ     │10.Сохранить  11. Загрузить")
    print()
    print("  0.ВЫХОД")